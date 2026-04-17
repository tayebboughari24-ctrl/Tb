import streamlit as st
from textblob import TextBlob
from PIL import Image, ImageStat

# Professional Page Config
st.set_page_config(page_title="Tayeb AI Analyzer", page_icon="🤖", layout="wide")

# Stylish Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=80)
    st.title("AI Control Hub")
    st.markdown("---")
    st.info("This platform uses Advanced AI to analyze your data.")
    st.write("👤 Developer: **Tayeb**")

# Main Title
st.title("🤖 Multi-Functional AI Analyzer")
st.write("Select a tool from the tabs below to start your analysis:")

# Modern Tabs for Organization
tab1, tab2, tab3 = st.tabs(["📷 Image Analysis", "✍️ Text Sentiment", "📂 File Processor"])

# --- TAB 1: Image Analysis ---
with tab1:
    st.subheader("Image Content Analysis")
    uploaded_img = st.file_uploader("Upload Image (JPG/PNG)", type=['jpg', 'jpeg', 'png'])
    if uploaded_img:
        col1, col2 = st.columns(2)
        with col1:
            img = Image.open(uploaded_img)
            st.image(img, caption="Uploaded Preview", use_container_width=True)
        with col2:
            if st.button("Run Image AI"):
                with st.spinner('Processing...'):
                    stat = ImageStat.Stat(img.convert('L'))
                    res = "Clear & Vibrant 😊" if stat.stddev[0] > 40 else "Neutral/Dark 😐"
                    st.success(f"AI Result: {res}")

# --- TAB 2: Text Sentiment ---
with tab2:
    st.subheader("Sentiment Analysis Tool")
    text_input = st.text_area("Enter English text to analyze emotions:")
    if st.button("Analyze Sentiment"):
        if text_input:
            score = TextBlob(text_input).sentiment.polarity
            if score > 0: st.success(f"Positive Sentiment 😊 (Score: {score:.2f})")
            elif score < 0: st.error(f"Negative Sentiment 😡 (Score: {score:.2f})")
            else: st.warning("Neutral Sentiment 😐")

# --- TAB 3: File Processor ---
with tab3:
    st.subheader("Text File Processing")
    uploaded_file = st.file_uploader("Upload a .txt file", type=['txt'])
    if uploaded_file:
        if st.button("Read Content"):
            content = uploaded_file.read().decode("utf-8")
            st.text_area("File Content:", content, height=200)
            st.info("File processed successfully!")
                    st.success(f"النتيجة: {res}")

# --- القسم الثاني: النصوص ---
with tab2:
    st.subheader("تحليل المشاعر والنصوص")
    text_input = st.text_area("اكتب نصاً بالإنجليزية لتحليله:")
    if st.button("تحليل النص"):
        if text_input:
            score = TextBlob(text_input).sentiment.polarity
            if score > 0: st.success(f"نص إيجابي 😊 (الدرجة: {score:.2f})")
            elif score < 0: st.error(f"نص سلبي 😡 (الدرجة: {score:.2f})")
            else: st.warning("نص حيادي 😐")

# --- القسم الثالث: الملفات ---
with tab3:
    st.subheader("معالجة الملفات النصية")
    uploaded_file = st.file_uploader("ارفع ملف .txt", type=['txt'])
    if uploaded_file:
        if st.button("قراءة الملف"):
            content = uploaded_file.read().decode("utf-8")
            st.text_area("محتوى الملف:", content, height=200)
            st.info(f"تمت قراءة الملف بنجاح!")
    
