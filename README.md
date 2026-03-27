### 🎓 **Agentic Multi-Modal Lecture Assistant**

Agentic Multi-Modal Lecture Assistant is an intelligent RAG-based learning ecosystem designed to transform passive video watching into an interactive study session. It doesn't just "search" text; it synchronizes visual keyframes with audio transcripts and uses an autonomous multi-agent team to ensure you actually master the material.

![Webpage]("[C:\Users\ashis\Pictures\Screenshots\Screenshot 2026-03-27 184027.png](https://github.com/Ashis153/Agentic-Rag-Lecture-Assistant/blob/main/Screenshot%202026-03-27%20184027.png)")

## 🚀 Key Features

**Multi-Modal Retrieval:**  
The system leverages OpenCV for temporal frame extraction and OpenAI Whisper for high-accuracy transcription, ensuring that both visual and auditory data are synchronized for the LLM.

**Visual-Aware Answers:**  
By linking specific moments in the video (images) to the text transcript, the AI is able to "see" what the professor is writing on the board or displaying on slides while generating responses.

### Agentic Workflow

- **Lecture Agent**  
  Performs high-density semantic search across ChromaDB to retrieve timestamped text and visual keyframes for localized video context.

- **Research Agent**  
  Autonomously orchestrates real-time web searches via Tavily AI to fill knowledge gaps when the lecture material is insufficient.

- **Socratic Tutor**  
  Manages the pedagogical layer by generating Active Recall questions, transforming the AI from a search tool into a learning partner.

**Blazing Fast Inference:**  
The entire reasoning engine is powered by the Groq LPU™ Inference Engine using Llama-3.3-70B, providing near-instant response times for a seamless user experience.

---

## 🏗️ System Architecture

The system follows a modular pipeline to process, index, and reason over video data:

**Ingestion:**  
During the initial phase, the video is split into 5-second visual frames and a full audio transcript is generated using Whisper to create a comprehensive data map.

**Vector Store:**  
Text chunks and their corresponding image metadata are embedded and stored in ChromaDB, allowing for high-dimensional similarity searches.

**Orchestration:**  
LangChain manages the complex logic and tool-calling between the user's query and the various autonomous agentic tools.

| Component | Technology |
| :--- | :--- |
| ***LLM*** | Groq (Llama-3.3-70B-Versatile) |
| ***Framework*** | LangChain / LangGraph |
| ***Vector DB*** | ChromaDB |
| ***Transcription*** | OpenAI Whisper |
| ***Computer Vision*** | OpenCV |
| ***Web Search*** | Tavily AI |
| ***UI*** | Streamlit |
