"""数据模型定义"""
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class Concept:
    """统计学概念"""
    id: str
    name: str              # 概念名称（中文）
    name_en: str           # 英文名称
    category: str          # 类别：描述统计/推断统计/概率论/...
    summary: str           # 简短定义（一句话）
    description: str       # 详细解释
    formula: str = ""      # 公式 (LaTeX)
    example: str = ""      # 简单例子
    tags: List[str] = field(default_factory=list)
    related_concepts: List[str] = field(default_factory=list)  # 相关概念ID列表
    difficulty: int = 1    # 难度 1-5
    wiki_content: str = "" # Wiki风格的详细内容


@dataclass
class Relation:
    """知识图谱中的关系"""
    source: str            # 源概念ID
    target: str            # 目标概念ID
    relation: str          # 关系类型：is_a / part_of / related_to / depends_on / opposite
    label: str = ""        # 关系描述


@dataclass
class Case:
    """案例"""
    id: str
    title: str
    field: str             # 应用领域
    description: str       # 案例描述
    problem: str           # 问题背景
    solution: str          # 解决方案
    code_example: str = "" # 代码示例
    concepts: List[str] = field(default_factory=list)  # 涉及的概念ID
    difficulty: int = 1


@dataclass
class Exercise:
    """课后练习"""
    id: str
    question: str          # 题目
    options: List[str] = field(default_factory=list)  # 选择题选项
    answer: str            # 答案
    explanation: str       # 解析
    category: str = "choice"  # choice /填空 / calculation / essay
    difficulty: int = 1    # 难度 1-5
    concepts: List[str] = field(default_factory=list)  # 相关概念
    hint: str = ""


@dataclass
class Quiz:
    """测验"""
    id: str
    title: str
    description: str
    questions: List[str] = field(default_factory=list)  # 题目ID列表
    time_limit: int = 30   # 时间限制(分钟)
    passing_score: int = 60  # 及格分
    difficulty: str = "medium"
