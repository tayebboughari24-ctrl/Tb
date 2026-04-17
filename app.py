import streamlit as st
import pandas as pd
import PyPDF2
from docx import Document
from PIL import Image, ImageStat
from textblob import TextBlob

# 1. إعدادات الصفحة
st.set_page_config(page_title="Emotion Analysis", layout="wide", page_icon="📊")

st.title("📊 Emotion Analysis")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📷 Image Vision", "✍️ Text Analysis", "📂 File Analyzer"])

# --- TAB 1: Image (تحليل أعمق بناءً على الألوان) ---
with tab1:
    st.subheader("Visual Emotion Analysis")
    up_img = st.file_uploader("Upload Image", type=['jpg', 'jpeg', 'png'], key="img_up")
    if up_img:
        img = Image.open(up_img)
        st.image(img, width=300)
        
        if st.button("Analyze Image Emotion"):
            # تحليل الألوان (Saturation/Brightness balance)
            stat = ImageStat.Stat(img.convert('RGB'))
            r, g, b = stat.mean
            # معادلة بسيطة: إذا كانت الألوان باهتة جداً يميل للسلبية
            color_intensity = (r + g + b) / 3
            variation = sum(stat.stddev) / 3
            
            if color_intensity > 150 and variation > 30:
                st.success("Result: Positive & Vibrant Tone 😊")
            elif color_intensity < 80:
                st.error("Result: Gloomy & Negative Tone 🌑")
            else:
                st.warning("Result: Neutral/Muted Tone 😐")

# --- TAB 2: Text (تحليل مباشر) ---
with tab2:
    st.subheader("Quick Text Check")
    user_text = st.text_area("Enter text:", height=150)
    if st.button("Analyze Text"):
        if user_text:
            score = TextBlob(user_text).sentiment.polarity
            if score > 0.1: st.success("Outcome: Positive 😊")
            elif score < -0.1: st.error("Outcome: Negative 😡")
            else: st.warning("Outcome: Neutral 😐")

# --- TAB 3: File Analyzer (التحليل بالنسب المئوية الحقيقية) ---
with tab3:
    st.subheader("Advanced File Emotion Analytics")
    up_any = st.file_uploader("Upload PDF, Word, or Excel", type=None, key="file_up")
    
    if up_any:
        name = up_any.name
        ext = name.split('.')[-1].lower()
        full_text = ""

        try:
            if ext == 'pdf':
                pdf = PyPDF2.PdfReader(up_any)
                full_text = " ".join([p.extract_text() for p in pdf.pages])
            elif ext == 'docx':
                doc = Document(up_any)
                full_text = " ".join([p.text for p in doc.paragraphs])
            elif ext == 'txt':
                full_text = up_any.getvalue().decode("utf-8")
            elif ext in ['xlsx', 'csv']:
                df = pd.read_excel(up_any) if 'xls' in ext else pd.read_csv(up_any)
                full_text = " ".join(df.astype(str).values.flatten())

            if full_text.strip():
                analysis = TextBlob(full_text).sentiment.polarity
                
                # معادلة تضخيم النسب (Amplification) لجعلها واقعية
                # إذا كانت Polarity 0.2 تصبح 60% إيجابي مثلاً
                if analysis > 0:
                    pos_p = min(100, (analysis * 100) + 50)
                    neg_p = 0
                elif analysis < 0:
                    neg_p = min(100, (abs(analysis) * 100) + 50)
                    pos_p = 0
                else:
                    pos_p = 0
                    neg_p = 0
                
                neu_p = 100 - max(pos_p, neg_p)

                st.markdown(f"### AI Percentage Report: `{name}`")
                col1, col2, col3 = st.columns(3)
                col1.metric("Positive Content", f"{pos_p:.1f}%")
                col2.metric("Negative Content", f"{neg_p:.1f}%")
                col3.metric("Neutral Content", f"{neu_p:.1f}%")
                
                st.progress(int(max(pos_p, neg_p, neu_p)))
        except Exception as e:
            st.error(f"Error: {e}")
        
