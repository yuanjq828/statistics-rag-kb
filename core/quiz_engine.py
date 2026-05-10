"""测验与练习引擎模块"""

import random
from typing import List, Dict, Any, Optional
from data.exercises import EXERCISES, get_exercises_by_concept, get_exercises_by_category
from data.quizzes import QUIZZES, get_quiz_by_id, get_score_level


class QuizSession:
    """测验会话管理"""

    def __init__(self, quiz_id: str):
        self.quiz_id = quiz_id
        self.quiz_data = get_quiz_by_id(quiz_id)

        if self.quiz_data is None:
            raise ValueError(f"未找到测验: {quiz_id}")

        # 加载题目
        self.questions = []
        for qid in self.quiz_data["questions"]:
            for ex in EXERCISES:
                if ex["id"] == qid:
                    self.questions.append(ex)
                    break

        # 状态
        self.current_index = 0
        self.answers = {}  # question_id -> user_answer
        self.start_time = None
        self.finished = False
        self.shuffle_questions()

    def shuffle_questions(self):
        """打乱题目顺序"""
        random.shuffle(self.questions)

    @property
    def total_questions(self) -> int:
        """总题数"""
        return len(self.questions)

    @property
    def current_question(self) -> Optional[Dict]:
        """当前题目"""
        if 0 <= self.current_index < len(self.questions):
            return self.questions[self.current_index]
        return None

    @property
    def progress(self) -> float:
        """答题进度（0~1）"""
        if self.total_questions == 0:
            return 0
        return min(self.current_index / self.total_questions, 1)

    def submit_answer(self, answer: str):
        """提交答案"""
        q = self.current_question
        if q:
            self.answers[q["id"]] = {
                "user_answer": answer,
                "correct_answer": q["answer"],
                "is_correct": q["answer"].upper() == answer.strip().upper() if q["options"] else False,
                "question": q
            }

    def next_question(self):
        """下一题"""
        if self.current_index < self.total_questions - 1:
            self.current_index += 1
        else:
            self.finished = True

    def prev_question(self):
        """上一题"""
        if self.current_index > 0:
            self.current_index -= 1

    def get_results(self) -> Dict:
        """获取测验结果"""
        correct = sum(1 for a in self.answers.values() if a.get("is_correct"))
        total = len(self.answers)
        score = (correct / total * 100) if total > 0 else 0
        level = get_score_level(score)

        incorrect_questions = [
            a for a in self.answers.values() if not a.get("is_correct")
        ]

        return {
            "quiz_title": self.quiz_data["title"],
            "total": total,
            "correct": correct,
            "score": round(score, 1),
            "level": level,
            "incorrect_questions": incorrect_questions,
            "answers": self.answers,
        }


def get_practice_recommendations(wrong_concepts: List[str]) -> List[Dict]:
    """根据错误概念推荐相关练习"""
    recommended = []
    seen_ids = set()

    for concept_id in wrong_concepts:
        exercises = get_exercises_by_concept(concept_id)
        for ex in exercises:
            if ex["id"] not in seen_ids:
                recommended.append(ex)
                seen_ids.add(ex["id"])

    return recommended[:10]
