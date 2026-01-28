0import streamlit as st
from PIL import Image
import requests
import io

# إعدادات الصفحة
st.set_page_config(page_title="Jimi AI Art", page_icon="🎨", layout="wide")

# جلب المفتاح من الخزنة
try:
    api_token = st.secrets["HUGGINGFACE_TOKEN"]
except:
    st.error("⚠️ لم يتم العثور على المفتاح! تأكد من إضافته في Secrets.")
    st.stop()

# دالة الاتصال بـ Hugging Face
def query(payload, model_id):
    headers = {"Authorization": f"Bearer {api_token}"}
    api_url = f"https://api-inference.huggingface.co/models/{model_id}"
    response = requests.post(api_url, headers=headers, json=payload)
    return response.content

# تنسيق الواجهة
st.markdown("""
<style>
    .stButton>button {
        background-color: #FF4B4B; 
        color: white; 
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
    }
    h1 { color: #333; text-align: center; }
</style>
""", unsafe_allow_html=True)

st.title("🎨 موقع شركة روني لخدمات الذكاء الأصطناعي")
st.markdown("### 🚀 حوّل خيالك إلى صور حقيقية")

# التبويبات
tab1, tab2 = st.tabs(["🖼️ صانع الصور (AI)", "✨ دمج الصور"])

# --- قسم 1: توليد الصور ---
with tab1:
    st.write("اكتب وصفاً دقيقاً بالإنجليزية للصورة التي تريدها:")
    prompt = st.text_area("مثال: A futuristic lion wearing sunglasses, cyberpunk style", height=80)
    
    if st.button("✨ اصنع الصورة الآن"):
        if prompt:
            with st.spinner('جاري الرسم... يرجى الانتظار لحظات...'):
                try:
                    # استخدام موديل Stable Diffusion القوي
                    model_id = "runwayml/stable-diffusion-v1-5"
                    image_bytes = query({"inputs": prompt}, model_id)
                    
                    # عرض الصورة
                    image = Image.open(io.BytesIO(image_bytes))
                    st.success("تم الإنشاء بنجاح!")
                    st.image(image, caption="تم الإنشاء بواسطة موقع مقتدى", use_container_width=True)
                    st.balloons() # احتفال
                except Exception as e:
                    st.error("حدث خطأ! قد يكون السيرفر مشغولاً، حاول مرة أخرى.")
        else:
            st.warning("الرجاء كتابة وصف للصورة أولاً.")

# --- قسم 2: دمج الصور ---
with tab2:
    st.header("دمج صورتين")
    c1, c2 = st.columns(2)
    with c1:
        img1 = st.file_uploader("الصورة 1", type=['png','jpg'], key="a")
    with c2:
        img2 = st.file_uploader("الصورة 2", type=['png','jpg'], key="b")
        
    if img1 and img2:
        if st.button("ادمج الصور 🔗"):
            i1 = Image.open(img1).convert("RGBA")
            i2 = Image.open(img2).convert("RGBA").resize(i1.size)
            final = Image.blend(i1, i2, alpha=0.5)
            st.image(final, caption="النتيجة", use_container_width=True)
            # --- التذييل (حقوق النشر) ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: grey; padding: 20px;'>
    © 2026 جميع الحقوق محفوظة للمطور <b>مقتدى سامي</b> <br>
    تم التطوير باستخدام تقنيات الذكاء الاصطناعي
</div>
""", unsafe_allow_html=True)
