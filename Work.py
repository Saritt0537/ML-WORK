import streamlit as st
import joblib
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="Iris Predictor Pro",
    page_icon="🌿",
    layout="wide"
)

# ธีมสีขาว-แดง (White & Red Theme)
st.markdown("""
    <style>
    /* พื้นหลังหลักและฟอนต์ภาพรวม */
    .stApp {
        background-color: #FFFFFF;
        color: #D32F2F;
    }
    /* หัวข้อและตัวหนังสือสำคัญ */
    h1, h2, h3, h4, h5, h6 {
        color: #C62828 !important;
    }
    /* ปุ่ม Slider และองค์ประกอบควบคุม */
    .stSlider slider {
        accent-color: #D32F2F !important;
    }
    /* ปรับแต่งส่วน Divider */
    hr {
        border-color: #FFCDD2 !important;
    }
    /* ปรับแต่ง Radio Button เมนูหลักให้เป็นโทนแดง */
    div.row-widget.stRadio > div {
        color: #D32F2F;
    }
    </style>
""", unsafe_allow_html=True)

# โหลดโมเดล
@st.cache_resource
def load_model():
    return joblib.load('iris_model.pkl')

model = load_model()

# โหลดข้อมูล Iris
iris = load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df['target'] = iris.target
target_names = iris.target_names
df['species'] = df['target'].map(lambda x: target_names[x])

# --- Custom Header ---
st.markdown("<h2 style='text-align: center; color: #D32F2F;'>🌿 Iris Flower Species Classification Dashboard</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7F0000;'>ระบบวิเคราะห์และจำแนกสายพันธุ์ดอกไอริสด้วยโมเดล Machine Learning แบบเรียลไทม์</p>", unsafe_allow_html=True)
st.divider()

# เมนูหลักแบบ Radio แนวนอน
selected_tab = st.radio(
    "เลือกเมนูการใช้งาน:",
    ["🎯 หน้าจอทำนายผล (Prediction Panel)", "📊 เจาะลึกข้อมูลดิบ (Dataset & Analytics)"],
    horizontal=True
)

if selected_tab == "🎯 หน้าจอทำนายผล (Prediction Panel)":
    
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("### 🎛️ กำหนดค่าตัวแปร (Features)")
        
        sl = st.slider('ความยาวกลีบเลี้ยง (Sepal Length)', float(df['sepal length (cm)'].min()), float(df['sepal length (cm)'].max()), 5.8)
        sw = st.slider('ความกว้างกลีบเลี้ยง (Sepal Width)', float(df['sepal width (cm)'].min()), float(df['sepal width (cm)'].max()), 3.0)
        pl = st.slider('ความยาวกลีบดอก (Petal Length)', float(df['petal length (cm)'].min()), float(df['petal length (cm)'].max()), 4.3)
        pw = st.slider('ความกว้างกลีบดอก (Petal Width)', float(df['petal width (cm)'].min()), float(df['petal width (cm)'].max()), 1.3)

        # แสดงตารางค่าที่ผู้ใช้เลือก
        st.markdown("#### ค่าที่คุณกำหนด:")
        input_df = pd.DataFrame({
            'Sepal Length': [sl], 'Sepal Width': [sw], 
            'Petal Length': [pl], 'Petal Width': [pw]
        })
        st.dataframe(input_df, hide_index=True)

        # ทำนายผล
        input_data = np.array([[sl, sw, pl, pw]])
        prediction = model.predict(input_data)
        result_name = target_names[prediction[0]].capitalize()

        # แสดงผลลัพธ์
        st.success(f"### ผลการทำนาย: Iris {result_name} 🌺")

    with col2:
        st.markdown("### 📊 กราฟจุด (Scatter Chart) แสดงความน่าจะเป็นของแต่ละสายพันธุ์")
        
        # คำนวณความน่าจะเป็น
        prediction_proba = model.predict_proba(input_data)

        # สร้าง DataFrame สำหรับทำกราฟจุด (แปลงเป็น %)
        proba_df = pd.DataFrame({
            'Species': [name.capitalize() for name in target_names],
            'Probability (%)': (prediction_proba[0] * 100)
        })
        
        # แสดงกราฟจุด (Scatter Chart) โดยอิงตามตารางข้อมูลความน่าจะเป็น
        st.scatter_chart(proba_df, x='Species', y='Probability (%)', color="#D32F2F")

else:
    st.markdown("### 📊 ข้อมูลเชิงสถิติและตัวอย่าง Dataset ทั้งหมด")
    m1, m2, m3 = st.columns(3)
    m1.metric("จำนวนข้อมูลทั้งหมด", f"{len(df)} แถว")
    m2.metric("จำนวนฟีเจอร์", f"{len(iris.feature_names)} คอลัมน์")
    m3.metric("จำนวนสายพันธุ์", f"{len(target_names)} สายพันธุ์")
    st.divider()
    st.dataframe(df, use_container_width=True)