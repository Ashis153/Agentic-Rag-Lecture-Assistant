import os
from groq import Groq
from langchain_community.tools.tavily_search import TavilySearchResults

class ResearchAgent:
    def __init__(self, groq_api_key):
        self.client = Groq(api_key=groq_api_key)
        self.search_tool = TavilySearchResults(k=2)

    def search_web(self, topic):
        try:
            results = self.search_tool.run(f"Simple explanation and formula for {topic}")
            prompt = f"Summarize these web results for a student: {results}. Focus on clarity and include 1 link."
            
            completion = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )
            return completion.choices[0].message.content
        except:
            return "Unable to reach the web right now."