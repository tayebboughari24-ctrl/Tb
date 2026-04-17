import streamlit as st
import pandas as pd
import PyPDF2
from docx import Document
from PIL import Image, ImageStat
from textblob import TextBlob

# 1. Page Configuration
st.set_page_config(page_title="Emotion Analysis", layout="wide", page_icon="📊")

# Header
st.title("📊 Emotion Analysis")
st.markdown("---")

# 2. Tabs
tab1, tab2, tab3 = st.tabs(["📷 Image Vision", "✍️ Text Analysis", "📂 File Analyzer"])

# --- TAB 1: Image (تحليل بسيط بدون نسب) ---
with tab1:
    st.subheader("Visual Tone Detection")
    up_img = st.file_uploader("Upload Image", type=['jpg', 'jpeg', 'png'], key="img_up")
    if up_img:
        img = Image.open(up_img)
        st.image(img, width=300)
        if st.button("Check Image"):
            stat = ImageStat.Stat(img.convert('L'))
            res = "Positive & Bright" if stat.stddev[0] > 40 else "Neutral/Muted"
            st.success(f"Result: {res}")

# --- TAB 2: Text (تحليل بسيط بدون نسب) ---
with tab2:
    st.subheader("Quick Text Check")
    user_text = st.text_area("Enter text:", height=150)
    if st.button("Analyze Sentiment"):
        if user_text:
            score = TextBlob(user_text).sentiment.polarity
            if score > 0: st.success("Outcome: Positive 😊")
            elif score < 0: st.error("Outcome: Negative 😡")
            else: st.warning("Outcome: Neutral 😐")

# --- TAB 3: File Analyzer (التحليل الاحترافي بالنسب المئوية فقط هنا) ---
with tab3:
    st.subheader("Advanced File Emotion Analytics")
    st.write("Upload a document to get a detailed percentage-based report.")
    up_any = st.file_uploader("Upload PDF, Word, or Excel", type=None, key="file_up")
    
    if up_any:
        name = up_any.name
        ext = name.split('.')[-1].lower()
        full_text = ""

        try:
            # Extraction
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
                # الحساب الدقيق للجمل
                blob = TextBlob(full_text)
                sentences = blob.sentences
                avg_pol = sum(s.sentiment.polarity for s in sentences) / len(sentences)
                
                # تحويل النتائج لنسب مئوية (Calculation logic)
                pos_val = max(0, avg_pol * 100) if avg_pol > 0 else 0
                neg_val = abs(min(0, avg_pol * 100)) if avg_pol < 0 else 0
                neu_val = 100 - (pos_val + neg_val)

                st.markdown(f"### AI Percentage Report: `{name}`")
                
                # عرض النسب المئوية بشكل احترافي
                col1, col2, col3 = st.columns(3)
                col1.metric("Positive Content", f"{pos_val:.1f}%")
                col2.metric("Negative Content", f"{neg_val:.1f}%")
                col3.metric("Neutral Content", f"{neu_val:.1f}%")
                
                # Progress bars visual
                st.write("Visual Representation:")
                st.progress(int(pos_val))
                st.caption(f"Current Positive Score: {pos_val:.1f}%")
            else:
                st.error("The file content is empty or unreadable.")
                
        except Exception as e:
            st.error(f"Analysis Error: {e}")
            
