import streamlit as st
from textblob import TextBlob
from PIL import Image, ImageStat

# 1. Page Config
st.set_page_config(page_title="Tayeb AI Hub", page_icon="🤖", layout="wide")

# 2. Sidebar
with st.sidebar:
    st.title("AI Control Hub")
    st.info("Advanced AI Analysis Platform")
    st.write("👤 Developer: **Tayeb**")

# 3. Main Interface
st.title("🤖 Multi-Functional AI Analyzer")

tab1, tab2, tab3 = st.tabs(["📷 Image", "✍️ Text", "📂 File"])

with tab1:
    st.subheader("Image AI")
    up_img = st.file_uploader("Upload Image", type=['jpg', 'png'])
    if up_img:
        img = Image.open(up_img)
        st.image(img, width=300)
        if st.button("Analyze Image"):
            stat = ImageStat.Stat(img.convert('L'))
            res = "Clear 😊" if stat.stddev[0] > 40 else "Neutral 😐"
            st.success(f"Result: {res}")

with tab2:
    st.subheader("Text AI")
    user_text = st.text_area("Enter English text:")
    if st.button("Analyze Text"):
        if user_text:
            score = TextBlob(user_text).sentiment.polarity
            if score > 0: st.success("Positive 😊")
            elif score < 0: st.error("Negative 😡")
            else: st.warning("Neutral 😐")

with tab3:
    st.subheader("File AI")
    up_file = st.file_uploader("Upload .txt", type=['txt'])
    if up_file:
        if st.button("Read File"):
            content = up_file.read().decode("utf-8")
            st.text_area("Content:", content)
