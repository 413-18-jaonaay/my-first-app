import time
import random
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="เกมบวกลบเลขจับเวลา")
st.title("➕➖ เกมบวกลบเลขจับเวลา")

# ระดับความยาก: กำหนดช่วงตัวเลขตามหลัก
LEVELS = {
    "Level 1 (หลักหน่วย 1-9)": (1, 9),
    "Level 2 (หลักสิบ 10-99)": (10, 99),
    "Level 3 (หลักร้อย 100-999)": (100, 999),
    "Level 4 (หลักพัน 1000-9999)": (1000, 9999),
}

# 🏆 ระดับฝีมือ (rank) ตามเปอร์เซ็นต์ความถูกต้อง
RANKS = [
    (0, 39, "🌱 Noob"),
    (40, 59, "⚙️ Pro"),
    (60, 79, "💻 Hacker"),
    (80, 99, "👑 Master"),
    (100, 100, "⚡ God"),
]


def get_rank(score, total):
    if total == 0:
        return "🌱 Noob"
    percent = (score / total) * 100
    for low, high, name in RANKS:
        if low <= percent <= high:
            return name
    return "🌱 Noob"


# 1. กำหนดค่าเริ่มต้นใน session_state ถ้ายังไม่มี
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "input_key" not in st.session_state:
    st.session_state.input_key = 0
if "is_ended" not in st.session_state:
    st.session_state.is_ended = False
if "score" not in st.session_state:
    st.session_state.score = 0
if "question_no" not in st.session_state:
    st.session_state.question_no = 0
if "last_submitted_key" not in st.session_state:
    st.session_state.last_submitted_key = None
if "feedback" not in st.session_state:
    st.session_state.feedback = None


# 🎯 ฟังก์ชันสุ่มโจทย์ใหม่ตามระดับที่เลือก
def new_question():
    low, high = LEVELS[st.session_state.level]
    st.session_state.num1 = random.randint(low, high)
    st.session_state.num2 = random.randint(low, high)
    st.session_state.op = random.choice(["+", "-"])
    st.session_state.input_key += 1  # เปลี่ยน key เพื่อเคลียร์ช่องตอบ


# 🎯 ฟังก์ชันเริ่มเกมใหม่ (ตั้งเวลา + ระดับ)
def start_game(minutes, level):
    st.session_state.level = level
    st.session_state.time_limit = minutes * 60
    st.session_state.start = time.time()
    st.session_state.score = 0
    st.session_state.question_no = 0
    st.session_state.is_ended = False
    st.session_state.feedback = None
    st.session_state.game_started = True
    new_question()


# 🎯 ฟังก์ชันตรวจคำตอบ (เรียกตอนกด Enter ในช่องกรอกคำตอบ)
def handle_answer(input_key):
    # กันไม่ให้ตรวจคำตอบซ้ำสำหรับข้อเดิม
    if st.session_state.last_submitted_key == input_key:
        return
    st.session_state.last_submitted_key = input_key

    answer = st.session_state.get(input_key, "")

    if st.session_state.op == "+":
        correct_answer = st.session_state.num1 + st.session_state.num2
    else:
        correct_answer = st.session_state.num1 - st.session_state.num2

    try:
        user_answer = int(answer.strip())
    except ValueError:
        user_answer = None

    st.session_state.question_no += 1
    if user_answer == correct_answer:
        st.session_state.feedback = ("success", "✅ ถูกต้อง!")
        st.session_state.score += 1
    else:
        st.session_state.feedback = ("error", f"❌ ผิด! เฉลยคือ {correct_answer}")

    new_question()


# ---------------------------------------------------------
# 🎯 ฟังก์ชัน MessageBox (Dialog) สรุปผล
# ---------------------------------------------------------
@st.dialog("📊 สรุปผลการเล่นเกม")
def show_result_dialog(score, total, elapsed):
    st.balloons()

    rank = get_rank(score, total)
    percent = (score / total * 100) if total > 0 else 0

    st.markdown(f"## {rank}")
    st.write(f"ระดับที่เล่น: **{st.session_state.level}**")
    st.write(f"ตอบถูก: **{score} / {total} ข้อ** ({percent:.0f}%)")
    st.write(f"เวลาที่ใช้: **{elapsed:.1f} วินาที**")

    if st.button("🔄 เล่นใหม่"):
        st.session_state.game_started = False
        st.session_state.is_ended = False
        st.rerun()


