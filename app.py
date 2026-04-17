import streamlit as st
import pandas as pd
import PyPDF2
from docx import Document
from PIL import Image, ImageStat
from textblob import TextBlob

# 1. Page Configuration
st.set_page_config(page_title="Emotion Analysis", layout="wide", page_icon="📊")

# Custom Title
st.title("📊 Emotion Analysis")
st.markdown("---")

# 2. Tabs for Organization
tab1, tab2, tab3 = st.tabs(["📷 Image Vision", "✍️ Text Analysis", "📂 File Analyzer"])

# --- TAB 1: Image Analysis ---
with tab1:
    st.subheader("Visual Tone Detection")
    up_img = st.file_uploader("Upload Image", type=['jpg', 'jpeg', 'png'], key="img_up")
    if up_img:
        img = Image.open(up_img)
        st.image(img, width=300)
        if st.button("Run Visual AI"):
            stat = ImageStat.Stat(img.convert('L'))
            res = "Vibrant & Positive" if stat.stddev[0] > 40 else "Neutral/Muted"
            st.info(f"Visual Tone Result: {res}")

# --- TAB 2: Text Analysis ---
with tab2:
    st.subheader("Manual Text Analysis")
    user_text = st.text_area("Paste text here for percentage calculation:", height=150)
    if st.button("Calculate Emotions"):
        if user_text:
            blob = TextBlob(user_text)
            polarity = blob.sentiment.polarity
            
            # Logic for percentages
            pos = max(0, polarity * 100) if polarity > 0 else 0
            neg = abs(min(0, polarity * 100)) if polarity < 0 else 0
            neu = 100 - (pos + neg)

            st.write("### Text Emotion Report")
            col1, col2, col3 = st.columns(3)
            col1.metric("Positive", f"{pos:.1f}%")
            col2.metric("Negative", f"{neg:.1f}%")
            col3.metric("Neutral", f"{neu:.1f}%")

# --- TAB 3: Universal File Analyzer (The Calculation Part) ---
with tab3:
    st.subheader("Full Document Emotion Calculation")
    st.write("Upload any file to calculate the total emotion percentage.")
    up_any = st.file_uploader("Upload PDF, Word, or Excel", type=None, key="file_up")
    
    if up_any:
        name = up_any.name
        ext = name.split('.')[-1].lower()
        full_content = ""

        try:
            # Automatic extraction based on format
            if ext == 'pdf':
                pdf = PyPDF2.PdfReader(up_any)
                full_content = "".join([p.extract_text() for p in pdf.pages])
            elif ext == 'docx':
                doc = Document(up_any)
                full_content = "\n".join([p.text for p in doc.paragraphs])
            elif ext == 'txt':
                full_content = up_any.getvalue().decode("utf-8")
            elif ext in ['xlsx', 'csv']:
                df = pd.read_excel(up_any) if 'xls' in ext else pd.read_csv(up_any)
                st.dataframe(df.head(5)) # Show small preview
                full_content = " ".join(df.astype(str).values.flatten())

            if full_content:
                # Perform AI Calculation
                analysis_blob = TextBlob(full_content)
                score = analysis_blob.sentiment.polarity
                
                # Math for percentages
                file_pos = max(0, score * 100) if score > 0 else 0
                file_neg = abs(min(0, score * 100)) if score < 0 else 0
                file_neu = 100 - (file_pos + file_neg)

                st.markdown("---")
                st.write(f"### Final Report for: `{name}`")
                
                # Visual Layout for Percentages
                fcol1, fcol2, fcol3 = st.columns(3)
                fcol1.metric("Positive Content", f"{file_pos:.1f}%")
                fcol2.metric("Negative Content", f"{file_neg:.1f}%")
                fcol3.metric("Neutral Content", f"{file_neu:.1f}%")
                
                # Summary Message
                if score > 0.1:
                    st.success("Analysis Complete: The document has a overall Positive tone.")
                elif score < -0.1:
                    st.error("Analysis Complete: The document has a overall Negative tone.")
                else:
                    st.warning("Analysis Complete: The document tone is Neutral.")
                    
        except Exception as e:
            st.error(f"Error analyzing file: {e}")
            
