"""RAG检索引擎模块 - 基于嵌入向量的语义检索"""

import os
import pickle
import hashlib
import numpy as np
from typing import List, Dict, Any, Optional
from data.concepts import CONCEPTS
from data.cases import CASES
from data.exercises import EXERCISES

# 尝试导入可选依赖
try:
    from sentence_transformers import SentenceTransformer
    _HAS_SENTENCE_TRANSFORMERS = True
except ImportError:
    _HAS_SENTENCE_TRANSFORMERS = False

# chromadb 有 protobuf 兼容性问题，延迟到 initialize_chroma() 中导入
_HAS_CHROMADB = False
_HAS_CHROMADB_IMPORT_ERROR = None


# 缓存目录
CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".cache")


class RAGEngine:
    """RAG检索引擎 - 支持知识检索和问答上下文构建"""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        初始化RAG引擎

        Args:
            model_name: 嵌入模型名称（默认使用轻量级模型）
        """
        self.model_name = model_name
        self.model = None
        self.documents = []
        self.document_ids = []
        self.document_metadata = []
        self._embeddings_cache = {}
        self.chroma_client = None
        self.collection = None

        # 初始化时构建文档库
        self._build_document_store()

    def _build_document_store(self):
        """构建文档库（从已有数据构建）"""
        self.documents = []
        self.document_ids = []
        self.document_metadata = []

        # 添加概念文档
        for c in CONCEPTS:
            doc_text = (
                f"概念名称：{c['name']}（{c['name_en']}）\n"
                f"类别：{c['category']}\n"
                f"定义：{c['summary']}\n"
                f"详细解释：{c['description']}\n"
                f"示例：{c['example']}\n"
                f"标签：{'，'.join(c['tags'])}\n"
                f"相关概念：{'，'.join(c.get('related_concepts', []))}\n"
                f"Wiki内容：{c.get('wiki_content', '')}"
            )
            self.documents.append(doc_text)
            self.document_ids.append(f"concept_{c['id']}")
            self.document_metadata.append({
                "type": "concept",
                "id": c["id"],
                "name": c["name"],
                "name_en": c["name_en"],
                "category": c["category"],
                "difficulty": c["difficulty"]
            })

        # 添加案例文档
        for case in CASES:
            doc_text = (
                f"案例：{case['title']}\n"
                f"领域：{case['field']}\n"
                f"描述：{case['description']}\n"
                f"问题：{case['problem']}\n"
                f"解决方案：{case['solution']}\n"
                f"涉及概念：{'，'.join(case['concepts'])}"
            )
            self.documents.append(doc_text)
            self.document_ids.append(f"case_{case['id']}")
            self.document_metadata.append({
                "type": "case",
                "id": case["id"],
                "title": case["title"],
                "field": case["field"],
                "difficulty": case["difficulty"]
            })

        # 添加练习文档
        for ex in EXERCISES:
            doc_text = (
                f"题目：{ex['question']}\n"
                f"答案：{ex['answer']}\n"
                f"解析：{ex['explanation']}\n"
                f"类型：{ex['category']}\n"
                f"难度：{ex['difficulty']}"
            )
            self.documents.append(doc_text)
            self.document_ids.append(f"exercise_{ex['id']}")
            self.document_metadata.append({
                "type": "exercise",
                "id": ex["id"],
                "category": ex["category"],
                "difficulty": ex["difficulty"]
            })

    def _get_embedding_model(self):
        """延迟加载嵌入模型"""
        if self.model is None and _HAS_SENTENCE_TRANSFORMERS:
            try:
                self.model = SentenceTransformer(self.model_name)
            except Exception as e:
                print(f"加载模型失败: {e}")
                self.model = None
        return self.model

    def _build_vocabulary(self, texts: List[str]) -> dict:
        """构建固定词汇表"""
        all_words = set()
        for text in texts:
            for char in text:
                if '\u4e00' <= char <= '\u9fff':  # 中文字符
                    all_words.add(char)
                elif char.isalnum():
                    all_words.add(char.lower())
            for word in text.split():
                if word.isascii():
                    all_words.add(word.lower())
        return {w: i for i, w in enumerate(sorted(all_words))}

    def _compute_embeddings_simple(self, texts: List[str]) -> np.ndarray:
        """使用简单的词袋方法计算嵌入（作为后备方案），保持固定词汇表"""
        if not hasattr(self, '_vocab') or self._vocab is None:
            self._vocab = self._build_vocabulary(self.documents) if hasattr(self, 'documents') and self.documents else {}

        vocab = self._vocab
        if not vocab:
            vocab = self._build_vocabulary(texts)
            self._vocab = vocab

        vectors = np.zeros((len(texts), len(vocab)))
        word_to_idx = vocab

        for i, text in enumerate(texts):
            words = set()
            for char in text:
                if '\u4e00' <= char <= '\u9fff':
                    words.add(char)
                elif char.isalnum():
                    words.add(char.lower())
            for word in text.split():
                if word.isascii():
                    words.add(word.lower())
            for word in words:
                if word in word_to_idx:
                    vectors[i, word_to_idx[word]] += 1

        # L2归一化
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        norms[norms == 0] = 1
        vectors = vectors / norms

        return vectors

    def _compute_embeddings(self, texts: List[str]) -> np.ndarray:
        """计算文本的嵌入向量"""
        model = self._get_embedding_model()
        if model is not None:
            try:
                return model.encode(texts, show_progress_bar=False)
            except Exception:
                pass
        return self._compute_embeddings_simple(texts)

    def initialize_chroma(self, persist_directory: str = None):
        """初始化ChromaDB（可选，延迟导入避免protobuf兼容性问题）"""
        global _HAS_CHROMADB, _HAS_CHROMADB_IMPORT_ERROR

        if _HAS_CHROMADB:
            pass  # 已确认可用
        elif _HAS_CHROMADB_IMPORT_ERROR:
            return False
        else:
            try:
                import chromadb
                from chromadb.config import Settings
                _HAS_CHROMADB = True
            except Exception as e:
                _HAS_CHROMADB = False
                _HAS_CHROMADB_IMPORT_ERROR = str(e)
                return False

        if persist_directory is None:
            persist_directory = os.path.join(CACHE_DIR, "chromadb")

        os.makedirs(persist_directory, exist_ok=True)

        try:
            import chromadb
            from chromadb.config import Settings
            self.chroma_client = chromadb.Client(Settings(
                persist_directory=persist_directory,
                anonymized_telemetry=False
            ))

            # 创建或获取集合
            collection_name = "statistics_kb"
            try:
                self.collection = self.chroma_client.get_collection(collection_name)
            except:
                self.collection = self.chroma_client.create_collection(collection_name)

            return True
        except Exception as e:
            print(f"ChromaDB初始化失败: {e}")
            return False

    def index_to_chroma(self):
        """将文档索引到ChromaDB"""
        if self.collection is None:
            return False

        try:
            # 计算嵌入
            embeddings = self._compute_embeddings(self.documents)

            # 添加到ChromaDB
            self.collection.add(
                embeddings=embeddings.tolist(),
                documents=self.documents,
                metadatas=self.document_metadata,
                ids=self.document_ids
            )
            return True
        except Exception as e:
            print(f"索引到ChromaDB失败: {e}")
            return False

    def search(self, query: str, top_k: int = 5, doc_type: str = None) -> List[Dict[str, Any]]:
        """
        语义搜索

        Args:
            query: 搜索查询
            top_k: 返回结果数量
            doc_type: 过滤类型（concept/case/exercise/None）

        Returns:
            搜索结果列表
        """
        # 计算查询嵌入
        query_embedding = self._compute_embeddings([query])[0]

        # 本地余弦相似度搜索（始终使用，避免chromadb兼容问题）
        doc_embeddings = self._compute_embeddings(self.documents)
        scores = np.dot(doc_embeddings, query_embedding)

        # 按分数排序
        sorted_indices = np.argsort(scores)[::-1]

        results = []
        for idx in sorted_indices:
            if idx < len(self.document_ids):
                meta = self.document_metadata[idx]
                # 按类型过滤
                if doc_type is None or meta.get("type") == doc_type:
                    results.append({
                        "id": self.document_ids[idx],
                        "score": float(scores[idx]),
                        "document": self.documents[idx][:500] + "...",
                        "metadata": meta
                    })
                    if len(results) >= top_k:
                        break

        return results

    def search_by_keyword(self, keyword: str, doc_type: str = None) -> List[Dict[str, Any]]:
        """基于关键词的搜索（补充语义搜索）"""
        keyword = keyword.lower().strip()
        results = []

        for i, doc in enumerate(self.documents):
            if keyword in doc.lower():
                meta = self.document_metadata[i]
                if doc_type is None or meta.get("type") == doc_type:
                    results.append({
                        "id": self.document_ids[i],
                        "document": doc[:500] + "...",
                        "metadata": meta
                    })

        return results[:20]

    def get_rag_context(self, query: str, max_docs: int = 3) -> str:
        """
        构建RAG问答上下文

        Args:
            query: 用户查询
            max_docs: 用于上下文的最大文档数

        Returns:
            格式化的上下文字符串
        """
        results = self.search(query, top_k=max_docs)

        context_parts = []
        for i, r in enumerate(results, 1):
            meta = r["metadata"]
            doc_type = meta.get("type", "unknown")

            if doc_type == "concept":
                header = f"[概念] {meta.get('name', '')} ({meta.get('name_en', '')})"
            elif doc_type == "case":
                header = f"[案例] {meta.get('title', '')}"
            elif doc_type == "exercise":
                header = f"[练习] {meta.get('id', '')}"
            else:
                header = f"[文档] {r['id']}"

            context_parts.append(f"--- 参考{i}: {header} ---\n{r['document']}\n")

        return "\n".join(context_parts)


# 全局单例
_engine = None


def get_rag_engine() -> RAGEngine:
    """获取RAG引擎单例"""
    global _engine
    if _engine is None:
        _engine = RAGEngine()
    return _engine
