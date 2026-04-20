import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/ask"

#Page config
st.set_page_config(page_title="AI Browser", layout="wide")

#Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}
.stApp {
    background: linear-gradient(135deg, #1f1c2c, #928DAB);
    color: #ffffff;
}
.glass {
    background: rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 25px;
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    margin-bottom: 20px;
    border: 1px solid rgba(255,255,255,0.1);
}
.stTextInput input {
    background: rgba(255,255,255,0.1) !important;
    color: white !important;
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.2);
    font-family: 'Poppins', sans-serif !important;
}
.stButton button {
    background: linear-gradient(45deg, #ff9966, #ff5e62);
    color: white;
    border-radius: 12px;
    border: none;
    padding: 10px 20px;
    font-weight: 600;
    transition: 0.3s;
    font-family: 'Poppins', sans-serif !important;
    width: 100%;
}
.stButton button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 15px rgba(255,94,98,0.6);
}
.source-link {
    display: block;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 10px;
    padding: 10px 16px;
    margin: 6px 0;
    color: #ffd6a5 !important;
    text-decoration: none;
    font-size: 0.88rem;
    transition: all 0.2s;
}
.source-link:hover {
    background: rgba(255,153,102,0.15);
    border-color: #ff9966;
    color: #ffb347 !important;
}
.answer-text {
    color: #f0f0f0;
    font-size: 1rem;
    line-height: 1.8;
}
.latency {
    display: inline-block;
    background: rgba(52,211,153,0.15);
    border: 1px solid rgba(52,211,153,0.3);
    color: #34d399;
    border-radius: 20px;
    padding: 3px 14px;
    font-size: 0.8rem;
    font-weight: 600;
}
.history-item {
    background: rgba(255,255,255,0.04);
    border-left: 3px solid #ff9966;
    border-radius: 0 10px 10px 0;
    padding: 8px 14px;
    margin: 6px 0;
    font-size: 0.85rem;
    color: #cbd5e1;
    cursor: pointer;
}
h1, h2, h3 { color: #ffffff !important; }
a { color: #ffd6a5; }
</style>
""", unsafe_allow_html=True)

#Init session state
if "history" not in st.session_state:
    st.session_state.history = []

#Header
st.markdown(
    "<h1 style='text-align:center;'>🔍 AI Search Engine</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center;color:#cbd5e1;'>Smart answers from the live web</p>",
    unsafe_allow_html=True
)
st.markdown("---")

#Layout
col1, col2 = st.columns([3, 1])

with col2:
    #Sidebar history panel
    st.markdown("### 🕐 Recent Searches")
    if st.session_state.history:
        for item in reversed(st.session_state.history[-5:]):
            st.markdown(
                f'<div class="history-item">🔎 {item["question"][:40]}...</div>',
                unsafe_allow_html=True
            )
        if st.button("🗑️ Clear History"):
            st.session_state.history = []
            st.rerun()
    else:
        st.markdown(
            "<p style='color:#64748b;font-size:0.85rem;'>No searches yet</p>",
            unsafe_allow_html=True
        )

with col1:
    #Search input
    question = st.text_input(
        "Enter your question:",
        placeholder="e.g. What is the Bitcoin price today?",
        label_visibility="collapsed"
    )

    if st.button("🔍 Search"):
        if not question:
            st.warning("Please enter a question.")
        else:
            with st.spinner("Thinking..."):
                try:
                    response = requests.post(
                        API_URL,
                        json={"question": question},
                        timeout=60
                    )

                    if response.status_code == 200:
                        data = response.json()

                        # Save to history
                        st.session_state.history.append({
                            "question": question,
                            "answer": data["answer"],
                            "sources": data["sources"],
                            "latency": data["latency"]
                        })

                        #Answer card
                        st.markdown('<div class="glass">', unsafe_allow_html=True)
                        st.markdown("### 🟠 Answer")
                        st.markdown(
                            f'<div class="answer-text">{data["answer"]}</div>',
                            unsafe_allow_html=True
                        )
                        st.markdown(
                            f'<span class="latency">⚡ {data["latency"]}</span>',
                            unsafe_allow_html=True
                        )
                        st.markdown('</div>', unsafe_allow_html=True)

                        #Sources card
                        if data.get("sources"):
                            st.markdown('<div class="glass">', unsafe_allow_html=True)
                            st.markdown("### 🔗 Sources")
                            for i, src in enumerate(data["sources"], 1):
                                if src:
                                    try:
                                        domain = src.split("/")[2].replace("www.", "")
                                    except Exception:
                                        domain = src
                                    st.markdown(
                                        f'<a class="source-link" href="{src}" target="_blank">'
                                        f'🌐 {i}. {domain}</a>',
                                        unsafe_allow_html=True
                                    )
                            st.markdown('</div>', unsafe_allow_html=True)

                    elif response.status_code == 404:
                        st.error("No results found. Try rephrasing.")
                    elif response.status_code == 429:
                        st.error("AI quota exhausted. Please wait.")
                    else:
                        st.error(f"API Error {response.status_code}")

                except requests.exceptions.ConnectionError:
                    st.error("Cannot connect to API. Make sure FastAPI is running:\n`uvicorn main:app --reload`")
                except Exception as e:
                    st.error(f"Connection failed: {e}")

    #Show previous results
    if st.session_state.history:
        st.markdown("---")
        st.markdown("### 📜 Previous Results")
        for item in reversed(st.session_state.history[:-1]):
            with st.expander(f"🔎 {item['question'][:60]}"):
                st.markdown(
                    f'<div class="answer-text">{item["answer"]}</div>',
                    unsafe_allow_html=True
                )
                st.markdown(
                    f'<span class="latency">⚡ {item["latency"]}</span>',
                    unsafe_allow_html=True
                )
