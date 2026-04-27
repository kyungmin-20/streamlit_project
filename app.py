import streamlit as st
import json
import os
from utils.quiz_utils import get_grade, check_answer

# ===== 페이지 설정 =====
st.set_page_config(page_title="배틀그라운드(pubg) 배린이 모의고사", page_icon="")

# ===== 제출자 정보 =====
STUDENT_ID = "2022204032"
STUDENT_NAME = "성경민"
QUIZ_TITLE = "배틀그라운드(pubg) 배린이 모의고사"


# ===== 캐싱: 데이터 로드 =====
@st.cache_data
def load_users():
    file_path = os.path.join("data", "users.json")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


@st.cache_data
def load_quiz_data():
    file_path = os.path.join("data", "quiz_questions.json")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


# ===== 세션 상태 초기화 =====
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "page" not in st.session_state:
    st.session_state.page = "main"
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "answers" not in st.session_state:
    st.session_state.answers = []
if "quiz_completed" not in st.session_state:
    st.session_state.quiz_completed = False
if "balloons_shown" not in st.session_state:
    st.session_state.balloons_shown = False


def reset_quiz():
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.answers = []
    st.session_state.quiz_completed = False
    st.session_state.balloons_shown = False


# ===== 사이드바 =====
def render_sidebar():
    with st.sidebar:
        st.subheader("👤 사용자 정보")
        if st.session_state.logged_in:
            st.success(f"로그인: {st.session_state.username}")
            if st.button("📤 로그아웃", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.username = ""
                reset_quiz()
                st.session_state.page = "main"
                st.rerun()

            st.markdown("---")
            if st.button("🔄 퀴즈 다시 풀기", use_container_width=True):
                reset_quiz()
                st.session_state.page = "quiz"
                st.rerun()
        else:
            st.info("로그인이 필요합니다.")

        st.markdown("---")
        st.subheader("ℹ️ 앱 정보")
        st.markdown(f"- **학번** : {STUDENT_ID}")
        st.markdown(f"- **이름** : {STUDENT_NAME}")
        st.markdown(f"- **주제** : {QUIZ_TITLE}")

        st.markdown("---")
        st.subheader("🧹 캐시 관리")
        st.caption("캐싱 시연용 — 캐시를 비우고 데이터를 다시 로드합니다.")
        if st.button("캐시 비우기", use_container_width=True):
            st.cache_data.clear()
            st.success("캐시가 초기화되었습니다.")


# ===== 1. 로그인 화면 =====
def render_login():
    st.title(f"🎮 {QUIZ_TITLE}")
    st.write("---")
    st.write(f"**학번:** {STUDENT_ID}")
    st.write(f"**이름:** {STUDENT_NAME}")
    st.write("---")

    st.subheader("🔐 로그인")
    username = st.text_input("사용자명", placeholder="예: demo")
    password = st.text_input("비밀번호", type="password")

    if st.button("로그인"):
        users_data = load_users()
        success = False
        for user in users_data["users"]:
            if user["username"] == username and user["password"] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                success = True
                st.rerun()
                break
        if not success:
            st.error("❌ 사용자명 또는 비밀번호가 올바르지 않습니다.")

    st.caption("테스트 계정: demo / demo")


# ===== 2. 메인 페이지 =====
def render_main():
    st.title(f"👤 {st.session_state.username}님 환영합니다!")
    st.write("---")
    st.subheader(f"🔫 {QUIZ_TITLE}")
    st.write("총 10문제로 구성되어 있습니다. 점수에 따라 등급이 매겨집니다.")
    st.write("- 문제 1~6번: 각 10점")
    st.write("- 문제 7~8번: 각 15점")
    st.write("- 문제 9~10번: 각 5점")
    st.write("**총 100점 만점**")
    st.write("---")

    if st.button(" 퀴즈 시작", use_container_width=True):
        reset_quiz()
        st.session_state.page = "quiz"
        st.rerun()

    if st.session_state.quiz_completed:
        if st.button("📊 이전 결과 보기", use_container_width=True):
            st.session_state.page = "result"
            st.rerun()


# ===== 3. 퀴즈 풀이 페이지 =====
def render_quiz():
    quiz_data = load_quiz_data()
    questions = quiz_data["quiz"]
    total = len(questions)
    idx = st.session_state.current_question

    if idx >= total:
        st.session_state.quiz_completed = True
        st.session_state.page = "result"
        st.rerun()
        return

    st.progress((idx + 1) / total)
    st.write(f"진행: {idx + 1} / {total}")
    st.write("---")

    q = questions[idx]
    st.subheader(f"Q{q['id']}. {q['question']}")

    if "image" in q and q["image"]:
        if os.path.exists(q["image"]):
            st.image(q["image"], width=300)
        else:
            st.warning(f"⚠️ 이미지 파일 없음: {q['image']}")

    user_answer = None
    if q["type"] == "multiple_choice":
        user_answer = st.radio(
            "보기를 선택하세요:",
            q["options"],
            key=f"q{idx}_radio",
            index=None
        )
    elif q["type"] == "ox":
        user_answer = st.radio(
            "선택하세요:",
            ["O", "X"],
            key=f"q{idx}_ox",
            index=None
        )
    elif q["type"] == "text_input":
        user_answer = st.text_input("답변을 입력하세요:", key=f"q{idx}_text")

    st.write("---")

    col1, col2 = st.columns(2)

    with col1:
        if idx > 0:
            if st.button("⬅️ 이전 문제", use_container_width=True):
                if st.session_state.answers:
                    last = st.session_state.answers.pop()
                    if last["is_correct"]:
                        st.session_state.score -= questions[idx - 1]["points"]
                st.session_state.current_question -= 1
                st.rerun()

    with col2:
        if st.button("다음 문제 ➡️", use_container_width=True):
            valid = True
            if q["type"] == "multiple_choice" or q["type"] == "ox":
                if user_answer is None:
                    valid = False
            elif q["type"] == "text_input":
                if not user_answer or not user_answer.strip():
                    valid = False

            if not valid:
                st.warning("보기를 선택해야 다음 문제로 넘어갈 수 있습니다. 보기를 선택한 뒤 진행해주세요.")
            else:
                is_correct = check_answer(q, user_answer)
                if is_correct:
                    st.session_state.score += q["points"]

                st.session_state.answers.append({
                    "question_id": q["id"],
                    "user_answer": user_answer,
                    "is_correct": is_correct
                })
                st.session_state.current_question += 1
                st.rerun()


# ===== 4. 결과 페이지 =====
def render_result():
    score = st.session_state.score
    grade = get_grade(score)
    username = st.session_state.username

    # 풍선 효과 
    if not st.session_state.balloons_shown:
        st.balloons()
        st.session_state.balloons_shown = True

    st.title("🎊 퀴즈 종료!")
    st.write("---")

    # 결과 카드 
    card_html = (
        '<div style="background: linear-gradient(135deg, #FFF1B0 0%, #FFD970 100%); '
        'border-radius: 16px; padding: 32px 24px; text-align: center; '
        'margin: 16px 0; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);">'
        f'<div style="font-size: 14px; color: #6b5c2e; margin-bottom: 18px;">{username} 님의 결과</div>'
        '<div style="font-size: 56px; margin: 12px 0; line-height: 1;">👏</div>'
        f'<div style="font-size: 26px; font-weight: 700; color: #1a1a1a; margin: 12px 0;">{grade["name"]}  {grade["short"]}</div>'
        f'<div style="font-size: 17px; color: #4a4a4a; margin-top: 12px;">'
        f'점수 <strong style="color: #1a1a1a; font-size: 22px;">{score}</strong> / 100</div>'
        '</div>'
    )
    st.markdown(card_html, unsafe_allow_html=True)

    # 결과 멘트 박스 
    message_html = (
        '<div style="background: #1e3a5f; border-radius: 10px; '
        'padding: 18px 20px; color: #a8c8ff; font-size: 14px; '
        'line-height: 1.7; margin: 16px 0 24px 0;">'
        f'{grade["message"]}'
        '</div>'
    )
    st.markdown(message_html, unsafe_allow_html=True)

    st.write("---")

    st.write("**정답 현황** (● 정답 / ○ 오답)")
    result_str = ""
    for ans in st.session_state.answers:
        if ans["is_correct"]:
            result_str += "● "
        else:
            result_str += "○ "
    st.write(result_str)

    st.write("---")

    if st.button("🔄 퀴즈 다시 풀기", use_container_width=True):
        reset_quiz()
        st.session_state.page = "quiz"
        st.rerun()

    if st.button("🏠 메인으로", use_container_width=True):
        st.session_state.page = "main"
        st.rerun()


# ===== 메인 라우팅 =====
render_sidebar()

if not st.session_state.logged_in:
    render_login()
    quiz_data = load_quiz_data()
    description = quiz_data.get("description", "")
    if description:
        with st.expander("🙄 이 앱은 무엇을 진단하나요?"):
            st.markdown(description)
else:
    if st.session_state.page == "main":
        render_main()
    elif st.session_state.page == "quiz":
        render_quiz()
    elif st.session_state.page == "result":
        render_result()