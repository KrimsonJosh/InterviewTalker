from openai import OpenAI
from src.core.config import get_settings

settings = get_settings()

class AIService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def build_prompt(self, resume: str, question: str) -> str:
        """
        Generate a custom prompt for the OpenAI API using the candidate's resume
        and the interview question in a STAR format.
        """
        return f"""
            You are an interview assistant helping candidates answer behavioral questions using their resume.

            Resume:
            {resume}

            Behavioral Interview Question:
            "{question}"

            Respond using the STAR format:
            - Situation
            - Task
            - Action
            - Result

            Be concise but thoughtful. Keep it professional and realistic.
        """

    async def generate_response(self, resume: str, question: str) -> str:
        """
        Generate an AI response using OpenAI's API.
        """
        try:
            prompt = self.build_prompt(resume, question)
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error generating AI response: {str(e)}") 