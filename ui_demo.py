import time
import base64
import streamlit as st

# =========================
# Page config
# =========================
st.set_page_config(
    page_title="Capstone AI Demo",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================
# Styles
# =========================
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root{
  --bgBase:#f7f8ff;
  --bgSoft:#eef2ff;
  --text:#0f172a;
  --muted:rgba(15,23,42,.62);
  --stroke:rgba(15,23,42,.10);
  --strokeSoft:rgba(15,23,42,.08);
  --surface:rgba(255,255,255,.62);
  --shadow:0 10px 26px rgba(15,23,42,.08);
  --blur:16px;
}

html, body, [class*="css"]{
  font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
  color: var(--text);
}

header{ background: transparent !important; }
#MainMenu, footer{ visibility: hidden; }

.stApp{
  background:
    /* top-center white */
    radial-gradient(
      1200px 1000px at 50% 10%,
      rgba(255,255,255,0.92) 0%,
      rgba(255,255,255,0.80) 30%,
      transparent 80%
    ),

    /* top-left yellow */
    radial-gradient(
      980px 920px at 10% 16%,
      rgba(255, 214, 90, 0.72) 0%,
      rgba(255, 214, 90, 0.35) 40%,
      transparent 70%
    ),

    /* top-right pink */
    radial-gradient(
      900px 850px at 92% 18%,
      rgba(255, 140, 220, 0.62) 0%,
      rgba(255, 140, 220, 0.22) 42%,
      transparent 70%
    ),

    /* bottom blue */
    radial-gradient(
    1500px 1050px at 50% 92%,
    rgba(155, 180, 220, 0.9) 0%,
    rgba(155, 180, 220, 0.35) 46%,
    transparent 82%
),
  linear-gradient(180deg, #ffffff 0%, #f6fbff 100%) !important;

  background-attachment: fixed;
}
  
.block-container{
  max-width: 1080px;
  padding-top: 34px !important;
  padding-bottom: 120px !important;
}

h1{
  position: relative;
  left: 360px;
  font-size: 36px !important;
  font-family: Inter, system-ui, sans-serif !important;
  font-weight: 800 !important;
  letter-spacing: 0.01em !important;
  margin-bottom: 6px !important;
  margin-top: 0 !important;
}

div[data-testid="stCaptionContainer"] p{
  text-align:center;
  color: var(--muted);
  margin-top: 0;
}

/* Sidebar */
section[data-testid="stSidebar"]{
  width: 260px !important;
  min-width: 260px !important;
  background: var(--surface) !important;
  border-right: 1px solid var(--strokeSoft) !important;
  backdrop-filter: blur(var(--blur));
  -webkit-backdrop-filter: blur(var(--blur));
}
section[data-testid="stSidebar"] hr{
  border: none !important;
  height: 1px !important;
  background: var(--strokeSoft) !important;
  margin: 14px 0 !important;
}
section[data-testid="stSidebar"] *:focus,
section[data-testid="stSidebar"] *:focus-visible{
  outline: none !important;
  box-shadow: none !important;
}
section[data-testid="stSidebar"] div[role="combobox"]{
  border: 1px solid var(--stroke) !important;
  border-radius: 14px !important;
  box-shadow: none !important;
}

/* Toggle */
section[data-testid="stSidebar"] div[role="switch"]{
  background: rgba(15,23,42,.14) !important;
  border: 1px solid rgba(15,23,42,.12) !important;
}
section[data-testid="stSidebar"] div[role="switch"][aria-checked="true"]{
  background: #0f172a !important;
  border-color: #0f172a !important;
}
section[data-testid="stSidebar"] div[role="switch"]::after{
  background: rgba(255,255,255,.95) !important;
}

.sidebar-footer{
  position: fixed;
  bottom: 18px;
  left: 18px;
  font-size: 12px;
  color: rgba(15,23,42,0.45);
}

/* Chat */
.stChatMessage{
  background: transparent !important;
  border: 0 !important;
  box-shadow: none !important;
  padding: 0 !important;
  margin-bottom: 14px !important;
}

.stChatMessage [data-testid="stChatMessageContent"]{
  padding: 14px 16px !important;
  border-radius: 18px !important;
  border: 1px solid var(--strokeSoft) !important;
  box-shadow: var(--shadow) !important;
  backdrop-filter: blur(var(--blur));
  -webkit-backdrop-filter: blur(var(--blur));
  font-size: 14px;
  line-height: 1.6;
  background: rgba(255,255,255,.82) !important;
  max-width: 940px !important;
}

.stChatMessage[aria-label="Chat message from user"] [data-testid="stChatMessageContent"]{
  background: rgba(15,23,42,.04) !important;
  border-color: var(--stroke) !important;
}

/* Avatar */
div[data-testid="stChatMessageAvatar"]{
  transform: scale(2.1) !important;
  transform-origin: center;
  margin-top: 8px !important;
}
div[data-testid="stChatMessageAvatar"],
div[data-testid="stChatMessageAvatar"] *{
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
}
div[data-testid="stChatMessageAvatar"] span{
  font-size: 24px !important;
  line-height: 1 !important;
}

/* Remove Streamlit bottom thin bar / wrappers */
div[data-testid="stBottomBlockContainer"],
div[data-testid="stBottomBlockContainer"] > div,
div[data-testid="stBottomBlockContainer"] form,
div[data-testid="stBottom"],
div[data-testid="stBottom"] > div,
div[data-testid="stChatInput"],
div[data-testid="stChatInput"] > div{
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
  outline: none !important;
  min-height: 0 !important;
}
div[data-testid="stBottomBlockContainer"]::before,
div[data-testid="stBottomBlockContainer"]::after,
div[data-testid="stBottom"]::before,
div[data-testid="stBottom"]::after,
div[data-testid="stChatInput"]::before,
div[data-testid="stChatInput"]::after{
  content: none !important;
  display: none !important;
}

/* Chat input: capsule */
.stChatInputContainer{
  background: transparent !important;
  padding-bottom: 22px !important;
}

.stChatInput{
  border-radius: 999px !important;
  background: rgba(255,255,255,.78) !important;
  border: 1px solid rgba(15,23,42,.12) !important;
  box-shadow: 0 12px 28px rgba(15,23,42,.10) !important;
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  min-height: 54px !important;
  padding: 0 10px !important;
}

/* Focus state identical */
.stChatInput:focus-within{
  background: rgba(255,255,255,.78) !important;
  border: 1px solid rgba(15,23,42,.12) !important;
  box-shadow: 0 12px 28px rgba(15,23,42,.10) !important;
}

.stChatInput textarea{
  background: transparent !important;
  border: 0 !important;
  outline: none !important;
  box-shadow: none !important;
  color: var(--text) !important;
  padding-left: 18px !important;
  padding-right: 10px !important;
  padding-top: 16px !important;
  padding-bottom: 16px !important;
  height: 54px !important;
  line-height: 1.2 !important;
  resize: none !important;
  overflow: hidden !important;
}
.stChatInput textarea::placeholder{
  color: rgba(15,23,42,.45) !important;
}

/* send button */
.stChatInput button{
  position: relative;
  width: 40px !important;
  height: 40px !important;
  border-radius: 999px !important;
  background: #111827 !important;
  border: none !important;
  box-shadow: 0 8px 20px rgba(17,24,39,.25) !important;
  margin-right: 6px !important;
}
.stChatInput button svg{ opacity: 0 !important; }
.stChatInput button::before{
  content: "↑";
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
  color: #fff;
  font-size: 18px;
  font-weight: 600;
}
.stChatInput button:hover{
  background: #0f172a !important;
  transform: translateY(-1px);
}

/* Pills */
div[data-testid="stPills"] > div{
  justify-content: center !important;
  gap: 10px !important;
  margin-top: 8px !important;
  margin-bottom: 6px !important;
}
div[data-testid="stPills"] button{
  border: 1px solid rgba(15,23,42,0.10) !important;
  background: rgba(255,255,255,0.72) !important;
  border-radius: 999px !important;
  padding: 9px 14px !important;
  box-shadow: 0 8px 18px rgba(15,23,42,0.08) !important;
  color: rgba(15,23,42,0.85) !important;
  font-size: 13px !important;
}
/* Keep pressed state subtle */
div[data-testid="stPills"] button[aria-pressed="true"]{
  background: rgba(255,255,255,0.72) !important;
  border-color: rgba(15,23,42,0.10) !important;
  box-shadow: 0 8px 18px rgba(15,23,42,0.08) !important;
}

/* Pills interactions */

/* Smooth transitions */
div[data-testid="stPills"] button{
  transition:
    transform 0.18s ease,
    box-shadow 0.18s ease,
    background-color 0.18s ease,
    border-color 0.18s ease !important;
  will-change: transform;
}

/* Hover */
div[data-testid="stPills"] button:hover{
  transform: translateY(-1.5px) !important;
  box-shadow: 0 10px 22px rgba(15,23,42,0.12) !important;
  background: rgba(255,255,255,0.88) !important;
  border-color: rgba(15,23,42,0.14) !important;
}

/* Active (mouse down): press back */
div[data-testid="stPills"] button:active{
  transform: translateY(0) !important;
  box-shadow: 0 6px 14px rgba(15,23,42,0.10) !important;
}

/* Selected */
div[data-testid="stPills"] button[aria-pressed="true"]{
  background: rgba(255,255,255,0.92) !important;
  border-color: rgba(15,23,42,0.18) !important;
  box-shadow: 0 10px 22px rgba(15,23,42,0.10) !important;
}

/* Chat role styling */

div[data-testid="stChatMessageContent"]{
  background: transparent !important;
}

/* Assistant */
div[data-testid="stChatMessageContent"][aria-label="Chat message from assistant"]{
  background: rgba(255,255,255,0.86) !important;
  border: 1px solid rgba(15,23,42,0.10) !important;
}

/* User */
div[data-testid="stChatMessageContent"][aria-label="Chat message from user"]{
  background: rgba(15,23,42,0.035) !important;
  border: 1px solid rgba(15,23,42,0.08) !important;
}

/* User align right */
div[data-testid="stChatMessage"]
  > div[data-testid="stChatMessageContent"][aria-label="Chat message from user"]{
  margin-left: auto !important;
}

</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# =========================
# Header icon
# =========================
def img_to_data_uri(path: str) -> str:
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/png;base64,{b64}"

icon_uri = img_to_data_uri("assets/logo.png")

st.markdown(
    f"""
    <div style="display:flex; justify-content:center; margin-bottom: -15px;">
        <img src="{icon_uri}" style="width:128px; 
                                     height:128px;
                                     transform: translateY(2px);
                                     filter: drop-shadow(0 14px 28px rgba(15,23,42,0.12));
        " />
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# Demo backend
# =========================
def mock_agent_response(user_input: str) -> dict:
    time.sleep(1.0)
    t = user_input.lower()

    if "order" in t:
        return {
            "answer": "I found your order #1001. It was shipped yesterday and is currently in transit.",
            "tool_used": "SQL Database (Order Tool)",
            "log": "SELECT status, delivery_date FROM orders WHERE user_id='User_A' AND order_id='1001';",
        }

    if "return" in t:
        return {
            "answer": "You can return items within 30 days of receipt. Want me to generate a return label?",
            "tool_used": "Policy RAG (Vector Search)",
            "log": "Retrieve: return_policy_2024.pdf (similarity=0.89)",
        }

    if any(k in t for k in ["jacket", "clothes", "buy"]):
        return {
            "answer": "I found a Vintage Denim Jacket in Blue ($85). Want more details or similar options?",
            "tool_used": "Product Search (RAG)",
            "log": "Vector search: 'blue jacket' -> top matches from vector DB",
        }

    return {
        "answer": "I can help you track orders, find products, or check policies. What can I do for you?",
        "tool_used": "General Chat",
        "log": "Fallback response",
    }

def run_turn(text: str):
    st.session_state.messages.append({"role": "user", "content": text})
    response = mock_agent_response(text)  # replace with real agent/model later
    st.session_state.messages.append({"role": "assistant", "content": response["answer"]})
    st.session_state.last_debug = response

# =========================
# State init
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm your AI shopping assistant. How can I help today?"}
    ]
if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None
if "last_debug" not in st.session_state:
    st.session_state.last_debug = None

# =========================
# Sidebar
# =========================
with st.sidebar:
    st.subheader("Controls")
    user = st.selectbox("Simulate User", ["User A", "User B", "Admin"])
    show_debug = st.toggle("Show Agent Logic / SQL", value=True)
    st.divider()
    st.caption(f"Logged in as {user}")
    st.markdown("<div class='sidebar-footer'>Capstone Project v1.0</div>", unsafe_allow_html=True)

# =========================
# Main
# =========================
st.title("TrendMate")
st.caption("Powered by Gemini & Streamlit")

AVATARS = {"assistant": "assets/avatar1.jpeg", "user": "assets/avatar.jpeg"}

# Render chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"], avatar=AVATARS.get(msg["role"])).write(msg["content"])

# ===============================
# Suggestions bars
# ===============================
if "pills_rev" not in st.session_state:
    st.session_state.pills_rev = 0

mapping = {
    "Order status": "Where is my order?",
    "Shipping policy": "What is your shipping policy and delivery time?",
    "Size guide": "Do you have a size guide?",
}

choice = st.pills(
    label="Suggestions",
    options=list(mapping.keys()),
    selection_mode="single",
    label_visibility="collapsed",
    key=f"suggest_pill_{st.session_state.pills_rev}",
)

if choice:
    run_turn(mapping[choice])
    st.session_state.pills_rev += 1
    st.rerun()

# ===============================
# Chat input
# ===============================
if prompt := st.chat_input("Type your message... Try 'recommend a jacket'"):
    run_turn(prompt)
    st.rerun()