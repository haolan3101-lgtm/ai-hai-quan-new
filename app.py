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

# --- HÀM GỬI TIN NHẮN (DÙNG MODEL GEMINI-PRO) ---
def hoi_google_gemini(noi_dung_hoi):
    # Đổi sang model gemini-pro (Dòng model quốc dân, không bao giờ lỗi 404)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    
    # Cấu trúc gói tin cho Gemini Pro (Đơn giản hơn Flash)
    data = {
        "contents": [{
            "parts": [{"text": noi_dung_hoi}]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 8000
        }
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Lỗi từ Google: {response.text}"
    except Exception as e:
        return f"Lỗi đường truyền: {str(e)}"

# --- CẤU HÌNH NHÂN CÁCH AI (KỸ THUẬT GỘP LỆNH) ---
# Vì Gemini Pro không có mục System Instruction riêng, ta gộp thẳng vào câu hỏi
prompt_cot_loi = """
BẠN LÀ: AI Giáo trình MH, Bản quyền của Trung tá QNCN Mai Xuân Hảo.
NHIỆM VỤ: Soạn thảo văn bản, giáo trình, đề tài lĩnh vực Quân sự, Hải quân.
PHONG CÁCH: Chính quy, nghiêm túc, dùng từ ngữ quân sự chính xác.
QUY TẮC: Luôn bắt đầu câu trả lời bằng: "Chào thủ trưởng/đồng chí, AI Giáo trình MH (Bản quyền của Trung tá QNCN Mai Xuân Hảo) sẵn sàng hỗ trợ."
--------------------------------------------------
YÊU CẦU CỦA NGƯỜI DÙNG: 
"""

# --- GIAO DIỆN CHAT ---
if "history" not in st.session_state:
    st.session_state.history = []

# Hiển thị lịch sử
for role, text in st.session_state.history:
    # Chỉ hiển thị nội dung chat, bỏ qua phần prompt cốt lõi để nhìn cho đẹp
    display_text = text
    with st.chat_message(role):
        st.markdown(display_text)

# Xử lý nhập liệu
if prompt := st.chat_input("Nhập yêu cầu tại đây..."):
    # 1. Hiện câu hỏi người dùng
    st.session_state.history.append(("user", prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Gửi lên Google
    with st.chat_message("assistant"):
        with st.spinner("Đang soạn thảo văn bản..."):
            # Gộp nhân cách vào câu hỏi để gửi đi
            cau_hoi_day_du = prompt_cot_loi + prompt
            
            tra_loi = hoi_google_gemini(cau_hoi_day_du)
            
            st.markdown(tra_loi)
            # Lưu lại lịch sử
            st.session_state.history.append(("assistant", tra_loi))
