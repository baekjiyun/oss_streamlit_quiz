import streamlit as st
import json
import time
import random
from pathlib import Path

st.set_page_config(
    page_title="한국 영화/드라마 명대사 퀴즈",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');
  html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }

  .stApp { background: #E8EDF2; min-height: 100vh; }

  .header-banner {
      background: #2C3947;
      border-radius: 12px;
      padding: 22px 28px;
      text-align: center;
      margin-bottom: 18px;
  }
  .header-banner h1 { color: white; font-size: 1.9rem; font-weight: 700; margin: 0; }
  .header-banner p  { color: rgba(255,255,255,0.7); font-size: 0.88rem; margin: 5px 0 0; }

  .student-badge {
      background: rgba(255,255,255,0.7);
      border: 1px solid rgba(44,57,71,0.15);
      border-radius: 10px;
      padding: 12px 18px;
      text-align: center;
      margin-bottom: 18px;
  }
  .student-badge .label { color: rgba(44,57,71,0.5); font-size: 0.82rem; margin-bottom: 3px; }
  .student-badge .info  { color: #547A95; font-weight: 700; font-size: 1.05rem; }

  .card {
      background: rgba(255,255,255,0.75);
      border: 1px solid rgba(44,57,71,0.12);
      border-radius: 12px;
      padding: 24px;
      margin-bottom: 16px;
  }
  .card h2 { color: #2C3947; font-size: 1.15rem; font-weight: 700; margin-top: 0; }
  .card h3 { color: #2C3947; font-size: 1.05rem; font-weight: 700; margin-top: 0; }

  .question-number { color: #547A95; font-size: 0.8rem; font-weight: 700; letter-spacing: 0.4px; margin-bottom: 8px; }
  .question-text   { color: #2C3947; font-size: 1.1rem; font-weight: 500; line-height: 1.7; }

  .choice-btn {
      display: block; width: 100%; box-sizing: border-box;
      background: white;
      border: 1px solid rgba(44,57,71,0.2);
      border-radius: 8px;
      padding: 14px 18px;
      color: #2C3947; font-size: 0.95rem;
      text-align: left; margin-bottom: 8px;
      line-height: 1.4;
  }
  .choice-correct  { background: white !important; border-color: #3ecf8e !important; color: #1a7a50 !important; font-weight: 600 !important; }
  .choice-wrong    { background: white !important; border-color: #e05070 !important; color: #b03050 !important; font-weight: 600 !important; }
  .choice-disabled { background: white !important; border-color: rgba(44,57,71,0.1) !important; color: rgba(44,57,71,0.35) !important; }

  .result-correct {
      background: rgba(62,207,142,0.12); border: 1px solid rgba(62,207,142,0.35);
      border-radius: 10px; padding: 12px;
      color: #1a7a50; font-weight: 600; text-align: center; font-size: 0.95rem; margin-top: 10px;
  }
  .result-wrong {
      background: rgba(220,60,90,0.1); border: 1px solid rgba(220,60,90,0.3);
      border-radius: 10px; padding: 12px;
      color: #b03050; font-weight: 600; text-align: center; font-size: 0.95rem; margin-top: 10px;
  }

  .score-board {
      background: rgba(84,122,149,0.1);
      border: 1px solid rgba(84,122,149,0.25);
      border-radius: 12px; padding: 28px; text-align: center; margin: 12px 0 20px;
  }
  .score-board .big-score   { font-size: 3rem; font-weight: 700; color: #547A95; line-height: 1; }
  .score-board .score-label { color: rgba(44,57,71,0.85); font-size: 1rem; margin-top: 8px; }
  .score-board .score-msg   { color: rgba(44,57,71,0.55); font-size: 0.88rem; margin-top: 5px; }

  .stProgress > div > div > div { background: #547A95 !important; }
  .stMarkdown, p, li { color: rgba(44,57,71,0.82); }
  #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

STUDENT_ID   = "2022204052"
STUDENT_NAME = "백지윤"

USERS = {
    "admin": "1234",
    "guest": "0000",
}

@st.cache_data
def load_quiz_data():
    data_path = Path(__file__).parent / "data" / "quiz_data.json"
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def init_session():
    defaults = {
        "logged_in":    False,
        "username":     "",
        "quiz_started": False,
        "quiz_done":    False,
        "current_q":    0,
        "score":        0,
        "answers":      [],
        "selected":     None,
        "answered":     False,
        "quiz_order":   [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()

def reset_quiz():
    keys = [
        "quiz_started", "quiz_done", "current_q", "score",
        "answers", "selected", "answered", "quiz_order",
    ]
    for k in keys:
        if k in st.session_state:
            del st.session_state[k]
    init_session()

st.markdown("""
<div class="header-banner">
  <h1>한국 영화/드라마 명대사 퀴즈</h1>
  <p>대사를 보고 어떤 작품인지 맞혀보세요!</p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="student-badge">
  <div class="label">제출자 정보</div>
  <div class="info">학번 {STUDENT_ID} &nbsp;|&nbsp; {STUDENT_NAME}</div>
</div>
""", unsafe_allow_html=True)

# ── 로그인 화면 ─────────────────────────────────
if not st.session_state.logged_in:

    st.markdown("### 로그인")
    st.markdown(
        '<p style="color:rgba(44,57,71,0.5);font-size:0.88rem;margin-bottom:14px;">'
        '퀴즈를 시작하려면 먼저 로그인하세요.</p>',
        unsafe_allow_html=True
    )

    with st.form("login_form"):
        uid = st.text_input("아이디", placeholder="아이디를 입력하세요")
        pwd = st.text_input("비밀번호", type="password", placeholder="비밀번호를 입력하세요")
        submitted = st.form_submit_button("로그인")

    if submitted:
        if uid in USERS and USERS[uid] == pwd:
            st.session_state.logged_in = True
            st.session_state.username  = uid
            st.success(f"환영합니다, {uid}님!")
            time.sleep(0.5)
            st.rerun()
        else:
            st.markdown(
                '<div class="result-wrong">아이디 또는 비밀번호가 올바르지 않습니다.</div>',
                unsafe_allow_html=True
            )

    with st.expander("테스트 계정 확인"):
        st.markdown("""
| 아이디 | 비밀번호 |
|--------|---------|
| admin  | 1234    |
| guest  | 0000    |
""")

# ── 로그인 후 메인 ───────────────────────────────
else:
    col_user, col_logout = st.columns([6, 1])
    with col_user:
        st.markdown(
            f'<p style="color:#547A95;font-weight:500;margin:0 0 8px;">👤 {st.session_state.username}</p>',
            unsafe_allow_html=True
        )
    with col_logout:
        if st.button("로그아웃"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

    was_cached = "quiz_data_loaded" in st.session_state
    quiz_data = load_quiz_data()
    if not was_cached:
        st.toast("데이터 최초 로드 (파일 읽음)", icon="📂")
        st.session_state.quiz_data_loaded = True
    else:
        st.toast("캐시에서 불러옴 (파일 읽기 없음)", icon="⚡")
    total = len(quiz_data)

    # ── 시작 전 안내 ─────────────────────────────
    if not st.session_state.quiz_started and not st.session_state.quiz_done:

        st.markdown(f"""
<div class="card">
  <h2>퀴즈 소개</h2>
  <p>한국 영화와 드라마 속 <b>명대사</b>를 보고 어떤 작품의 대사인지 맞혀보세요!</p>
  <ul>
    <li>총 <b>{total}문제</b> &nbsp;·&nbsp; 객관식 4지선다</li>
    <li>문제는 매번 <b>랜덤 순서</b>로 출제</li>
    <li>결과 화면에서 <b>오답 노트</b> 제공</li>
  </ul>
</div>
""", unsafe_allow_html=True)

        if st.button("퀴즈 시작"):
            order = list(range(total))
            random.shuffle(order)
            st.session_state.quiz_order   = order
            st.session_state.quiz_started = True
            st.rerun()

    # ── 퀴즈 진행 ────────────────────────────────
    elif st.session_state.quiz_started and not st.session_state.quiz_done:

        idx   = st.session_state.current_q
        q_idx = st.session_state.quiz_order[idx]
        q     = quiz_data[q_idx]

        st.progress(idx / total)
        st.markdown(
            f'<p style="color:rgba(44,57,71,0.5);font-size:0.8rem;text-align:right;margin-top:-6px;">'
            f'{idx} / {total} 완료 &nbsp;·&nbsp; {st.session_state.score}점</p>',
            unsafe_allow_html=True
        )

        with st.container(border=False):
            st.markdown(f'<div class="question-number">문제 {idx + 1} / {total}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="question-text">{q["question"]}</div>', unsafe_allow_html=True)

        with st.container(border=True):
            choices = q["choices"]
            answer  = q["answer"]
            labels  = ["①", "②", "③", "④"]

            if not st.session_state.answered:
                for i, choice in enumerate(choices):
                    if st.button(f"{labels[i]}  {choice}", key=f"c_{idx}_{i}"):
                        st.session_state.selected = choice
                        st.session_state.answered = True
                        if choice == answer:
                            st.session_state.score += 1
                        st.session_state.answers.append({
                            "question_id": q["id"],
                            "question":    q["question"],
                            "selected":    choice,
                            "correct":     (choice == answer),
                            "answer":      answer,
                        })
                        st.rerun()
            else:
                selected = st.session_state.selected
                for i, choice in enumerate(choices):
                    if choice == answer:
                        css, icon = "choice-correct", "✓"
                    elif choice == selected:
                        css, icon = "choice-wrong",   "✗"
                    else:
                        css, icon = "choice-disabled", " "
                    st.markdown(
                        f'<div class="choice-btn {css}">{icon} {labels[i]}  {choice}</div>',
                        unsafe_allow_html=True
                    )

                if selected == answer:
                    st.markdown('<div class="result-correct">정답입니다! +1점</div>', unsafe_allow_html=True)
                else:
                    st.markdown(
                        f'<div class="result-wrong">오답입니다. 정답은 <b>{answer}</b>입니다.</div>',
                        unsafe_allow_html=True
                    )

                st.markdown("<br>", unsafe_allow_html=True)

                if idx + 1 < total:
                    if st.button("다음 문제"):
                        st.session_state.current_q += 1
                        st.session_state.answered   = False
                        st.session_state.selected   = None
                        st.rerun()
                else:
                    if st.button("결과 보기"):
                        st.session_state.quiz_done    = True
                        st.session_state.quiz_started = False
                        st.rerun()

    # ── 결과 화면 ────────────────────────────────
    elif st.session_state.quiz_done:

        score   = st.session_state.score
        answers = st.session_state.answers

        st.markdown(f"""
<div class="score-board">
  <div class="big-score">{score} / {total}</div>
</div>
""", unsafe_allow_html=True)

        correct_pct = int(score / total * 100)
        st.markdown(f"**정답률: {correct_pct}%**")
        st.progress(score / total)

        wrong = [a for a in answers if not a["correct"]]
        if wrong:
            wrong_html = f"""
<div class="card">
  <h3>오답 노트</h3>
  <p style="color:rgba(44,57,71,0.5);font-size:0.84rem;margin-bottom:4px;">총 {len(wrong)}문제 틀렸어요. 복습해보세요!</p>
"""
            for a in wrong:
                wrong_html += f"""
<p style="border-bottom:1px solid rgba(44,57,71,0.1);padding:12px 0;color:rgba(44,57,71,0.82);margin:0;">
  <b style="color:#2C3947;">Q. {a['question']}</b><br>
  <span style="color:#b03050;">✗ 내 답: {a['selected']}</span>
  &nbsp;&nbsp;→&nbsp;&nbsp;
  <span style="color:#1a7a50;">✓ 정답: {a['answer']}</span>
</p>
"""
            wrong_html += "</div>"
            st.markdown(wrong_html, unsafe_allow_html=True)
        else:
            st.markdown('<div class="result-correct">모든 문제를 맞혔어요! 오답이 없습니다.</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("다시 도전하기"):
                reset_quiz()
                st.rerun()
        with col2:
            if st.button("처음으로 돌아가기"):
                reset_quiz()
                st.rerun()
