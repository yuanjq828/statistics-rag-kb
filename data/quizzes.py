"""在线测验数据"""

QUIZZES = [
    {
        "id": "quiz_basic",
        "title": "统计学基础概念测验",
        "description": "测试您对统计学基本概念的掌握程度，包括描述统计与推断统计的区别、集中趋势和离散程度度量。",
        "questions": [
            "ex_001", "ex_002", "ex_003", "ex_004", "ex_005",
            "ex_006", "ex_007", "ex_008", "ex_011", "ex_028"
        ],
        "time_limit": 15,
        "passing_score": 60,
        "difficulty": "easy"
    },
    {
        "id": "quiz_intermediate",
        "title": "概率与推断统计测验",
        "description": "测试您在概率论、假设检验、置信区间等推断统计方面的知识水平。",
        "questions": [
            "ex_009", "ex_010", "ex_012", "ex_013", "ex_014",
            "ex_015", "ex_017", "ex_019", "ex_020", "ex_021"
        ],
        "time_limit": 20,
        "passing_score": 60,
        "difficulty": "medium"
    },
    {
        "id": "quiz_advanced",
        "title": "回归分析与综合应用测验",
        "description": "测试您在回归分析、相关分析以及综合应用方面的能力，包含多种题型。",
        "questions": [
            "ex_016", "ex_018", "ex_022", "ex_023", "ex_024",
            "ex_025", "ex_026", "ex_027", "ex_029", "ex_030"
        ],
        "time_limit": 30,
        "passing_score": 50,
        "difficulty": "hard"
    },
    {
        "id": "quiz_full",
        "title": "统计学综合能力测验",
        "description": "全面的统计学知识测验，涵盖描述统计、推断统计、概率论、回归分析等所有核心内容。",
        "questions": [f"ex_{i:03d}" for i in range(1, 31)],
        "time_limit": 45,
        "passing_score": 60,
        "difficulty": "mixed"
    },
]


# 测验成绩等级
SCORE_LEVELS = [
    {"min": 90, "level": "优秀 🏆", "description": "您对统计学的理解非常透彻！"},
    {"min": 75, "level": "良好 🌟", "description": "您掌握了大部分核心概念，继续加油！"},
    {"min": 60, "level": "合格 ✅", "description": "您已掌握基本概念，建议复习薄弱环节。"},
    {"min": 0, "level": "待提高 📚", "description": "建议重新学习相关概念，打好基础。"},
]


def get_quiz_by_id(quiz_id: str) -> dict:
    """根据ID获取测验"""
    for q in QUIZZES:
        if q["id"] == quiz_id:
            return q
    return None


def get_score_level(score: float) -> dict:
    """根据分数获取等级"""
    for level in SCORE_LEVELS:
        if score >= level["min"]:
            return level
    return SCORE_LEVELS[-1]
