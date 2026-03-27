import os
from groq import Groq
import chromadb
from chromadb.utils import embedding_functions
from src.research_agent import ResearchAgent

class LectureAgent:
    def __init__(self, lecture_name, groq_api_key):
        self.client = Groq(api_key=groq_api_key)
        self.lecture_name = lecture_name
        self.researcher = ResearchAgent(groq_api_key)
        
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
        db_path = os.path.abspath("./vector_db")
        chroma_client = chromadb.PersistentClient(path=db_path)
        
        try:
            self.collection = chroma_client.get_collection(
                name=lecture_name, 
                embedding_function=self.embedding_fn
            )
        except:
            self.collection = None

    def ask(self, query):
        if not self.collection: return "Index not found.", None, 0

        results = self.collection.query(query_texts=[query], n_results=5)
        context_text = "\n".join(results['documents'][0])
        
        img_path, timestamp = self._get_best_image(results)

        completion = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a Teaching Assistant.Try to be relevant from the lecture uploaded. If the lecture context is missing a specific answer or example, start with '[NEED_RESEARCH]'."},
                {"role": "user", "content": f"Context: {context_text}\n\nQuestion: {query}"}
            ],
            temperature=0.3
        )
        answer = completion.choices[0].message.content

        if "[NEED_RESEARCH]" in answer:
            answer = answer.replace("[NEED_RESEARCH]", "*(Supplementing with Web Data...)*\n\n")
            web_info = self.researcher.search_web(query)
            answer += f"\n\n---\n** Web Insights:**\n{web_info}"

        return answer, img_path, timestamp

    def _get_best_image(self, results):
        for meta in results['metadatas'][0]:
            raw_path = meta.get('image_path', "")
            base_dir = os.path.dirname(raw_path)
            t = int(meta.get('start', 0))
            for offset in range(0, 16): 
                check = os.path.join(base_dir, f"frame_{t - offset}s.jpg")
                if os.path.exists(check): return check, (t - offset)
        return None, 0