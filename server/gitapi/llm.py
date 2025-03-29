import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")

if not groq_key:
    raise ValueError("GROQ_API_KEY is missing. Please check your .env file.")

def llm_prompt(files):
    client = Groq(api_key=groq_key)

    file_content_summary = "\n\n".join([f"File: {file['path']}\n{file['content']}" for file in files])

    prompt = f"""
      You are a helpful AI assistant tasked with generating a professional README file. 
      Below is the codebase of a project with multiple files. Analyze it and generate a detailed README.

      ### Instructions:
      - Provide a clear and concise **Project Title** and **Description**.
      - List **Installation Instructions** for setting up the project.
      - Explain how to run the project under **Usage**.
      - Highlight key **Features**.
      - Provide a **File Structure** overview, mentioning relevant files and their purposes.
      - Add a section for **Contributing** guidelines.
      - Include **License** information if applicable.
      - Provide **Contact Information**.

      Ensure the README is well-structured using markdown. Here is the codebase:

      {file_content_summary}
      """

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Ensure this is the correct model
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI that specializes in generating professional README files for GitHub repositories."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.5,
            max_tokens=	32768,
            top_p=1
        )

        print(completion.choices[0].message.content)
    except Exception as e:
        print(f"Error: {e}")
