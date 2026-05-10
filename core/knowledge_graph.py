"""知识图谱构建与管理模块"""

import networkx as nx
from data.concepts import CONCEPTS, get_concept_by_id
from data.knowledge_graph_data import RELATIONS, CATEGORY_META, RELATION_STYLES


def build_knowledge_graph() -> nx.DiGraph:
    """构建完整的知识图谱有向图"""
    G = nx.DiGraph()

    # 添加概念节点
    for concept in CONCEPTS:
        meta = CATEGORY_META.get(concept["category"], {"color": "#999", "icon": "📄"})
        G.add_node(
            concept["id"],
            label=concept["name"],
            category=concept["category"],
            color=meta["color"],
            icon=meta["icon"],
            difficulty=concept["difficulty"],
            summary=concept["summary"],
            name_en=concept["name_en"]
        )

    # 添加关系边
    for source, target, rel_type, label in RELATIONS:
        style = RELATION_STYLES.get(rel_type, {"color": "#999", "style": "solid", "label": label})
        if G.has_node(source) and G.has_node(target):
            G.add_edge(
                source, target,
                relation=rel_type,
                label=style["label"],
                color=style["color"],
                style=style["style"]
            )

    return G


def get_related_concepts(concept_id: str, depth: int = 1) -> list:
    """获取与指定概念相关的概念（广度优先）"""
    G = build_knowledge_graph()
    if concept_id not in G:
        return []

    related = {}
    visited = {concept_id}
    current_level = {concept_id}

    for _ in range(depth):
        next_level = set()
        for node in current_level:
            # 前向邻居
            for neighbor in G.successors(node):
                if neighbor not in visited:
                    edge_data = G.get_edge_data(node, neighbor)
                    related[neighbor] = {
                        "concept": get_concept_by_id(neighbor),
                        "relation": edge_data.get("label", ""),
                        "direction": "outgoing"
                    }
                    visited.add(neighbor)
                    next_level.add(neighbor)
            # 后向邻居
            for neighbor in G.predecessors(node):
                if neighbor not in visited:
                    edge_data = G.get_edge_data(neighbor, node)
                    related[neighbor] = {
                        "concept": get_concept_by_id(neighbor),
                        "relation": edge_data.get("label", ""),
                        "direction": "incoming"
                    }
                    visited.add(neighbor)
                    next_level.add(neighbor)
        current_level = next_level
        if not current_level:
            break

    return list(related.values())


def get_graph_statistics() -> dict:
    """获取知识图谱的统计信息"""
    G = build_knowledge_graph()
    return {
        "nodes": G.number_of_nodes(),
        "edges": G.number_of_edges(),
        "categories": len(set(nx.get_node_attributes(G, "category").values())),
        "density": nx.density(G),
        "avg_degree": sum(dict(G.degree()).values()) / G.number_of_nodes() if G.number_of_nodes() > 0 else 0,
    }


def find_shortest_path(source: str, target: str) -> list:
    """查找两个概念之间的最短路径"""
    G = build_knowledge_graph()
    try:
        path = nx.shortest_path(G, source=source, target=target)
        path_with_names = []
        for node_id in path:
            concept = get_concept_by_id(node_id)
            path_with_names.append({
                "id": node_id,
                "name": concept["name"] if concept else node_id
            })
        return path_with_names
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        return []


def get_concepts_by_difficulty(min_level: int = 1, max_level: int = 5) -> list:
    """根据难度范围获取概念"""
    return [c for c in CONCEPTS if min_level <= c["difficulty"] <= max_level]


def get_knowledge_graph_plotly_data() -> tuple:
    """生成适用于Plotly可视化的图数据"""
    G = build_knowledge_graph()
    pos = nx.spring_layout(G, k=1.5, iterations=50, seed=42)

    # 节点坐标
    node_x = []
    node_y = []
    node_text = []
    node_color = []
    node_size = []
    node_hover = []

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        data = G.nodes[node]
        node_text.append(data.get("label", node))
        node_color.append(data.get("color", "#999"))
        # 根据难度调整节点大小
        diff = data.get("difficulty", 1)
        node_size.append(15 + diff * 5)
        # 悬停信息
        hover = (
            f"<b>{data.get('label', node)}</b><br>"
            f"英文: {data.get('name_en', '')}<br>"
            f"类别: {data.get('category', '')}<br>"
            f"难度: {'⭐' * data.get('difficulty', 1)}<br>"
            f"{data.get('summary', '')}"
        )
        node_hover.append(hover)

    # 边坐标
    edge_x = []
    edge_y = []
    edge_text = []
    edge_color_list = []

    for edge in G.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        # 每条边需要两个点（起点和终点），中间加None断开
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_text.append(edge[2].get("label", ""))
        edge_color_list.append(edge[2].get("color", "#999"))

    return {
        "edge_x": edge_x,
        "edge_y": edge_y,
        "edge_text": edge_text,
        "edge_color": edge_color_list,
        "node_x": node_x,
        "node_y": node_y,
        "node_text": node_text,
        "node_color": node_color,
        "node_size": node_size,
        "node_hover": node_hover,
    }
