import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")

def llm_prompt(prompt):
  client = Groq(api_key=groq_key)


  completion = client.chat.completions.create(
    model="gemma2-9b-it",
    messages = [
    {
      "role": "system",
      "content": prompt
    }
    ],
    temperature=0.5,
    max_tokens=5640,
    top_p=1
  )

  print(completion.choices[0].message.content)
