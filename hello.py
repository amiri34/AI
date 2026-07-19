import streamlit as st
from google import genai
from datetime import datetime
import pytz

# ۱. تنظیمات هدر صفحه مرورگر
st.set_page_config(page_title="Amir AI", page_icon="⚡", layout="centered")

# ۲. استایل دارک مدرن (دقیقاً همان ظاهر شیکی که ساختی)
st.markdown("""
    <style>
    .stApp { background-color: #121214; color: #E2E8F0; }
    body, div, p, span, input, textarea { text-align: justify; direction: rtl; }
    .brand-title { font-size: 2.8rem; font-weight: 900; background: linear-gradient(45deg, #FF4B4B, #FF8F00); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .time-container { font-family: 'monospace'; font-size: 1.1rem; color: #8A99AD; text-align: left; direction: ltr; margin-top: 15px; }
    .user-bubble { background-color: #2D3748; padding: 14px 18px; border-radius: 18px 18px 4px 18px; margin: 10px 0; border: 1px solid #4A5568; color: #F7FAFC; }
    .bot-bubble { background-color: #1A202C; padding: 14px 18px; border-radius: 18px 18px 18px 4px; margin: 10px 0; border: 1px solid #2B6CB0; color: #E2E8F0; }
    .welcome-text { color: #718096; font-size: 1.1rem; margin-bottom: 25px; }
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

st.markdown('<div class="welcome-text">به چت‌بات اختصاصی امیر خوش آمدید. قدرت گرفته از Google Gemini!</div>', unsafe_allow_html=True)

# ۴. تنظیم کردن کلید API گوگل که خودت فرستادی
GEMINI_API_KEY = "AQ.Ab8RN6L_-z6a2hmY14AJea0rpQBYETZK71lo8RokK5dDiKdLNQ" 

# ۵. راه‌اندازی کلاینت رسمی گوگل (بدون نیاز به پروکسی چون روی سرور ابری تحریم نیست)
client = genai.Client(api_key=GEMINI_API_KEY)

# ۶. مدیریت تاریخچه چت
if "messages" not in st.session_state:
    st.session_state.messages = []

# نمایش پیام‌های قبلی
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-bubble"><b>👤 شما:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-bubble"><b>⚡ هوش مصنوعی:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)

# ۷. دریافت پیام جدید
if user_input := st.chat_input("Message Amir AI..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f'<div class="user-bubble"><b>👤 شما:</b><br>{user_input}</div>', unsafe_allow_html=True)
    
    with st.container():
        bot_placeholder = st.empty()
        
        try:
            # ارسال درخواست به مدل جمینای گوگل
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_input,
            )
            output_text = response.text
            
            bot_placeholder.markdown(f'<div class="bot-bubble"><b>⚡ هوش مصنوعی:</b><br>{output_text}</div>', unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": output_text})
            
        except Exception as e:
            bot_placeholder.error(f"خطا در ارتباط با گوگل: {str(e)}")