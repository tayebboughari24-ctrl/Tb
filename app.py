import streamlit as st
import pandas as pd
import PyPDF2
from docx import Document
from PIL import Image, ImageStat
from textblob import TextBlob

# 1. Page Configuration
st.set_page_config(page_title="Emotion Analysis", layout="wide", page_icon="📊")

st.title("📊 Emotion Analysis")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📷 Image Vision", "✍️ Text Analysis", "📂 File Analyzer"])

# --- TAB 1 & 2 (Simple Results) ---
with tab1:
    up_img = st.file_uploader("Upload Image", type=['jpg', 'jpeg', 'png'], key="img_up")
    if up_img:
        img = Image.open(up_img)
        st.image(img, width=300)
        stat = ImageStat.Stat(img.convert('L'))
        res = "Positive & Bright" if stat.stddev[0] > 40 else "Neutral/Muted"
        st.success(f"Result: {res}")

with tab2:
    user_text = st.text_area("Enter text:", height=150)
    if st.button("Analyze Sentiment"):
        if user_text:
            score = TextBlob(user_text).sentiment.polarity
            if score > 0: st.success("Outcome: Positive 😊")
            elif score < 0: st.error("Outcome: Negative 😡")
            else: st.warning("Outcome: Neutral 😐")

# --- TAB 3: File Analyzer (New Accurate Percentage Logic) ---
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
                
                # منطق الحساب الجديد (Strict Percentage Mapping)
                # إذا كانت النتيجة 0.5 (إيجابي) ستتحول إلى 100% إيجابي في عرض النسبة
                if analysis > 0:
                    pos_p = analysis * 100
                    neg_p = 0
                    neu_p = 100 - pos_p
                elif analysis < 0:
                    neg_p = abs(analysis) * 100
                    pos_p = 0
                    neu_p = 100 - neg_p
                else:
                    pos_p = 0
                    neg_p = 0
                    neu_p = 100

                st.markdown(f"### AI Percentage Report: `{name}`")
                
                # عرض الأرقام بشكل كبير
                col1, col2, col3 = st.columns(3)
                col1.metric("Positive Content", f"{pos_p:.1f}%")
                col2.metric("Negative Content", f"{neg_p:.1f}%")
                col3.metric("Neutral Content", f"{neu_p:.1f}%")
                
                # شريط تقدم بناءً على النتيجة الغالبة
                if analysis > 0:
                    st.write("Overall Progress (Positive Trend):")
                    st.progress(int(pos_p))
                elif analysis < 0:
                    st.write("Overall Progress (Negative Trend):")
                    st.progress(int(neg_p))
                else:
                    st.write("Overall Progress (Neutral):")
                    st.progress(100)

        except Exception as e:
            st.error(f"Error: {e}")
            