# ---------------------------------------------------------
# หน้าตั้งค่าก่อนเริ่มเกม
# ---------------------------------------------------------
if not st.session_state.game_started:
    st.subheader("⚙️ ตั้งค่าเกม")

    minutes = st.number_input(
        "ตั้งเวลาเล่น (นาที):", min_value=1, max_value=60, value=3, step=1
    )
    level = st.selectbox("เลือกระดับความยาก:", list(LEVELS.keys()))

    if st.button("▶️ เริ่มเกม", type="primary"):
        start_game(minutes, level)
        st.rerun()

else:
    elapsed_time = time.time() - st.session_state.start
    remaining_time = max(0, st.session_state.time_limit - elapsed_time)

    # ถ้าหมดเวลาให้จบเกมทันที (เช็คฝั่ง server ตอนโหลด/กดปุ่ม)
    if remaining_time <= 0 and not st.session_state.is_ended:
        st.session_state.is_ended = True

    # แสดงคะแนนและข้อที่ตอบแล้ว
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("คะแนน", st.session_state.score)
    with col2:
        st.metric("ข้อที่ตอบแล้ว", st.session_state.question_no)
    with col3:
        # นาฬิกานับถอยหลังฝั่ง client ด้วย JS ไม่รีเฟรชหน้า จึงไม่รบกวนการพิมพ์
        remaining_ms = int(remaining_time * 1000)
        components.html(
            f"""
            <div style="font-size:2rem; font-weight:600; text-align:center;
                        font-family: 'Source Sans Pro', sans-serif;">
                ⏱️ <span id="timer">--:--</span>
            </div>
            <script>
                let remaining = {remaining_ms};
                const el = document.getElementById("timer");
                function tick() {{
                    if (remaining <= 0) {{
                        el.textContent = "00:00";
                        return;
                    }}
                    remaining -= 1000;
                    let totalSec = Math.floor(remaining / 1000);
                    let m = Math.floor(totalSec / 60).toString().padStart(2, '0');
                    let s = (totalSec % 60).toString().padStart(2, '0');
                    el.textContent = m + ":" + s;
                }}
                let totalSec0 = Math.floor(remaining / 1000);
                let m0 = Math.floor(totalSec0 / 60).toString().padStart(2, '0');
                let s0 = (totalSec0 % 60).toString().padStart(2, '0');
                el.textContent = m0 + ":" + s0;
                setInterval(tick, 1000);
            </script>
            """,
            height=60,
        )

    st.caption(f"ระดับ: {st.session_state.level}")
    st.divider()

    if not st.session_state.is_ended:
        # แสดงโจทย์
        st.header(f"{st.session_state.num1} {st.session_state.op} {st.session_state.num2} = ?")

        current_key = f"ans_val_{st.session_state.input_key}"
        st.text_input(
            "กรอกคำตอบ แล้วกด Enter เพื่อส่งคำตอบ:",
            key=current_key,
            on_change=handle_answer,
            args=(current_key,),
        )

        # แจ้งผลลัพธ์ของข้อก่อนหน้า (ถูก/ผิด) ไว้ด้านล่างช่องตอบ
        if st.session_state.feedback:
            kind, msg = st.session_state.feedback
            getattr(st, kind)(msg)

        # โฟกัสกลับไปที่ช่องกรอกคำตอบให้อัตโนมัติ เพื่อให้พิมพ์ต่อเนื่องได้
        # โดยไม่ต้องคลิกเมาส์ใหม่ทุกครั้งหลังตอบ
        components.html(
            """
            <script>
                setTimeout(function() {
                    const inputs = window.parent.document.querySelectorAll('input[type="text"]');
                    if (inputs.length > 0) {
                        const target = inputs[inputs.length - 1];
                        target.focus();
                    }
                }, 60);
            </script>
            """,
            height=0,
        )

    st.divider()
    if st.button("⏹️ จบเกม / เริ่มใหม่"):
        st.session_state.game_started = False
        st.session_state.is_ended = False
        st.rerun()

    # เมื่อหมดเวลา ให้เปิด Dialog สรุปผล
    if st.session_state.is_ended:
        show_result_dialog(st.session_state.score, st.session_state.question_no, elapsed_time)
