import streamlit as st
import google.generativeai as genai
import os

# --- CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="AI Giáo trình MH", page_icon="⚓")
st.title("⚓ AI GIÁO TRÌNH MH")
st.markdown("**Bản quyền:** Trung tá QNCN Mai Xuân Hảo")
st.markdown("---")

# --- KẾT NỐI API ---
# Lấy key an toàn
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.warning("⚠️ Đang chờ nhập API Key trong phần Secrets...")
    st.stop()

# --- CẤU HÌNH AI (Dùng bản 1.5 Flash mới nhất) ---
generation_config = {
  "temperature": 0.7,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
}

# Tắt bộ lọc an toàn để viết nội dung quân sự không bị chặn
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

# Khởi tạo Model
try:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        safety_settings=safety_settings
    )
except Exception as e:
    st.error(f"Lỗi khởi tạo Model: {e}")
    st.stop()

# --- HUẤN LUYỆN AI (Prompt ẩn) ---
promt_huan_luyen = """
Bạn là AI Giáo trình MH, Bản quyền của Trung tá QNCN Mai Xuân Hảo.
Nhiệm vụ: Soạn thảo văn bản, giáo trình, đề tài lĩnh vực Quân sự, Hải quân.
Phong cách: Chính quy, nghiêm túc, chuẩn mực.
Luôn bắt đầu bằng: "Chào thủ trưởng/đồng chí, AI Giáo trình MH (Bản quyền của Trung tá QNCN Mai Xuân Hảo) sẵn sàng hỗ trợ."
"""

# --- XỬ LÝ CHAT ---
if "history" not in st.session_state:
    st.session_state.history = []

# Hiển thị lịch sử
for role, text in st.session_state.history:
    if role == "user":
        with st.chat_message("user"):
            st.markdown(text)
    else:
        with st.chat_message("assistant"):
            st.markdown(text)

# Nhập liệu
if prompt := st.chat_input("Nhập yêu cầu tại đây..."):
    # Hiện câu hỏi người dùng
    st.session_state.history.append(("user", prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI trả lời
    with st.chat_message("assistant"):
        with st.spinner("Đang soạn thảo..."):
            try:
                # Gửi kèm prompt huấn luyện mỗi lần chat để AI không quên vai
                full_prompt = promt_huan_luyen + "\n\n" + "Yêu cầu của người dùng: " + prompt
                
                response = model.generate_content(full_prompt)
                st.markdown(response.text)
                st.session_state.history.append(("model", response.text))
            except Exception as e:
                st.error(f"Lỗi kết nối: {e}")
