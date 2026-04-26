# 일반 상식 퀴즈 — Streamlit 중간고사 대체 과제

> **2022204052 백지윤**

---

## 프로젝트 소개

한국 영화와 드라마 속 명대사를 보고 어떤 작품인지 맞히는 객관식 4지선다 퀴즈 앱입니다.
문제는 매번 랜덤 순서로 출제되며, 틀린 문제는 결과 화면에서 오답 노트로 확인할 수 있습니다.

---

## 필수 기능 구현 내용

### 1. 로그인 기능

- 아이디 / 비밀번호 입력 방식
- 미리 정의된 사용자 딕셔너리(`USERS`)와 비교하여 로그인 성공/실패 처리
- `st.session_state.logged_in`으로 로그인 상태 구분
- 로그인 전에는 퀴즈 화면 접근 불가

### 2. 캐싱 기능 (`@st.cache_data`)

- `load_quiz_data()` 함수에 적용
- **캐싱이 필요한 이유**: Streamlit은 버튼 클릭 등 매 상호작용마다 전체 스크립트를 재실행합니다.  
  캐싱 없이는 매번 디스크에서 `quiz_data.json`을 읽게 되지만,  
  `@st.cache_data`를 적용하면 최초 1회만 파일을 읽고 이후에는 메모리에서 즉시 반환합니다.

### 3. 퀴즈 기능

- 총 15문제 · 객관식 4지선다
- 문제 제시 → 보기 선택 → 정답/오답 즉시 확인 → 최종 결과 확인
- 문제 랜덤 출제
- 결과 화면: 점수, 정답률, 오답 노트

---

## 실행 방법

```bash
# 1. 저장소 클론
git clone https://github.com/baekjiyun/oss_streamlit_quiz.git
cd oss_streamlit_quiz

# 2. 가상환경 생성 및 활성화 (Mac/Linux)
python3 -m venv venv
source venv/bin/activate

# 3. 패키지 설치
pip install -r requirements.txt

# 4. 앱 실행
streamlit run app.py
```

---

## 테스트 계정

| 아이디 | 비밀번호 |
| ------ | -------- |
| admin  | 1234     |
| guest  | 0000     |

---

## 프로젝트 구조

```
streamlit-quiz/
├── app.py              # 메인 실행 파일
├── requirements.txt    # 패키지 목록
├── .gitignore          # Python용 gitignore
├── README.md           # 프로젝트 설명
└── data/
    └── quiz_data.json  # 퀴즈 문제 데이터 (15문제)
```
