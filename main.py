import streamlit as st
import os
import sys
from dotenv import load_dotenv

# 1. Setup
load_dotenv()
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# --- Initialize Session State (MUST BE FIRST) ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "lecture_name" not in st.session_state:
    st.session_state.lecture_name = None

from src.ingest import process_lecture
from src.indexer import index_lecture_data
from src.Lecture_agent import LectureAgent  
from src.research_agent import ResearchAgent
from src.tutor_agent import TutorAgent

# --- Page Config ---
st.set_page_config(page_title="AI Lecture Strategist", layout="wide")

# --- Sidebar: Simple & Organized ---
with st.sidebar:
    st.title("🎓 Lecture Setup")
    uploaded_file = st.file_uploader("Upload MP4 Lecture", type=['mp4'])
    
    if uploaded_file:
        video_path = os.path.join("temp_uploads", uploaded_file.name)
        os.makedirs("temp_uploads", exist_ok=True)
        with open(video_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Side-by-side buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("1. Process"):
                with st.spinner("Analyzing..."):
                    _, name = process_lecture(video_path)
                    st.session_state.lecture_name = name
                    st.success("Done!")
        with col2:
            # Added .get() check for safety
            if st.session_state.get("lecture_name") and st.button("2. Index"):
                with st.spinner("Indexing..."):
                    index_lecture_data(st.session_state.lecture_name)
                    st.balloons()

    if st.session_state.get("lecture_name"):
        st.divider()
        st.caption(f"Active: {st.session_state.lecture_name}")
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()

# --- Main Interface ---
st.title("🤖 Intelligent Study Assistant")

if not st.session_state.get("lecture_name"):
    st.info("Please upload and process a video in the sidebar to begin.")
else:
    # Display Chat History
    for msg in st.session_state.get("messages", []):
        with st.chat_message(msg["role"]):
            if msg["role"] == "assistant" and msg.get("image"):
                img_col, txt_col = st.columns([1, 2])
                with img_col: st.image(msg["image"])
                with txt_col: st.markdown(msg["content"])
            else:
                st.markdown(msg["content"])
            
            if msg.get("challenge"):
                st.info(f"💡 **Tutor Challenge:** {msg['challenge']}")

    # --- Chat Input & Logic ---
    if prompt := st.chat_input("Ask a question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.status("Agents are collaborating...", expanded=False) as status:
                st.write("Searching lecture transcripts...")
                agent = LectureAgent(st.session_state.lecture_name, os.getenv("GROQ_API_KEY"))
                answer, img_path, time_val = agent.ask(prompt)
                
                st.write("Generating follow-up challenge...")
                tutor = TutorAgent(os.getenv("GROQ_API_KEY"))
                challenge_q = tutor.generate_challenge(answer)
                status.update(label="Response Ready!", state="complete")

            if img_path and os.path.exists(img_path):
                c1, c2 = st.columns([1, 2])
                with c1: st.image(img_path, caption=f"At {int(time_val)}s")
                with c2: st.markdown(answer)
            else:
                st.markdown(answer)
            
            st.info(f"💡 **Tutor Challenge:** {challenge_q}")

            st.session_state.messages.append({
                "role": "assistant", 
                "content": answer, 
                "image": img_path if img_path and os.path.exists(img_path) else None,
                "challenge": challenge_q 
            })