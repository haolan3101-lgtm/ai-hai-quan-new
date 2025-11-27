import streamlit as st
import requests
import json

# --- CẤU HÌNH TRANG WEB ---
st.set_page_config(page_title="AI Giáo trình MH", page_icon="⚓")
st.title("⚓ AI GIÁO TRÌNH MH")
st.markdown("**Bản quyền:** Trung tá QNCN Mai Xuân Hảo")
st.markdown("---")

# --- LẤY API KEY ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    st.error("⚠️ Chưa nhập API Key trong Secrets.")
    st.stop()

# --- HÀM GỬI TIN NHẮN TRỰC TIẾP (KHÔNG DÙNG THƯ VIỆN) ---
def hoi_google_gemini(noi_dung_hoi):
    # Địa chỉ máy chủ Google (Dùng bản 1.5 Flash mới nhất qua đường truyền Web)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    # Đóng gói tin nhắn
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{
            "parts": [{"text": noi_dung_hoi}]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 8192
        }
    }
    
    # Gửi đi
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        return f"Lỗi từ Google: {response.text}"

# --- CẤU HÌNH NHÂN CÁCH AI ---
prompt_huan_luyen = """
Bạn là AI Giáo trình MH, Bản quyền của Trung tá QNCN Mai Xuân Hảo.
Nhiệm vụ: Soạn thảo văn bản, giáo trình, đề tài lĩnh vực Quân sự, Hải quân.
Phong cách: Chính quy, nghiêm túc, dùng từ ngữ quân sự chính xác.
Luôn bắt đầu câu trả lời bằng: "Chào thủ trưởng/đồng chí, AI Giáo trình MH (Bản quyền của Trung tá QNCN Mai Xuân Hảo) sẵn sàng hỗ trợ."
\n\n YÊU CẦU CỦA NGƯỜI DÙNG: 
"""

# --- GIAO DIỆN CHAT ---
if "history" not in st.session_state:
    st.session_state.history = []

# Hiển thị lịch sử
for role, text in st.session_state.history:
    with st.chat_message(role):
        st.markdown(text)

# Xử lý nhập liệu
if prompt := st.chat_input("Nhập yêu cầu tại đây..."):
    # Hiện câu hỏi
    st.session_state.history.append(("user", prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gửi lên Google và chờ trả lời
    with st.chat_message("assistant"):
        with st.spinner("Đang soạn thảo văn bản..."):
            # Ghép prompt huấn luyện vào câu hỏi để AI nhớ vai trò
            cau_hoi_day_du = prompt_huan_luyen + prompt
            
            tra_loi = hoi_google_gemini(cau_hoi_day_du)
            
            st.markdown(tra_loi)
            st.session_state.history.append(("assistant", tra_loi))
