# 🎮 배틀그라운드(pubg) 배린이 모의고사

> 중간고사 대체 과제 - Streamlit으로 만든 PUBG 지식 퀴즈 앱

## 📌 제출자 정보

- **학번** : 2022204032
- **이름** : 성경민
- **주제** : 배틀그라운드(PUBG) 게임 지식 퀴즈

## 실행 방법

### 1. 가상 환경 생성
python -m venv venv

### 2. 가상 환경 활성화 (Windows)
venv\Scripts\activate

### 3. 의존성 설치
pip install -r requirements.txt

### 4. Streamlit 앱 실행
streamlit run app.py

## 🔑 테스트 계정

미리 정의된 사용자 정보(`data/users.json`)를 통해 로그인할 수 있습니다.

| 사용자명 | 비밀번호 |
|---------|---------|
| tjdrudals | 1234 |
| demo | demo |

---

## 주요 기능
### 로그인 기능 (users.json 기반 검증)
- `app.py`의 `render_login()` 함수
- `data/users.json`에 미리 정의된 사용자 목록과 비교
- 성공 → `st.session_state.logged_in = True` 후 메인 페이지 이동
- 실패 → `st.error()`로 에러 메시지 표시

### 캐싱 기능 (`@st.cache_data`로 JSON 데이터 로드)
- 세션 상태 관리 (`st.session_state`)
- 10문제 퀴즈 (객관식 / O·X / 주관식 혼합)
- 점수 누적 후 3단계 등급 판정 (배린이 / 배청년 / 고인물)
- `load_users()` 함수 : `data/users.json` 로드
- `load_quiz_data()` 함수 : `data/quiz_questions.json` 로드
- 사이드바에 "캐시 비우기" 버튼 추가 → `st.cache_data.clear()` 호출

### 세션 상태 관리 (`st.session_state`)
프로젝트에서 사용하는 세션 상태 키 :

| 키 | 용도 |
|-----|------|
| `logged_in` | 로그인 여부 |
| `username` | 로그인한 사용자명 |
| `page` | 현재 페이지 (main / quiz / result) |
| `current_question` | 현재 퀴즈 문제 인덱스 |
| `score` | 누적 점수 |
| `answers` | 사용자가 입력한 답변 기록 |
| `quiz_completed` | 퀴즈 완료 여부 |
| `balloons_shown` | 결과 페이지 풍선 효과 표시 여부 |

### 퀴즈 기능
- 문제 유형 : 객관식 (`multiple_choice`) / O·X (`ox`) / 주관식 (`text_input`)
- 보기 미선택 시 경고 메시지 (`st.warning`) 표시
- 문제 간 이동 : "다음 문제" / "이전 문제" 버튼

## 📁 폴더 구조

```
streamlit-pubg-quiz/
├── app.py                      # 메인 실행 파일
├── requirements.txt            # 패키지 의존성 검사
├── .gitignore                  # Python용 gitignore
├── README.md                   # 프로젝트 가이드
│
├── data/
│   ├── quiz_questions.json     # 퀴즈 문제 데이터
│   └── users.json              # 로그인용 사용자 데이터
│
├── assets/
│   └── images/
│       └── FAMAS.jpg           # 8번 문제 이미지
│
└── utils/
    ├── __init__.py
    └── quiz_utils.py           # 등급 판정, 정답 체크 함수
```