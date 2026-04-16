import streamlit as st
from textblob import TextBlob

# 1. إعداد شكل الصفحة (مثل المواقع الاحترافية)
st.set_page_config(page_title="Tayeb AI Analyzer", layout="wide")

# 2. تصميم القائمة الجانبية (Sidebar)
with st.sidebar:
    st.title("⚙️ Control Panel")
    st.write("Welcome to your AI App")
    st.markdown("---")
    st.info("Created by: Tayeb")

# 3. محتوى الصفحة الرئيسي
st.title("📊 Intelligent Sentiment Analysis")
st.write("Enter any English text below to analyze its emotion.")

# 4. صندوق الكتابة
user_input = st.text_area("Your Text:", placeholder="Type something like: I love this project!")

# 5. زر التحليل والنتائج
if st.button("Analyze Now"):
    if user_input:
        score = TextBlob(user_input).sentiment.polarity
        if score > 0:
            st.balloons() # حركة احتفالية
            st.success(f"Positive Sentiment! 😊 (Score: {score})")
        elif score < 0:
            st.error(f"Negative Sentiment! 😡 (Score: {score})")
        else:
            st.warning("Neutral Sentiment! 😐")
    else:
        st.error("Please enter some text first!")
          
