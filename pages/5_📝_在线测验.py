"""
📝 在线测验页面 - 限时测验挑战
"""

import streamlit as st
from data.exercises import EXERCISES
from data.quizzes import QUIZZES, get_quiz_by_id
from data.concepts import get_concept_by_id
from data.knowledge_graph_data import CATEGORY_META
from core.quiz_engine import QuizSession, get_practice_recommendations


st.set_page_config(page_title="在线测验", page_icon="📝", layout="wide")

with open("static/custom.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# 初始化session状态
if "quiz_session" not in st.session_state:
    st.session_state["quiz_session"] = None

if "quiz_results" not in st.session_state:
    st.session_state["quiz_results"] = None

if "quiz_page" not in st.session_state:
    st.session_state["quiz_page"] = "select"  # select, taking, results


def render_quiz_page():
    # 顶部
    if st.session_state["quiz_page"] == "select":
        render_quiz_selection()
    elif st.session_state["quiz_page"] == "taking":
        render_quiz_taking()
    elif st.session_state["quiz_page"] == "results":
        render_quiz_results()


def render_quiz_selection():
    st.markdown("""
    <div class="hero-section">
        <h1>📝 在线测验</h1>
        <p class="hero-subtitle">限时测验挑战，检验你的统计学知识水平</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # 测验列表
    for quiz in QUIZZES:
        with st.container():
            diff_badge = {
                "easy": "🟢 基础",
                "medium": "🟡 中等",
                "hard": "🔴 困难",
                "mixed": "🟣 综合"
            }.get(quiz["difficulty"], "⚪ 未知")

            st.markdown(f"""
            <div class="case-card">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <h3>{quiz['title']}</h3>
                        <p style="color:#666;margin:0.3rem 0;">{quiz['description']}</p>
                    </div>
                    <div style="text-align:right;">
                        <span style="font-size:1.2rem;">{diff_badge}</span><br>
                        <small>⏱ {quiz['time_limit']}分钟 | 📝 {len(quiz['questions'])}题</small><br>
                        <small>✅ {quiz['passing_score']}分及格</small>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(
                f"🚀 开始 {quiz['title']}",
                key=f"start_{quiz['id']}",
                use_container_width=True
            ):
                try:
                    st.session_state["quiz_session"] = QuizSession(quiz["id"])
                    st.session_state["quiz_page"] = "taking"
                    st.session_state["quiz_results"] = None
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))

            st.markdown("<br>", unsafe_allow_html=True)

    # 答题记录
    if st.session_state.get("quiz_results"):
        st.markdown("---")
        st.markdown("### 📊 最近的测验结果")
        results = st.session_state["quiz_results"]
        st.markdown(f"""
        <div style="background:white;padding:1.5rem;border-radius:1rem;box-shadow:0 2px 8px rgba(0,0,0,0.08);">
            <h4>{results.get('quiz_title', '')}</h4>
            <p>得分: <strong>{results.get('score', 0)}</strong> 分 |
               正确: {results.get('correct', 0)}/{results.get('total', 0)} |
               等级: <strong>{results.get('level', {}).get('level', '')}</strong>
            </p>
            <p>{results.get('level', {}).get('description', '')}</p>
        </div>
        """, unsafe_allow_html=True)


def render_quiz_taking():
    session = st.session_state["quiz_session"]

    if session is None:
        st.error("会话异常，请重新选择测验")
        st.session_state["quiz_page"] = "select"
        st.rerun()
        return

    if session.finished:
        results = session.get_results()
        st.session_state["quiz_results"] = results
        st.session_state["quiz_page"] = "results"
        st.rerun()
        return

    # 测验头部
    st.markdown(f"""
    <div class="quiz-header">
        <h2>{session.quiz_data['title']}</h2>
        <p>⏱ {session.quiz_data['time_limit']}分钟 | ✅ {session.quiz_data['passing_score']}分及格</p>
    </div>
    """, unsafe_allow_html=True)

    # 进度
    progress_text = f"第 {session.current_index + 1} / {session.total_questions} 题"
    st.progress(session.progress, text=progress_text)
    st.markdown(f"<p style='text-align:center;color:#666;'>{progress_text}</p>", unsafe_allow_html=True)

    st.markdown("---")

    # 当前题目
    q = session.current_question
    if q:
        cat_label = {"choice": "选择题", "calculation": "计算题", "essay": "论述题"}.get(q["category"], q["category"])
        diff_stars = "⭐" * q["difficulty"]

        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;align-items:center;">
            <h3>📝 题目</h3>
            <span>
                <span style="background:#e0f2fe;padding:0.15rem 0.5rem;border-radius:0.25rem;font-size:0.8rem;">{cat_label}</span>
                <span style="margin-left:8px;color:#f59e0b;">{diff_stars}</span>
            </span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"**{q['question']}**")

        # 选择题
        if q["options"]:
            answer_key = f"quiz_answer_{q['id']}"
            selected = st.radio(
                "请选择：",
                q["options"],
                key=answer_key,
                index=None,
                label_visibility="collapsed"
            )

            # 先前的答案
            prev_answer = session.answers.get(q["id"], {})
            if prev_answer:
                for i, opt in enumerate(q["options"]):
                    if opt.startswith(prev_answer.get("user_answer", "")):
                        selected = opt
                        break

        else:
            # 简答题/计算题
            answer_key = f"quiz_text_{q['id']}"
            selected = st.text_area(
                "请输入你的答案：",
                key=answer_key,
                placeholder="在此输入你的答案..."
            )

        # 操作按钮
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            if session.current_index > 0:
                if st.button("⬅️ 上一题", use_container_width=True):
                    session.prev_question()
                    st.rerun()

        with col2:
            btn_label = "✅ 提交并下一题" if session.current_index < session.total_questions - 1 else "✅ 完成测验"
            if st.button(btn_label, use_container_width=True, type="primary"):
                if selected is not None and selected:
                    # 提取选项字母
                    if q["options"]:
                        user_answer = selected[0]
                    else:
                        user_answer = selected

                    session.submit_answer(user_answer)
                    session.next_question()
                    st.rerun()
                else:
                    st.warning("请先回答本题")

        with col3:
            if st.button("⏹️ 提前交卷", use_container_width=True):
                session.finished = True
                st.rerun()

        # 提示（可选的）
        if q.get("hint"):
            with st.expander("💡 查看提示"):
                st.markdown(q["hint"])

        # 进度详情
        answered_count = len(session.answers)
        st.markdown(f"""
        <div style="text-align:center;color:#888;margin-top:1rem;">
            <small>已答 {answered_count}/{session.total_questions} 题</small>
        </div>
        """, unsafe_allow_html=True)


