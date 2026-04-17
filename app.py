import streamlit as st
from textblob import TextBlob
from PIL import Image, ImageStat

# 1. إعدادات تجعل الواجهة عصرية واحترافية
st.set_page_config(page_title="Tayeb AI Platform", page_icon="🚀", layout="wide")

# 2. تصميم القائمة الجانبية الأنيقة (Sidebar)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=100)
    st.title("Tayeb AI Control")
    st.markdown("---")
    st.info("هذه المنصة مدعومة بالذكاء الاصطناعي لتحليل البيانات.")
    st.write("👤 المطور: **طيب**")

# 3. العنوان الرئيسي
st.title("🤖 منصة التحليل الذكي الشاملة")
st.write("اختر الأداة التي تريد استخدامها من الأعلى:")

# 4. إنشاء التبويبات الجميلة (Tabs) للحفاظ على الترتيب
tab1, tab2, tab3 = st.tabs(["📷 تحليل الصور", "✍️ تحليل النصوص", "📂 معالجة الملفات"])

# --- القسم الأول: الصور ---
with tab1:
    st.subheader("تحليل محتوى الصور")
    uploaded_img = st.file_uploader("ارفع صورة هنا...", type=['jpg', 'jpeg', 'png'])
    if uploaded_img:
        col1, col2 = st.columns(2)
        with col1:
            img = Image.open(uploaded_img)
            st.image(img, caption="الصورة المرفوعة", use_container_width=True)
        with col2:
            if st.button("بدأ تحليل الصورة"):
                with st.spinner('جاري التحليل...'):
                    stat = ImageStat.Stat(img.convert('L'))
                    res = "إيجابية وواضحة 😊" if stat.stddev[0] > 40 else "متعادلة أو غامضة 😐"
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
    
