import streamlit as st
from PIL import Image
import requests
import io
from deep_translator import GoogleTranslator

# 1. إعدادات الصفحة
st.set_page_config(page_title="Jimi AI Art", page_icon="🎨", layout="wide")

# 2. جلب المفتاح
try:
    api_token = st.secrets["HUGGINGFACE_TOKEN"]
except:
    st.error("⚠️ لم يتم العثور على المفتاح! تأكد من إضافته في Secrets.")
    st.stop()

# 3. دالة الاتصال
def query(payload, model_id):
    headers = {"Authorization": f"Bearer {api_token}"}
    api_url = f"https://api-inference.huggingface.co/models/{model_id}"
    response = requests.post(api_url, headers=headers, json=payload)
    return response.content

# 4. التنسيق
st.markdown("""
<style>
    .stButton>button {
        background-color: #FF4B4B; color: white; width: 100%;
        border-radius: 8px; font-weight: bold;
    }
    h1 { color: #333; text-align: center; }
</style>
""", unsafe_allow_html=True)

st.title("🎨 موقع مقتدى للذكاء الاصطناعي")
st.markdown("### 🚀 اكتب بالعربي أو الإنجليزي، ولا يهمك!")

tab1, tab2 = st.tabs(["🖼️ صانع الصور", "✨ دمج الصور"])

# --- قسم 1: توليد الصور ---
with tab1:
    st.write("اكتب وصف الصورة (مثال: أسد يرتدي نظارة شمسية في بغداد)")
    prompt = st.text_area("الوصف:", height=80)
    
    if st.button("✨ اصنع الصورة"):
        if prompt:
            with st.spinner('جاري الترجمة والرسم... 🎨'):
                try:
                    # الترجمة من أي لغة للإنجليزية
                    translator = GoogleTranslator(source='auto', target='en')
                    translated_prompt = translator.translate(prompt)
                    st.caption(f"🤖 (جاري الرسم بناءً على: {translated_prompt})")

                    # الإرسال للذكاء الاصطناعي
                    model_id = "runwayml/stable-diffusion-v1-5"
                    image_bytes = query({"inputs": translated_prompt}, model_id)
                    
                    image = Image.open(io.BytesIO(image_bytes))
                    st.success("تم!")
                    st.image(image, caption="صنع بواسطة موقع مقتدى", use_container_width=True)
                except Exception as e:
                    st.error("الموقع يقوم بتثبيت المترجم... انتظر دقيقة ثم حاول مرة أخرى!")
        else:
            st.warning("اكتب شيئاً أولاً!")

# --- قسم 2: دمج الصور ---
with tab2:
    st.header("دمج صورتين")
    c1, c2 = st.columns(2)
    with c1: img1 = st.file_uploader("صورة 1", type=['png','jpg'], key="a")
    with c2: img2 = st.file_uploader("صورة 2", type=['png','jpg'], key="b")
        
    if img1 and img2:
        if st.button("ادمج الصور 🔗"):
            i1 = Image.open(img1).convert("RGBA")
            i2 = Image.open(img2).convert("RGBA").resize(i1.size)
            final = Image.blend(i1, i2, alpha=0.5)
            st.image(final, caption="النتيجة", use_container_width=True)

# الحقوق
st.markdown("---")
st.markdown("<div style='text-align: center;'>© 2026 جميع الحقوق محفوظة للمطور <b>مقتدى سامي</b></div>", unsafe_allow_html=True)
