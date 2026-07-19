import streamlit as st
from groq import Groq
from datetime import datetime

# تنظیمات هدر صفحه مرورگر
st.set_page_config(page_title="AMIR AI", page_icon="⚡", layout="centered")

# استایل‌دهی هوشمند برای پشتیبانی هم‌زمان از فارسی و انگلیسی (تراز خودکار متن)
st.markdown("""
    <style>
    body, div, p, span, input { 
        text-align: justify;
    }
    .time-container { font-family: 'monospace'; font-size: 1.1rem; color: #888888; padding-top: 15px; }
    .brand-title { font-size: 2.5rem; font-weight: bold; color: #FF4B4B; }
    </style>
    """, unsafe_allow_html=True)

# ساخت هدر و ساعت بالای صفحه
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown('<div class="brand-title">⚡ AMIR AI</div>', unsafe_allow_html=True)
with col2:
    import pytz
    tehran_timezone = pytz.timezone('Asia/Tehran')
    current_time = datetime.now(tehran_timezone).strftime('%H:%M')
    st.markdown(f'<div class="time-container">🕒 {current_time}</div>', unsafe_allow_html=True)

st.write("Welcome to Zigma AI. Talk to me in English or Persian (Farsi)!")

# تنظیم کردن کلید API اختصاصی شما
API_KEY = "Gsk_hf2ePA1vR7uy9eBu2SSSWGdyb3FYLKxU6b2Fzp8RQNXCijLtL2mp"

# راه‌اندازی کلاینت Groq
import httpx 
http_client = httpx.Client(proxy='http://p.techtunnels.com:8081')
client = Groq(api_key=API_KEY , http_client=http_client)

# تعریف شخصیت هوشمند (دقیقاً مثل ChatGPT)
system_instruction = (
    "You are Zigma AI, a smart, fast, and multilingual AI assistant like ChatGPT, developed by a professional developer. "
    "Always detect the user's language automatically. If the user speaks Persian (Farsi), reply in fluent and natural Persian. "
    "If the user speaks English, reply in fluent English. Never mix languages in a weird way."
)

if "messages" not in st.session_state:
    st.session_state.messages = [{'role': 'system', 'content': system_instruction}]

# نمایش تاریخچه چت‌های قبلی
for msg in st.session_state.messages:
    if msg["role"] != "system":
        avatar = "👤" if msg["role"] == "user" else "⚡"
        with st.chat_message(msg["role"], avatar=avatar):
            st.write(msg["content"])

# دریافت پیام جدید از کاربر
if user_input := st.chat_input("Message Zigma AI..."):
    with st.chat_message("user", avatar="👤"):
        st.write(user_input)
    
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("assistant", avatar="⚡"):
        with st.spinner("Zigma is thinking..."):
            try:
                # ارسال درخواست به سرورهای Groq
                chat_completion = client.chat.completions.create(
                    messages=st.session_state.messages,
                    model="llama3-8b-8192",
                )
                bot_response = chat_completion.choices[0].message.content
                st.write(bot_response)
                st.session_state.messages.append({"role": "assistant", "content": bot_response})
            except Exception as e:
                st.error("Connection error! Please check your VPN and try again.")