import streamlit as st
import pandas as pd
import PyPDF2
from docx import Document
from PIL import Image, ImageStat
from textblob import TextBlob

# 1. إعداد الصفحة
st.set_page_config(page_title="Tayeb AI Pro", layout="wide")

st.title("🤖 Tayeb Multi-AI Platform")

# 2. التبويبات الثلاثة (كما كانت لضمان التنظيم)
tab1, tab2, tab3 = st.tabs(["📷 Image Tool", "✍️ Text Tool", "📂 Universal File Explorer"])

# --- التبويب الأول: الصور فقط ---
with tab1:
    st.subheader("Image Analysis")
    up_img = st.file_uploader("Upload Image", type=['jpg', 'jpeg', 'png'], key="img_up")
    if up_img:
        img = Image.open(up_img)
        st.image(img, width=300)
        if st.button("Analyze Image Quality"):
            stat = ImageStat.Stat(img.convert('L'))
            res = "Clear 😊" if stat.stddev[0] > 40 else "Low Contrast 😐"
            st.success(f"Result: {res}")

# --- التبويب الثاني: النص المباشر فقط ---
with tab2:
    st.subheader("Direct Text Sentiment")
    user_text = st.text_area("Type or paste your English text here:", height=150)
    if st.button("Analyze Sentiment"):
        if user_text:
            score = TextBlob(user_text).sentiment.polarity
            if score > 0: st.success(f"Positive 😊 ({score:.2f})")
            elif score < 0: st.error(f"Negative 😡 ({score:.2f})")
            else: st.warning("Neutral 😐")

# --- التبويب الثالث: الملفات الشاملة (هنا التغيير الذكي) ---
with tab3:
    st.subheader("Smart File Reader")
    st.write("Upload any file (PDF, Excel, Word, TXT) and I will read it automatically.")
    
    up_any = st.file_uploader("Drop any document here", type=None, key="file_up")
    
    if up_any:
        name = up_any.name
        ext = name.split('.')[-1].lower()
        st.info(f"File Type Detected: {ext.upper()}")

        # قراءة PDF
        if ext == 'pdf':
            pdf = PyPDF2.PdfReader(up_any)
            content = "".join([p.extract_text() for p in pdf.pages])
            st.text_area("PDF Content:", content[:5000], height=300)
        
        # قراءة Excel/CSV
        elif ext in ['xlsx', 'csv', 'xls']:
            df = pd.read_excel(up_any) if 'xls' in ext else pd.read_csv(up_any)
            st.dataframe(df)
            st.success(f"Loaded {len(df)} rows.")

        # قراءة Word
        elif ext == 'docx':
            doc = Document(up_any)
            content = "\n".join([p.text for p in doc.paragraphs])
            st.text_area("Word Content:", content, height=300)

        # قراءة Text
        elif ext == 'txt':
            content = up_any.getvalue().decode("utf-8")
            st.text_area("Text Content:", content, height=300)
        
        else:
            st.warning("Preview not available for this format, but file is uploaded.")
    
