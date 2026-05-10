"""知识图谱关系数据"""

# 知识图谱关系定义 (source, target, relation_type, label)
RELATIONS = [
    # ---------- 类别层次 ----------
    ("descriptive_stats", "mean", "contains", "包含概念"),
    ("descriptive_stats", "median", "contains", "包含概念"),
    ("descriptive_stats", "mode", "contains", "包含概念"),
    ("descriptive_stats", "std_dev", "contains", "包含概念"),
    ("descriptive_stats", "variance", "contains", "包含概念"),
    ("descriptive_stats", "correlation", "contains", "包含概念"),
    ("descriptive_stats", "z_score", "contains", "包含概念"),
    ("descriptive_stats", "quantile", "contains", "包含概念"),
    ("descriptive_stats", "histogram", "contains", "包含可视化方法"),
    ("descriptive_stats", "box_plot", "contains", "包含可视化方法"),

    ("inferential_stats", "hypothesis_testing", "contains", "包含方法"),
    ("inferential_stats", "confidence_interval", "contains", "包含方法"),
    ("inferential_stats", "t_test", "contains", "包含方法"),
    ("inferential_stats", "anova", "contains", "包含方法"),
    ("inferential_stats", "chi_square", "contains", "包含方法"),
    ("inferential_stats", "regression", "contains", "包含方法"),
    ("inferential_stats", "sampling_distribution", "contains", "依赖概念"),

    ("probability", "bayes", "contains", "包含定理"),
    ("probability", "normal_distribution", "contains", "包含分布"),
    ("probability", "central_limit_theorem", "contains", "包含定理"),

    # ---------- 依赖关系 ----------
    ("mean", "descriptive_stats", "belongs_to", "属于"),
    ("median", "descriptive_stats", "belongs_to", "属于"),
    ("std_dev", "variance", "derived_from", "由...推导"),
    ("std_dev", "mean", "depends_on", "依赖"),
    ("z_score", "mean", "depends_on", "依赖"),
    ("z_score", "std_dev", "depends_on", "依赖"),
    ("z_score", "standard_normal", "related_to", "相关"),

    ("normal_distribution", "standard_normal", "generalizes", "一般化"),
    ("standard_normal", "normal_distribution", "special_case", "特例"),
    ("normal_distribution", "central_limit_theorem", "related_to", "相关"),

    ("hypothesis_testing", "p_value", "uses", "使用"),
    ("hypothesis_testing", "type_error", "related_to", "涉及"),
    ("hypothesis_testing", "t_test", "has_method", "包含方法"),
    ("hypothesis_testing", "chi_square", "has_method", "包含方法"),
    ("t_test", "anova", "generalizes", "推广"),
    ("t_test", "hypothesis_testing", "belongs_to", "属于"),
    ("chi_square", "hypothesis_testing", "belongs_to", "属于"),
    ("anova", "hypothesis_testing", "belongs_to", "属于"),

    ("confidence_interval", "sampling_distribution", "depends_on", "依赖"),
    ("confidence_interval", "inferential_stats", "belongs_to", "属于"),

    ("sampling_distribution", "central_limit_theorem", "depends_on", "依赖"),
    ("sampling_distribution", "standard_error", "related_to", "相关"),

    ("correlation", "regression", "related_to", "密切相关"),
    ("regression", "r_squared", "evaluated_by", "由...评估"),
    ("regression", "correlation", "related_to", "密切相关"),
    ("regression", "least_squares", "uses", "使用"),

    ("box_plot", "quantile", "uses", "使用"),
    ("box_plot", "median", "uses", "使用"),
    ("histogram", "descriptive_stats", "belongs_to", "属于"),

    ("bayes", "probability", "belongs_to", "属于"),
    ("bayes", "conditional_probability", "depends_on", "依赖"),

    # ---------- 跨类别关联 ----------
    ("inferential_stats", "descriptive_stats", "depends_on", "建立在...基础上"),
    ("central_limit_theorem", "inferential_stats", "supports", "支撑"),
    ("normal_distribution", "inferential_stats", "supports", "支撑"),
    ("t_test", "normal_distribution", "assumes", "假设"),
    ("anova", "normal_distribution", "assumes", "假设"),

    # ---------- 对比关系 ----------
    ("mean", "median", "contrasts", "对比"),
    ("mean", "mode", "contrasts", "对比"),
    ("std_dev", "variance", "contrasts", "对比(单位不同)"),
    ("t_test", "chi_square", "contrasts", "对比(数据类型不同)"),
    ("descriptive_stats", "inferential_stats", "contrasts", "对比(目的不同)"),
]


# 知识图谱元数据
CATEGORY_META = {
    "基础概念": {"color": "#FF6B6B", "icon": "📐"},
    "描述统计": {"color": "#4ECDC4", "icon": "📊"},
    "推断统计": {"color": "#45B7D1", "icon": "🔬"},
    "概率论": {"color": "#96CEB4", "icon": "🎲"},
    "概率分布": {"color": "#FFEAA7", "icon": "📈"},
    "数据可视化": {"color": "#DDA0DD", "icon": "📉"},
}

# 关系类型样式
RELATION_STYLES = {
    "contains": {"color": "#4CAF50", "style": "solid", "label": "包含"},
    "belongs_to": {"color": "#2196F3", "style": "solid", "label": "属于"},
    "depends_on": {"color": "#FF9800", "style": "dashed", "label": "依赖"},
    "related_to": {"color": "#9E9E9E", "style": "dotted", "label": "相关"},
    "contrasts": {"color": "#F44336", "style": "dashed", "label": "对比"},
    "derived_from": {"color": "#9C27B0", "style": "solid", "label": "推导自"},
    "generalizes": {"color": "#00BCD4", "style": "solid", "label": "推广"},
    "special_case": {"color": "#FF5722", "style": "dashed", "label": "特例"},
    "supports": {"color": "#8BC34A", "style": "solid", "label": "支撑"},
    "uses": {"color": "#795548", "style": "solid", "label": "使用"},
    "assumes": {"color": "#E91E63", "style": "dotted", "label": "假设"},
    "evaluated_by": {"color": "#607D8B", "style": "solid", "label": "评估"},
    "has_method": {"color": "#0097A7", "style": "solid", "label": "方法"},
}
