import streamlit as st
import pandas as pd
import PyPDF2
from docx import Document
from PIL import Image, ImageStat
from textblob import TextBlob

# 1. إعداد الاسم والهوية (تعديل الاسم ليظهر بشكل احترافي)
st.set_page_config(page_title="Solycast AI Platform", layout="wide", page_icon="🌐")

# تصميم الهيدر
st.title("🌐 Solycast Intelligence")
st.markdown("---")

# 2. التبويبات المنظمة
tab1, tab2, tab3 = st.tabs(["📷 Image Analysis", "✍️ Text Sentiment", "📂 Smart File Analyzer"])

# --- التبويب الأول: الصور ---
with tab1:
    st.subheader("Visual Analysis")
    up_img = st.file_uploader("Upload Image", type=['jpg', 'jpeg', 'png'], key="img_up")
    if up_img:
        img = Image.open(up_img)
        st.image(img, width=300)
        if st.button("Analyze Image"):
            stat = ImageStat.Stat(img.convert('L'))
            res = "Positive & Bright 😊" if stat.stddev[0] > 40 else "Neutral/Low Light 😐"
            st.success(f"Visual Result: {res}")

# --- التبويب الثاني: النص المباشر ---
with tab2:
    st.subheader("Instant Sentiment Check")
    user_text = st.text_area("Write your text here:", height=150)
    if st.button("Run AI Analysis"):
        if user_text:
            score = TextBlob(user_text).sentiment.polarity
            if score > 0: st.success(f"Sentiment: Positive 😊 ({score:.2f})")
            elif score < 0: st.error(f"Sentiment: Negative 😡 ({score:.2f})")
            else: st.warning("Sentiment: Neutral 😐")

# --- التبويب الثالث: الملفات الشاملة مع التحليل التلقائي ---
with tab3:
    st.subheader("Universal Document Analyzer")
    up_any = st.file_uploader("Upload PDF, Word, or Excel", type=None, key="file_up")
    
    if up_any:
        name = up_any.name
        ext = name.split('.')[-1].lower()
        content_text = ""

        # استخراج النص بناءً على النوع
        if ext == 'pdf':
            pdf = PyPDF2.PdfReader(up_any)
            content_text = "".join([p.extract_text() for p in pdf.pages])
        elif ext == 'docx':
            doc = Document(up_any)
            content_text = "\n".join([p.text for p in doc.paragraphs])
        elif ext == 'txt':
            content_text = up_any.getvalue().decode("utf-8")
        elif ext in ['xlsx', 'csv']:
            df = pd.read_excel(up_any) if 'xls' in ext else pd.read_csv(up_any)
            st.dataframe(df)
            content_text = " ".join(df.astype(str).values.flatten()[:500]) # تحليل عينة من البيانات

        # إظهار المحتوى + التحليل التلقائي
        if content_text:
            st.text_area("File Content Preview:", content_text[:1000], height=200)
            
            # زر التحليل الذكي للملف
            if st.button("Analyze File Sentiment"):
                analysis = TextBlob(content_text).sentiment.polarity
                if analysis > 0:
                    st.success(f"AI Analysis: This file contains POSITIVE content 😊 (Score: {analysis:.2f})")
                elif analysis < 0:
                    st.error(f"AI Analysis: This file contains NEGATIVE content 😡 (Score: {analysis:.2f})")
                else:
                    st.warning("AI Analysis: This file contains NEUTRAL content 😐")
        
