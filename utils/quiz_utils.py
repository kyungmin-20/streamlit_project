# 퀴즈 관련 헬퍼 함수


def get_grade(score):
    if score <= 40:
        return {
            "name": "🌱 배린이",
            "short": "[최종 점수 40점 이하 !]",
            "message": "[축하합니다! 당신은 배린이 입니다 ! 아직 배그에 대해서 잘 모르는 상태입니다. 배그를 더 많이 플레이하며 배그에 대한 지식을 쌓아보세요!]"
        }
    elif score <= 69:
        return {
            "name": "⚔️ 배청년",
            "short": "[최종 점수 41점 ~ 69점 !]",
            "message": "[축하합니다! 당신은 배청년 입니다 ! 배그에 대한 기본적인 지식은 가지고 있습니다. 아직 부족합니다. 더 많은 지식을 쌓아보세요 !]"
        }
    else:
        return {
            "name": "🏆 고인물",
            "short": "[최종 점수 70점 이상 !]",
            "message": "[축하합니다! 당신은 고인물 입니다 ! 배그에 대한 깊은 지식을 가지고 있습니다. 정말로 고수네요! 다음 목표를 정해보세요 !]"
        }


def check_answer(question, user_answer):
    """문제 유형에 따라 정답 여부를 판정"""
    q_type = question["type"]

    if q_type == "multiple_choice":
        try:
            user_idx = question["options"].index(user_answer)
        except (ValueError, TypeError):
            return False
        return user_idx == question["correct_answer"]

    elif q_type == "ox":
        if user_answer is None:
            return False
        user_bool = (user_answer == "O")
        return user_bool == question["correct_answer"]

    elif q_type == "text_input":
        if user_answer is None:
            return False
        cleaned = user_answer.strip()
        return cleaned in question["allowed_answers"]

    return False