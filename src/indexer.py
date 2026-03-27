import os
import json
import chromadb
from chromadb.utils import embedding_functions

def index_lecture_data(lecture_name, api_key=None): 
    transcript_path = os.path.join("data", lecture_name, "transcript.json")
    db_path = "./vector_db"
    
    if not os.path.exists(transcript_path):
        return " Error: Transcript not found."

    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    
    client = chromadb.PersistentClient(path=db_path)
    collection = client.get_or_create_collection(
        name=lecture_name, 
        embedding_function=embedding_fn
    )

    with open(transcript_path, "r") as f:
        segments = json.load(f)

    documents, metadatas, ids = [], [], []

    for i, seg in enumerate(segments):
        documents.append(seg['text'])
        metadatas.append({
            "start": seg['start'],
            "image_path": f"data/{lecture_name}/keyframes/frame_{int(seg['start'])}s.jpg"
        })
        ids.append(f"id_{i}")

    collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
    
    return f" Successfully indexed {len(documents)} segments using local embeddings!"