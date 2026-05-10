"""
📊 案例分析页面 - 真实世界的统计学应用
"""

import streamlit as st
from data.cases import CASES
from data.concepts import get_concept_by_id
from data.knowledge_graph_data import CATEGORY_META


st.set_page_config(page_title="案例分析", page_icon="📊", layout="wide")

with open("static/custom.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def render_cases_page():
    st.markdown("""
    <div class="hero-section">
        <h1>📊 案例分析</h1>
        <p class="hero-subtitle">通过真实世界的案例，理解统计学在医学、教育、经济等领域的应用</p>
    </div>
    """, unsafe_allow_html=True)

    # 筛选
    col1, col2 = st.columns([1, 1])
    with col1:
        fields = ["全部领域"] + sorted(set(c["field"] for c in CASES))
        selected_field = st.selectbox("🏷️ 按领域筛选", fields)
    with col2:
        difficulties = [f"全部难度"] + [f"{i}星" for i in range(1, 6)]
        selected_diff = st.selectbox("⭐ 按难度筛选", difficulties)

    # 过滤案例
    filtered_cases = CASES
    if selected_field != "全部领域":
        filtered_cases = [c for c in filtered_cases if c["field"] == selected_field]
    if selected_diff != "全部难度":
        diff_level = int(selected_diff[0])
        filtered_cases = [c for c in filtered_cases if c["difficulty"] == diff_level]

    st.markdown(f"**共 {len(filtered_cases)} 个案例**")
    st.markdown("---")

    # 案例列表
    for case in filtered_cases:
        with st.container():
            st.markdown(f"""
            <div class="case-card">
                <div class="case-header">
                    <h3>{case['title']}</h3>
                    <span class="case-field-badge">{case['field']}</span>
                    <span style="margin-left: 8px; color: #f59e0b;">
                        {'⭐' * case['difficulty']}
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            with st.expander("📖 查看详情"):
                st.markdown("**📝 案例描述**")
                st.markdown(case["description"])

                st.markdown("**❓ 问题背景**")
                st.markdown(case["problem"])

                st.markdown("**💡 解决方案**")
                st.markdown(case["solution"])

                # 涉及概念
                if case.get("concepts"):
                    st.markdown("**🔗 涉及概念**")
                    cols = st.columns(len(case["concepts"]))
                    for i, cid in enumerate(case["concepts"]):
                        concept = get_concept_by_id(cid)
                        if concept:
                            meta = CATEGORY_META.get(concept["category"], {"color": "#999", "icon": "📄"})
                            cols[i].markdown(
                                f'<span style="display:inline-block;padding:0.2rem 0.6rem;'
                                f'background:{meta["color"]}22;color:{meta["color"]};'
                                f'border-radius:0.25rem;font-size:0.85rem;">'
                                f'{meta["icon"]} {concept["name"]}</span>',
                                unsafe_allow_html=True
                            )

                # 代码示例
                if case.get("code_example"):
                    st.markdown("**💻 代码示例**")
                    st.code(case["code_example"], language="python")

            st.markdown("<br>", unsafe_allow_html=True)


if __name__ == "__main__":
    render_cases_page()
