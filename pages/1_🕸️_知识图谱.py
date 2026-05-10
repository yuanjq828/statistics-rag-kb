"""
🕸️ 知识图谱页面 - 交互式概念关系网络
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from core.knowledge_graph import (
    build_knowledge_graph, get_graph_statistics,
    get_knowledge_graph_plotly_data, find_shortest_path,
    get_related_concepts
)
from data.concepts import CONCEPTS, get_concept_by_id


st.set_page_config(page_title="知识图谱", page_icon="🕸️", layout="wide")

with open("static/custom.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def render_graph_page():
    st.markdown("""
    <div class="hero-section">
        <h1>🕸️ 统计学知识图谱</h1>
        <p class="hero-subtitle">探索概念之间的内在联系，构建系统化的知识网络</p>
    </div>
    """, unsafe_allow_html=True)

    # 统计信息
    stats = get_graph_statistics()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📦 概念节点", stats["nodes"])
    with col2:
        st.metric("🔗 关系边", stats["edges"])
    with col3:
        st.metric("📂 知识类别", stats["categories"])
    with col4:
        st.metric("📊 网络密度", f"{stats['density']:.3f}")

    st.markdown("---")

    # 控制面板
    col_left, col_right = st.columns([1, 3])

    with col_left:
        st.markdown("### 🎛️ 控制面板")

        # 选择概念
        concept_names = {c["name"]: c["id"] for c in CONCEPTS}
        selected_name = st.selectbox(
            "🔍 高亮概念",
            ["全部"] + list(concept_names.keys())
        )

        # 显示深度
        show_depth = st.slider("📏 关联深度", 1, 3, 1, help="显示选中概念的相关深度")

        # 布局选择
        layout_option = st.selectbox(
            "🎨 布局方式",
            ["spring", "circular", "kamada_kawai"],
            format_func=lambda x: {"spring": "力导向", "circular": "环形", "kamada_kawai": "能量优化"}.get(x, x)
        )

        st.markdown("---")
        st.markdown("### 📖 图例")

        # 类别图例
        from data.knowledge_graph_data import CATEGORY_META
        for cat, meta in CATEGORY_META.items():
            st.markdown(
                f'<span style="display:inline-block;width:12px;height:12px;'
                f'background:{meta["color"]};border-radius:2px;margin-right:8px;"></span>'
                f'{meta["icon"]} {cat}',
                unsafe_allow_html=True
            )

        st.markdown("---")
        st.markdown("### 📐 路径查找")
        source_name = st.selectbox("起点概念", list(concept_names.keys()), key="path_source")
        target_name = st.selectbox("终点概念", list(concept_names.keys()), key="path_target")
        if st.button("🛤️ 查找最短路径", use_container_width=True):
            path = find_shortest_path(concept_names[source_name], concept_names[target_name])
            if path:
                path_str = " → ".join(p["name"] for p in path)
                st.success(f"路径: {path_str}")
            else:
                st.warning("未找到连接路径")

    with col_right:
        st.markdown("### 🕸️ 知识图谱可视化")

        # 构建图谱数据
        graph_data = get_knowledge_graph_plotly_data()

        # 创建交互式图表
        fig = go.Figure()

        # 添加边
        edge_trace = go.Scatter(
            x=graph_data["edge_x"],
            y=graph_data["edge_y"],
            mode="lines",
            line=dict(width=1, color="#ccc"),
            hoverinfo="none",
            showlegend=False
        )
        fig.add_trace(edge_trace)

        # 添加节点
        node_trace = go.Scatter(
            x=graph_data["node_x"],
            y=graph_data["node_y"],
            mode="markers+text",
            text=graph_data["node_text"],
            textposition="top center",
            textfont=dict(size=10, color="#333"),
            hovertext=graph_data["node_hover"],
            hoverinfo="text",
            marker=dict(
                color=graph_data["node_color"],
                size=graph_data["node_size"],
                line=dict(width=1, color="#fff"),
                symbol="circle"
            ),
            showlegend=False
        )
        fig.add_trace(node_trace)

        # 高亮选中的概念
        if selected_name != "全部":
            selected_id = concept_names[selected_name]
            # 高亮节点
            highlight_indices = [i for i, n in enumerate(graph_data["node_text"]) if n == selected_name]
            if highlight_indices:
                node_trace.marker.color = [
                    "#FFD700" if graph_data["node_text"][i] == selected_name
                    else "rgba(200,200,200,0.4)"
                    for i in range(len(graph_data["node_text"]))
                ]
                node_trace.marker.size = [
                    25 if graph_data["node_text"][i] == selected_name
                    else graph_data["node_size"][i]
                    for i in range(len(graph_data["node_text"]))
                ]
                node_trace.textfont.color = [
                    "#FFD700" if graph_data["node_text"][i] == selected_name
                    else "#999"
                    for i in range(len(graph_data["node_text"]))
                ]

                # 获取相关概念并高亮
                related = get_related_concepts(selected_id, depth=show_depth)
                related_names = {r["concept"]["name"] for r in related if r["concept"]}
                for i, name in enumerate(graph_data["node_text"]):
                    if name != selected_name and name in related_names:
                        node_trace.marker.color[i] = "rgba(102, 126, 234, 0.7)"
                        node_trace.marker.size[i] = 20
                        node_trace.textfont.color[i] = "#667eea"

                st.info(f"✨ 已高亮显示 **{selected_name}** 及其 {show_depth} 层关联概念")

        # 更新布局
        if layout_option == "circular":
            import networkx as nx
            G = build_knowledge_graph()
            pos = nx.circular_layout(G)
            # 更新坐标
            for i, node in enumerate(G.nodes()):
                if i < len(node_trace.x):
                    node_trace.x[i] = pos[node][0]
                    node_trace.y[i] = pos[node][1]

        fig.update_layout(
            title="统计学概念知识图谱",
            title_font_size=16,
            showlegend=False,
            hovermode="closest",
            margin=dict(b=20, l=20, r=20, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=700,
            font=dict(family="sans-serif"),
        )

        st.plotly_chart(fig, use_container_width=True)

    # 底部：概念详情
    if selected_name != "全部":
        st.markdown("---")
        st.markdown(f"### 📖 {selected_name} 详情")
        concept = get_concept_by_id(concept_names[selected_name])
        if concept:
            from core.wiki_cards import render_wiki_card
            st.markdown(render_wiki_card(concept["id"]), unsafe_allow_html=True)

            # 显示相关概念
            related = get_related_concepts(concept["id"], depth=2)
            if related:
                st.markdown("#### 🔗 关联概念")
                for r in related:
                    if r["concept"]:
                        st.markdown(f"- **{r['concept']['name']}** ({r['relation']})")


if __name__ == "__main__":
    render_graph_page()
