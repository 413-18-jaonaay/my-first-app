import time
import random
import streamlit as st

st.title("➕➖ เกมบวกลบเลขจับเวลา")

# 1. กำหนดค่าเริ่มต้นใน session_state ถ้ายังไม่มี
if "num1" not in st.session_state:
    st.session_state.num1 = random.randint(1, 50)
if "num2" not in st.session_state:
    st.session_state.num2 = random.randint(1, 50)
if "op" not in st.session_state:
    st.session_state.op = random.choice(["+", "-"])
if "input_key" not in st.session_state:
    st.session_state.input_key = 0
if "start" not in st.session_state:
    st.session_state.start = time.time()
if "is_ended" not in st.session_state:
    st.session_state.is_ended = False
if "score" not in st.session_state:
    st.session_state.score = 0
if "question_no" not in st.session_state:
    st.session_state.question_no = 1


# 🎯 ฟังก์ชันสุ่มโจทย์ใหม่
def new_question():
    st.session_state.num1 = random.randint(1, 50)
    st.session_state.num2 = random.randint(1, 50)
    st.session_state.op = random.choice(["+", "-"])
    st.session_state.input_key += 1  # เปลี่ยน key เพื่อเคลียร์ช่องตอบ


# 🎯 ฟังก์ชันเคลียร์ค่าเมื่อกดปุ่มเริ่มใหม่
def reset_game():
    st.session_state.score = 0
    st.session_state.question_no = 1
    st.session_state.input_key += 1  # เปลี่ยน key เพื่อเคลียร์ช่องตอบ
    st.session_state.start = time.time()  # เริ่มเวลาใหม่
    st.session_state.is_ended = False  # ปิด Dialog
    new_question()


# ---------------------------------------------------------
# 🎯 ฟังก์ชัน MessageBox (Dialog)
# ---------------------------------------------------------
@st.dialog("📊 สรุปผลการเล่นเกม")
def show_result_dialog(score, total, elapsed):
    st.balloons()

    st.write(f"คะแนนที่ทำได้: **{score} / {total}**")
    st.write(f"เวลาที่ใช้: **{elapsed:.1f} วินาที**")

    if score == total:
        st.success("✅ เยี่ยมมาก! ตอบถูกทุกข้อ")
    elif score >= total * 0.6:
        st.info("👍 ทำได้ดี ลองอีกครั้งเพื่อทำคะแนนเต็ม")
    else:
        st.error("❌ ยังไม่ผ่านเกณฑ์ ลองใหม่อีกครั้ง")

    if st.button("🔄 เริ่มเกมใหม่"):
        reset_game()
        st.rerun()


TOTAL_QUESTIONS = 10  # จำนวนข้อทั้งหมดที่ต้องตอบ

# แสดงคะแนนและข้อที่กำลังเล่น
col1, col2 = st.columns(2)
with col1:
    st.metric("คะแนน", st.session_state.score)
with col2:
    st.metric("ข้อที่", f"{st.session_state.question_no} / {TOTAL_QUESTIONS}")

# แสดงเวลาที่ผ่านไป
elapsed_time = time.time() - st.session_state.start
st.write(f"⏱️ เวลาที่ผ่านไป: **{elapsed_time:.1f} วินาที**")

st.divider()

# แสดงโจทย์
st.header(f"{st.session_state.num1} {st.session_state.op} {st.session_state.num2} = ?")

answer = st.text_input("กรอกคำตอบ:", key=f"ans_val_{st.session_state.input_key}")

if st.button("ตอบ", type="primary"):
    if st.session_state.op == "+":
        correct_answer = st.session_state.num1 + st.session_state.num2
    else:
        correct_answer = st.session_state.num1 - st.session_state.num2

    try:
        user_answer = int(answer.strip())
    except ValueError:
        user_answer = None

    if user_answer == correct_answer:
        st.success("✅ ถูกต้อง!")
        st.session_state.score += 1
    else:
        st.error(f"❌ ยังไม่ถูกต้อง (เฉลย: {correct_answer})")

    if st.session_state.question_no >= TOTAL_QUESTIONS:
        st.session_state.is_ended = True
    else:
        st.session_state.question_no += 1
        new_question()
        st.rerun()

st.divider()
if st.button("🔄 เริ่มเกมใหม่"):
    reset_game()
    st.rerun()

# เมื่อเล่นครบทุกข้อ ให้เปิด Dialog สรุปผล
if st.session_state.is_ended:
    total_elapsed = time.time() - st.session_state.start
    show_result_dialog(st.session_state.score, TOTAL_QUESTIONS, total_elapsed)


