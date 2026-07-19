import streamlit as st
from groq import Groq
from datetime import datetime
import pytz

# ۱. تنظیمات هدر صفحه مرورگر
st.set_page_config(page_title="Amir AI", page_icon="⚡", layout="centered")

# ۲. استایل پیشرفته و فوق‌العاده جذاب برای رابط کاربری (تم دارک مدرن)
st.markdown("""
    <style>
    /* تغییر رنگ پس‌زمینه کل صفحه به دارک ملایم */
    .stApp {
        background-color: #121214;
        color: #E2E8F0;
    }
    
    /* تنظیمات فونت و راست‌چین کردن متون فارسی */
    body, div, p, span, input, textarea {
        text-align: justify;
        direction: rtl;
    }
    
    /* هدر اصلی برنامه */
    .brand-title { 
        font-size: 2.8rem; 
        font-weight: 900; 
        background: linear-gradient(45deg, #FF4B4B, #FF8F00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 1px;
    }
    
    /* کادر نمایش ساعت */
    .time-container { 
        font-family: 'monospace'; 
        font-size: 1.1rem; 
        color: #8A99AD; 
        text-align: left; 
        direction: ltr;
        margin-top: 15px;
    }
    
    /* شخصی‌سازی باکس پیام کاربر */
    .user-bubble {
        background-color: #2D3748;
        padding: 14px 18px;
        border-radius: 18px 18px 4px 18px;
        margin: 10px 0;
        border: 1px solid #4A5568;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        color: #F7FAFC;
    }
    
    /* شخصی‌سازی باکس پیام هوش مصنوعی */
    .bot-bubble {
        background-color: #1A202C;
        padding: 14px 18px;
        border-radius: 18px 18px 18px 4px;
        margin: 10px 0;
        border: 1px solid #2B6CB0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        color: #E2E8F0;
    }
    
    /* استایل دادن به بخش خوش‌آمدگویی */
    .welcome-text {
        color: #718096;
        font-size: 1.1rem;
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# ۳. ساخت هدر و ساعت هماهنگ با زمان ایران
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown('<div class="brand-title">⚡ AMIR AI</div>', unsafe_allow_html=True)
with col2:
    tehran_timezone = pytz.timezone('Asia/Tehran')
    current_time = datetime.now(tehran_timezone).strftime("%H:%M")
    st.markdown(f'<div class="time-container">🕒 {current_time}</div>', unsafe_allow_html=True)

st.markdown('<div class="welcome-text">به چت‌بات اختصاصی امیر خوش آمدید. Talk to me in English or Persian!</div>', unsafe_allow_html=True)

# ۴. تنظیم کردن کلید API (حتماً کلید کامل خودت را بگذار)
API_KEY = "Gsk_hf2..." 

# ۵. راه‌اندازی کلاینت هوش مصنوعی با سرور ضد تحریمِ همیشه پایدار
client = Groq(
    api_key=API_KEY,
    base_url="https://api.groq.com/openapi/v1"
)

# ۶. مدیریت تاریخچه چت در سشن استریم‌لیت
if "messages" not in st.session_state:
    st.session_state.messages = []

# نمایش پیام‌های قبلی با استایل جدید و شیک
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-bubble"><b>👤 شما:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-bubble"><b>⚡ هوش مصنوعی:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)

# ۷. دریافت پیام جدید از کاربر
if user_input := st.chat_input("Message Amir AI..."):
    # نمایش پیام جدید کاربر
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f'<div class="user-bubble"><b>👤 شما:</b><br>{user_input}</div>', unsafe_allow_html=True)
    
    # گرفتن پاسخ از هوش مصنوعی (همان بخشی که در عکس نشان دادی)
    with st.container():
        bot_placeholder = st.empty()
        
        try:
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            )
            output_text = response.choices[0].message.content
            # قرار دادن متن داخل باکس شیک ربات
            bot_placeholder.markdown(f'<div class="bot-bubble"><b>⚡ هوش مصنوعی:</b><br>{output_text}</div>', unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": output_text})
            
        except Exception as e:
            bot_placeholder.error("خطا در اتصال! لطفاً بعداً دوباره تلاش کنید.")