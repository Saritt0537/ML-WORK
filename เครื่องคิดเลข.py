import streamlit as st

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Cal Sud Hod", page_icon="🧮", layout="centered")

# ตกแต่ง CSS ให้เป็นธีมสีแดงดำ (Red-Black Theme)
st.markdown("""
    <style>
    .block-container {
        max-width: 450px;
        padding-top: 2rem;
    }
    .stButton>button {
        width: 100%;
        height: 60px;
        font-size: 22px;
        font-weight: bold;
        border-radius: 10px;
        background-color: #1a1a1a;
        color: #ffffff;
        border: 1px solid #333333;
        transition: 0.1s;
    }
    .stButton>button:hover {
        background-color: #2c2c2c;
        border-color: #ff3333;
        color: #ff3333;
    }
    /* ปรับแต่งสีปุ่ม C ให้เป็นสีแดงเด่นชัด */
    div[data-testid="column"]:nth-of-type(1) div.stButton>button {
        background-color: #b30000;
        border: 1px solid #ff1a1a;
        color: white;
    }
    div[data-testid="column"]:nth-of-type(1) div.stButton>button:hover {
        background-color: #e60000;
    }
    </style>
""", unsafe_allow_html=True)

# จัดการสถานะการคำนวณผ่าน st.session_state
if "display" not in st.session_state:
    st.session_state.display = "0"

def click_btn(val):
    current = st.session_state.display
    if val == "C" or current == "Error":
        st.session_state.display = "0"
    elif val == "=":
        try:
            expr = current.replace("×", "*").replace("÷", "/")
            result = str(eval(expr))
            st.session_state.display = result
        except:
            st.session_state.display = "Error"
    else:
        if current == "0" and val not in ["+", "-", "×", "÷"]:
            st.session_state.display = val
        else:
            st.session_state.display += val

# เปลี่ยนชื่อหัวข้อหลักด้านบน
st.markdown("<h2 style='text-align: center; color: #ff3333;'>🧮 Cal Sud Hod</h2>", unsafe_allow_html=True)

# หน้าจอ LCD แสดงผลลัพธ์ (ดีไซน์สีแดงดำ)
st.markdown(f"""
    <div style="background-color: #121212; padding: 15px; border-radius: 10px; text-align: right; margin-bottom: 20px; border: 2px solid #b30000;">
        <span style="font-family: monospace; font-size: 36px; font-weight: bold; color: #ff3333;">{st.session_state.display}</span>
    </div>
""", unsafe_allow_html=True)

# แผงปุ่มกด (จัดเรียง 4 คอลัมน์)
buttons = [
    ["C", "(", ")", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "=", ""]
]

for row in buttons:
    cols = st.columns(4)
    for i, char in enumerate(row):
        if char != "":
            with cols[i]:
                if st.button(char, key=f"btn_{char}"):
                    click_btn(char)
                    st.rerun()