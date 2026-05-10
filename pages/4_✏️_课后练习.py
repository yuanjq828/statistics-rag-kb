"""
✏️ 课后练习页面 - 分类分级的练习题
"""

import streamlit as st
from data.exercises import EXERCISES, get_exercises_by_concept, get_exercises_by_category
from data.concepts import CONCEPTS, get_concept_by_id
from data.knowledge_graph_data import CATEGORY_META


st.set_page_config(page_title="课后练习", page_icon="✏️", layout="wide")

with open("static/custom.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# 初始化session状态
if "show_answer" not in st.session_state:
    st.session_state["show_answer"] = {}

if "exercise_answered" not in st.session_state:
    st.session_state["exercise_answered"] = {}


def render_exercises_page():
    st.markdown("""
    <div class="hero-section">
        <h1>✏️ 课后练习</h1>
        <p class="hero-subtitle">分类分级的练习题，帮助巩固和深化统计学知识</p>
    </div>
    """, unsafe_allow_html=True)

    # 筛选面板
    col1, col2, col3 = st.columns(3)

    with col1:
        categories = ["全部题型", "choice (选择题)", "calculation (计算题)", "essay (论述题)"]
        selected_cat = st.selectbox("📋 题型筛选", categories)
        cat_map = {
            "全部题型": None,
            "choice (选择题)": "choice",
            "calculation (计算题)": "calculation",
            "essay (论述题)": "essay"
        }

    with col2:
        difficulties = ["全部难度", "1星 (基础)", "2星 (简单)", "3星 (中等)", "4星 (较难)", "5星 (挑战)"]
        selected_diff = st.selectbox("⭐ 难度筛选", difficulties)

    with col3:
        # 按相关概念筛选
        concept_list = ["全部概念"] + sorted([c["name"] for c in CONCEPTS])
        selected_concept = st.selectbox("🔗 相关概念", concept_list)

    # 搜索
    search_query = st.text_input("🔍 搜索题目", placeholder="输入关键词搜索题目...")

    st.markdown("---")

    # 过滤练习
    filtered = EXERCISES

    if selected_cat != "全部题型":
        cat_key = cat_map[selected_cat]
        filtered = [ex for ex in filtered if ex["category"] == cat_key]

    if selected_diff != "全部难度":
        diff_level = int(selected_diff[0])
        filtered = [ex for ex in filtered if ex["difficulty"] == diff_level]

    if selected_concept != "全部概念":
        concept_obj = get_concept_by_id(
            next(c["id"] for c in CONCEPTS if c["name"] == selected_concept)
        )
        if concept_obj:
            filtered = [ex for ex in filtered if concept_obj["id"] in ex.get("concepts", [])]

    if search_query:
        filtered = [
            ex for ex in filtered
            if search_query.lower() in ex["question"].lower()
            or search_query.lower() in ex.get("explanation", "").lower()
        ]

    st.markdown(f"**共 {len(filtered)} 道练习题**")

    # 统计
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("选择题", len([e for e in filtered if e["category"] == "choice"]))
    with col2:
        st.metric("计算题", len([e for e in filtered if e["category"] == "calculation"]))
    with col3:
        st.metric("论述题", len([e for e in filtered if e["category"] == "essay"]))

    st.markdown("---")

    # 显示练习
    for ex in filtered:
        with st.container():
            # 难度标签
            diff_stars = "⭐" * ex["difficulty"]
            cat_label = {"choice": "选择题", "calculation": "计算题", "essay": "论述题"}.get(ex["category"], ex["category"])

            st.markdown(f"""
            <div class="exercise-card">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <strong style="font-size:1.05rem;">📝 {ex['question'][:100]}{'...' if len(ex['question']) > 100 else ''}</strong>
                    <span>
                        <span style="background:#e0f2fe;padding:0.15rem 0.5rem;border-radius:0.25rem;font-size:0.8rem;">{cat_label}</span>
                        <span style="margin-left:8px;color:#f59e0b;">{diff_stars}</span>
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # 显示完整题目
            st.markdown(f"**{ex['question']}**")

            # 选择题选项
            if ex["options"]:
                option_key = f"option_{ex['id']}"
                selected_option = st.radio(
                    "选择答案：",
                    ex["options"],
                    key=option_key,
                    index=None,
                    label_visibility="collapsed"
                )

                col_a, col_b = st.columns([1, 1])
                with col_a:
                    if st.button("✅ 提交答案", key=f"submit_{ex['id']}", use_container_width=True):
                        if selected_option:
                            user_letter = selected_option[0]
                            is_correct = user_letter.upper() == ex["answer"].strip().upper()
                            st.session_state["exercise_answered"][ex["id"]] = {
                                "user_answer": user_letter,
                                "is_correct": is_correct
                            }
                        else:
                            st.warning("请先选择一个选项")

                with col_b:
                    if st.button("💡 显示答案", key=f"show_{ex['id']}", use_container_width=True):
                        st.session_state["show_answer"][ex["id"]] = True

                # 显示结果
                if ex["id"] in st.session_state.get("exercise_answered", {}):
                    result = st.session_state["exercise_answered"][ex["id"]]
                    if result["is_correct"]:
                        st.success(f"✅ 正确！答案就是 {ex['answer']}")
                    else:
                        st.error(f"❌ 不正确。正确答案是 {ex['answer']}，你选的是 {result['user_answer']}")

            else:
                # 简答题/计算题
                if st.button("💡 显示答案/解析", key=f"show_{ex['id']}", use_container_width=True):
                    st.session_state["show_answer"][ex["id"]] = True

            # 显示答案和解析
            if st.session_state.get("show_answer", {}).get(ex["id"]):
                st.markdown(f"""
                <div style="background:#f0fdf4;padding:1rem;border-radius:0.5rem;border-left:3px solid #22c55e;margin:0.5rem 0;">
                    <strong>✅ 参考答案：</strong><br>
                    {ex['answer']}
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div style="background:#f8fafc;padding:1rem;border-radius:0.5rem;border-left:3px solid #667eea;margin:0.5rem 0;">
                    <strong>📖 解析：</strong><br>
                    {ex['explanation']}
                </div>
                """, unsafe_allow_html=True)

                if ex.get("hint"):
                    st.markdown(f"""
                    <div style="background:#fffbeb;padding:0.5rem 1rem;border-radius:0.5rem;border-left:3px solid #f59e0b;margin:0.5rem 0;">
                        <strong>💡 提示：</strong> {ex['hint']}
                    </div>
                    """, unsafe_allow_html=True)

                # 相关概念
                if ex.get("concepts"):
                    st.markdown("**🔗 相关概念：**")
                    cols = st.columns(len(ex["concepts"]))
                    for i, cid in enumerate(ex["concepts"]):
                        concept = get_concept_by_id(cid)
                        if concept:
                            meta = CATEGORY_META.get(concept["category"], {"color": "#999", "icon": "📄"})
                            cols[i].markdown(
                                f'<span style="display:inline-block;padding:0.2rem 0.6rem;'
                                f'background:{meta["color"]}22;color:{meta["color"]};'
                                f'border-radius:0.25rem;font-size:0.8rem;">'
                                f'{meta["icon"]} {concept["name"]}</span>',
                                unsafe_allow_html=True
                            )

            st.markdown("---")


if __name__ == "__main__":
    render_exercises_page()