def render_quiz_results():
    results = st.session_state.get("quiz_results")
    if not results:
        st.error("没有测验结果")
        st.session_state["quiz_page"] = "select"
        st.rerun()
        return

    st.markdown("""
    <div class="hero-section">
        <h1>📊 测验结果</h1>
    </div>
    """, unsafe_allow_html=True)

    # 分数展示
    score = results["score"]
    level = results.get("level", {})

    # 根据分数显示不同颜色
    if score >= 90:
        color = "#22c55e"
    elif score >= 75:
        color = "#3b82f6"
    elif score >= 60:
        color = "#f59e0b"
    else:
        color = "#ef4444"

    st.markdown(f"""
    <div style="text-align:center;padding:2rem;background:white;border-radius:1rem;box-shadow:0 2px 8px rgba(0,0,0,0.08);margin-bottom:1.5rem;">
        <h2 style="color:{color};">{score} 分</h2>
        <h3>{level.get('level', '')}</h3>
        <p style="color:#666;">{level.get('description', '')}</p>
        <p style="color:#888;">正确 {results['correct']}/{results['total']} 题</p>
    </div>
    """, unsafe_allow_html=True)

    # 进度条
    st.progress(score / 100)
    st.markdown(f"<p style='text-align:center;'>{results.get('quiz_title', '')}</p>", unsafe_allow_html=True)

    # 错题回顾
    incorrect = results.get("incorrect_questions", [])
    if incorrect:
        st.markdown("---")
        st.markdown("### ❌ 错题回顾")

        # 收集错题涉及的概念
        wrong_concepts = []

        for i, wrong in enumerate(incorrect, 1):
            q_data = wrong.get("question", {})
            with st.expander(f"第{i}题: {q_data.get('question', '')[:80]}..."):
                st.markdown(f"**题目：** {q_data.get('question', '')}")
                if q_data.get("options"):
                    st.markdown(f"**你的答案：** {wrong.get('user_answer', '')}")
                    st.markdown(f"**正确答案：** {wrong.get('correct_answer', '')}")
                st.markdown(f"**解析：** {q_data.get('explanation', '')}")

                # 收集概念
                for cid in q_data.get("concepts", []):
                    wrong_concepts.append(cid)

        # 推荐练习
        if wrong_concepts:
            st.markdown("---")
            st.markdown("### 📚 针对性练习推荐")
            recommendations = get_practice_recommendations(wrong_concepts)
            if recommendations:
                for rec in recommendations[:5]:
                    st.markdown(f"- {rec['question'][:80]}...")
            else:
                st.info("已完成所有相关练习！")

    # 概念掌握情况
    st.markdown("---")
    st.markdown("### 📈 概念掌握情况")
    all_concepts = set()
    for answer in results.get("answers", {}).values():
        q = answer.get("question", {})
        for cid in q.get("concepts", []):
            all_concepts.add(cid)

    if all_concepts:
        cols = st.columns(min(len(all_concepts), 5))
        for i, cid in enumerate(all_concepts):
            concept = get_concept_by_id(cid)
            if concept:
                meta = CATEGORY_META.get(concept["category"], {"color": "#999", "icon": "📄"})
                cols[i % 5].markdown(
                    f'<span style="display:block;padding:0.3rem 0.6rem;'
                    f'background:{meta["color"]}22;color:{meta["color"]};'
                    f'border-radius:0.25rem;font-size:0.85rem;text-align:center;">'
                    f'{meta["icon"]} {concept["name"]}</span>',
                    unsafe_allow_html=True
                )

    # 操作按钮
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 重新测验", use_container_width=True):
            st.session_state["quiz_session"] = None
            st.session_state["quiz_page"] = "select"
            st.rerun()

    with col2:
        if st.button("🏠 返回首页", use_container_width=True):
            st.session_state["quiz_page"] = "select"
            st.switch_page("app.py")


if __name__ == "__main__":
    render_quiz_page()
