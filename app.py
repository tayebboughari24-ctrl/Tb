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

# --- TAB 1 & 2 (Simple as requested) ---
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
            elif score < -0.05: st.error("Outcome: Negative 😡")
            else: st.warning("Outcome: Neutral 😐")

# --- TAB 3: File Analyzer (The Accurate Percentage Logic) ---
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
                blob = TextBlob(full_text)
                # طريقة الحساب الجديدة: تعتمد على قوة القطبية (Subjectivity & Polarity)
                pol = blob.sentiment.polarity  # من -1 إلى 1
                subj = blob.sentiment.subjectivity # من 0 إلى 1 (قوة الرأي)

                # معادلة ذكية لتحويل الأرقام الصغيرة إلى نسب مئوية مفهومة
                if pol > 0:
                    pos_p = (pol * 100) + (subj * 20) # نرفع النسبة بناءً على قوة الكلمات
                    neg_p = 0
                elif pol < 0:
                    neg_p = (abs(pol) * 100) + (subj * 20)
                    pos_p = 0
                else:
                    pos_p = 0
                    neg_p = 0
                
                # التأكد أن المجموع لا يتعدى 100
                pos_p = min(pos_p, 100)
                neg_p = min(neg_p, 100)
                neu_p = 100 - max(pos_p, neg_p)

                st.markdown(f"### AI Percentage Report: `{name}`")
                c1, c2, c3 = st.columns(3)
                c1.metric("Positive", f"{pos_p:.1f}%")
                c2.metric("Negative", f"{neg_p:.1f}%")
                c3.metric("Neutral", f"{neu_p:.1f}%")
                
                # شريط تقدم مرئي
                if pos_p > neg_p:
                    st.progress(int(pos_p))
                    st.write(f"Confidence in Positive Sentiment: {pos_p:.1f}%")
                elif neg_p > pos_p:
                    st.progress(int(neg_p))
                    st.write(f"Confidence in Negative Sentiment: {neg_p:.1f}%")
                else:
                    st.progress(int(neu_p))
                    st.write("Confidence: Neutral Content")

        except Exception as e:
            st.error(f"Error: {e}")
                    
