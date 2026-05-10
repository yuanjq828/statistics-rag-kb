"""
📖 Wiki卡片页面 - 统计学概念百科全书
"""

import re
import streamlit as st
from data.concepts import CONCEPTS, get_concept_by_id, get_all_categories
from data.knowledge_graph_data import CATEGORY_META
from core.wiki_cards import search_concepts


st.set_page_config(page_title="Wiki卡片", page_icon="📖", layout="wide")

with open("static/custom.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def _wiki_to_streamlit(md_text: str) -> str:
    """将Wiki内容中的Markdown转为Streamlit友好的格式"""
    if not md_text:
        return ""
    text = md_text
    text = re.sub(r'^### (.+)$', r'##### \1', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.+)$', r'#### \1', text, flags=re.MULTILINE)
    return text


def render_wiki_page():
    st.markdown("""
    <div class="hero-section">
        <h1>📖 Wiki 卡片</h1>
        <p class="hero-subtitle">统计学核心概念的百科全书，涵盖定义、公式、实例与应用</p>
    </div>
    """, unsafe_allow_html=True)

    # 搜索栏
    search_query = st.text_input(
        "🔍 搜索概念（支持中文/英文/关键词）",
        placeholder="例如：均值、正态分布、t-test...",
        label_visibility="visible"
    )

    # 分类筛选
    categories = ["全部"] + get_all_categories()
    selected_category = st.selectbox("📂 按类别筛选", categories)

    # 难度筛选
    difficulty = st.slider("⭐ 最低难度", 1, 5, 1)

    st.markdown("---")

    # 获取概念列表
    if search_query:
        concepts = search_concepts(search_query)
        if not concepts:
            st.warning(f"未找到与 '{search_query}' 相关的概念")
            concepts = CONCEPTS
    else:
        concepts = CONCEPTS

    # 按类别筛选
    if selected_category != "全部":
        concepts = [c for c in concepts if c["category"] == selected_category]

    # 按难度筛选
    concepts = [c for c in concepts if c["difficulty"] >= difficulty]

    if not concepts:
        st.info("没有符合条件的概念")
        return

    # 布局：左侧为概念列表，右侧为详情
    left_col, right_col = st.columns([1, 2.5])

    with left_col:
        st.markdown(f"**共 {len(concepts)} 个概念**")
        for c in concepts:
            meta = CATEGORY_META.get(c["category"], {"color": "#999", "icon": "📄"})
            if st.button(
                f"{meta['icon']} {c['name']}  ({c['name_en']})",
                key=f"btn_{c['id']}",
                use_container_width=True,
                help=c["summary"]
            ):
                st.session_state["selected_concept"] = c["id"]

    with right_col:
        # 获取选中的概念
        concept_id = st.session_state.get("selected_concept")
        if concept_id is None and concepts:
            concept_id = concepts[0]["id"]
            st.session_state["selected_concept"] = concept_id

        if concept_id:
            concept = get_concept_by_id(concept_id)
            if concept:
                meta = CATEGORY_META.get(concept["category"], {"color": "#999", "icon": "📄"})

                # === 使用 Streamlit 原生组件渲染 Wiki 卡片 ===
                with st.container():
                    # 卡片容器（带背景和阴影）
                    st.markdown(f"""
                    <div style="background:white;border-radius:12px;padding:24px 28px;
                                box-shadow:0 2px 12px rgba(0,0,0,0.08);margin-bottom:20px;">
                    """, unsafe_allow_html=True)

                    # ---- 头部 ----
                    col_icon, col_title = st.columns([1, 8])
                    with col_icon:
                        st.markdown(f"<span style='font-size:40px;line-height:1;'>{meta['icon']}</span>",
                                    unsafe_allow_html=True)
                    with col_title:
                        st.markdown(
                            f"<h2 style='margin:0;color:#1a1a2e;font-size:1.5rem;'>{concept['name']}</h2>"
                            f"<span style='color:#999;font-style:italic;'>{concept['name_en']}</span>"
                            f"<div style='margin-top:4px;'>"
                            f"<span style='background:{meta['color']};color:white;padding:2px 12px;"
                            f"border-radius:20px;font-size:0.8rem;margin-right:8px;'>{concept['category']}</span>"
                            f"<span style='color:#f59e0b;font-size:0.85rem;'>{'⭐' * concept['difficulty']}</span>"
                            f"</div>",
                            unsafe_allow_html=True
                        )

                    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

                    # ---- 定义 ----
                    st.info(f"📖 **定义：** {concept['summary']}")

                    # ---- 详细解释 ----
                    st.markdown(f"**📝 详细解释：**")
                    st.markdown(concept['description'])

                    # ---- 公式 ----
                    if concept.get("formula"):
                        st.markdown("")
                        st.latex(concept["formula"])

                    # ---- 实例 ----
                    st.markdown(f"""
                    <div style="background:#fffbeb;padding:14px 18px;border-radius:8px;
                                border-left:4px solid #f59e0b;margin:12px 0;color:#444;">
                        <strong>💡 实例：</strong><br>{concept['example']}
                    </div>
                    """, unsafe_allow_html=True)

                    # ---- Wiki内容 ----
                    wiki_content = concept.get("wiki_content", "")
                    if wiki_content:
                        st.markdown("---")
                        st.markdown(_wiki_to_streamlit(wiki_content))

                    # ---- 标签 ----
                    if concept.get("tags"):
                        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
                        tags_html = " ".join(
                            f'<span style="background:#eef2ff;color:#4f46e5;padding:4px 12px;'
                            f'border-radius:20px;font-size:0.8rem;margin:0 4px 4px 0;display:inline-block;">'
                            f'#{tag}</span>' for tag in concept['tags']
                        )
                        st.markdown(f'<div>{tags_html}</div>', unsafe_allow_html=True)

                    st.markdown("</div>", unsafe_allow_html=True)

                # ---- 相关概念导航 ----
                if concept.get("related_concepts"):
                    st.markdown("---")
                    st.markdown("##### 🔗 相关概念")
                    rel_cols = st.columns(min(len(concept["related_concepts"]), 4))
                    for i, rel_id in enumerate(concept["related_concepts"]):
                        rel_c = get_concept_by_id(rel_id)
                        if rel_c:
                            c_meta = CATEGORY_META.get(rel_c["category"], {"color": "#999", "icon": "📄"})
                            with rel_cols[i % 4]:
                                if st.button(
                                    f"{c_meta['icon']} {rel_c['name']}",
                                    key=f"rel_{rel_id}",
                                    use_container_width=True
                                ):
                                    st.session_state["selected_concept"] = rel_id
                                    st.rerun()


if __name__ == "__main__":
    render_wiki_page()
