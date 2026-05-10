"""
📊 统计学 RAG 知识库系统
========================
基于检索增强生成（RAG）的交互式统计学学习平台
包含：知识图谱、Wiki卡片、案例分析、课后练习、在线测验
"""

import streamlit as st

# --- 页面配置 ---
st.set_page_config(
    page_title="统计学 RAG 知识库",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- 自定义CSS ---
with open("static/custom.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# --- 侧边栏导航 ---
def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-header">
            <h1>📊 统计学知识库</h1>
            <p class="sidebar-subtitle">RAG 交互式学习平台</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # 统计概览
        st.markdown("### 📈 知识库概览")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("概念数", "25+", delta="核心")
        with col2:
            st.metric("案例数", "8+", delta="实践")

        col3, col4 = st.columns(2)
        with col3:
            st.metric("练习题", "30+", delta="巩固")
        with col4:
            st.metric("测验套", "4", delta="挑战")

        st.markdown("---")

        # RAG 搜索
        st.markdown("### 🔍 RAG 智能搜索")
        with st.form("rag_search_form"):
            query = st.text_input(
                "输入问题或关键词",
                placeholder="例如：什么是中心极限定理？",
                label_visibility="collapsed"
            )
            search_btn = st.form_submit_button("🔍 搜索", use_container_width=True)

        if search_btn and query:
            st.session_state["rag_query"] = query

        st.markdown("---")

        # 学习建议
        st.markdown("### 💡 学习路径建议")
        st.info(
            """
            **新手入门**：
            1. 📖 浏览 Wiki 卡片
            2. 📚 查看知识图谱
            3. ✏️ 做基础练习
            
            **进阶学习**：
            1. 🔬 研究案例分析
            2. 📝 挑战在线测验
            3. 🔍 使用 RAG 搜索
            """
        )

        st.markdown("---")
        st.caption("Powered by RAG + Knowledge Graph")


# --- 主页面 ---
def render_home():
    st.markdown("""
    <div class="hero-section">
        <h1>🎓 统计学 RAG 知识库</h1>
        <p class="hero-subtitle">
            融合知识图谱、语义检索与交互式学习的统计学智慧平台
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 功能区展示
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card" onclick="alert('跳转到知识图谱')">
            <div class="feature-icon">🕸️</div>
            <h3>知识图谱</h3>
            <p>探索统计学概念之间的关系网络，可视化学习路径</p>
            <ul>
                <li>25+ 核心概念节点</li>
                <li>概念间依赖与关联</li>
                <li>交互式探索</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📖</div>
            <h3>Wiki 卡片</h3>
            <p>结构化展示每个概念的完整定义、公式和实例</p>
            <ul>
                <li>中英双语对照</li>
                <li>LaTeX 公式展示</li>
                <li>实例与应用场景</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <h3>案例分析</h3>
            <p>真实世界的统计学应用案例，理论与实践结合</p>
            <ul>
                <li>8+ 跨领域案例</li>
                <li>完整的分析思路</li>
                <li>Python 代码示例</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    col4, col5, col6 = st.columns(3)

    with col4:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">✏️</div>
            <h3>课后练习</h3>
            <p>分类分级的练习题，巩固所学知识</p>
            <ul>
                <li>选择题/计算题/论述题</li>
                <li>难度分级（1-5星）</li>
                <li>详细解析与提示</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📝</div>
            <h3>在线测验</h3>
            <p>限时测验挑战，检验学习成果</p>
            <ul>
                <li>4套完整测验卷</li>
                <li>自动评分与反馈</li>
                <li>薄弱点分析推荐</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col6:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <h3>RAG 智能问答</h3>
            <p>基于检索增强生成的智能问答系统</p>
            <ul>
                <li>语义理解搜索</li>
                <li>多源知识融合</li>
                <li>上下文感知回答</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # RAG 搜索结果显示
    if "rag_query" in st.session_state:
        query = st.session_state["rag_query"]
        st.markdown(f"### 🔍 搜索结果：{query}")
        with st.spinner("正在检索知识库..."):
            from core.rag_engine import get_rag_engine
            engine = get_rag_engine()
            results = engine.search(query, top_k=5)

            if results:
                for i, r in enumerate(results, 1):
                    meta = r["metadata"]
                    with st.expander(f"{i}. [{meta.get('type', '未知').upper()}] {meta.get('name', meta.get('title', r['id']))} (相似度: {r.get('score', 0):.2f})"):
                        st.markdown(r["document"])
            else:
                st.warning("未找到相关结果，试试其他关键词？")


# --- 主逻辑 ---
def main():
    render_sidebar()
    render_home()


if __name__ == "__main__":
    main()
