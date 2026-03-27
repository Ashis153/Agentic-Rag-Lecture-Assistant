from groq import Groq

# Ensure this name matches 'TutorAgent' exactly
class TutorAgent: 
    def __init__(self, groq_api_key):
        self.client = Groq(api_key=groq_api_key)

    def generate_challenge(self, last_answer):
        prompt = f"""
        You are a Socratic Tutor. Based on this explanation: '{last_answer}'
        Generate ONE brief, engaging follow-up question to test the student's understanding.
        Rules: 1 sentence max, do not give the answer, be encouraging.
        """
        
        completion = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return completion.choices[0].message.content