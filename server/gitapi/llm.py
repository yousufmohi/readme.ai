import os
from dotenv import load_dotenv
import requests
from groq import Groq

load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")

if not groq_key:
    raise ValueError("GROQ_API_KEY is missing. Please check your .env file.")

def llm_prompt(file_summaries, repo):
    client = Groq(api_key=groq_key)

    def chunk_data(data, max_tokens=4000):
        chunks = []
        current_chunk = []
        current_size = 0
        for file in data:
            file_size = len(file['summary'])
            if current_size + file_size > max_tokens:
                chunks.append(current_chunk)
                current_chunk = []
                current_size = 0
            current_chunk.append(file)
            current_size += file_size
        if current_chunk:
            chunks.append(current_chunk)
        return chunks

    chunks = chunk_data(file_summaries)
    all_summaries = []

    for chunk in chunks:
        summary_text = '\n\n'.join([f"File: {file['path']}\n{file['summary']}" for file in chunk])

        # Updated prompt for generating a better README
        prompt = f"""
        You are an AI assistant specializing in generating clear, concise, and professional README files for open-source projects. Based only on the project files provided below, please create a comprehensive README that includes only the relevant information. Your goal is to make the README as informative and easy to follow as possible, while ensuring that it is accurate, well-organized, and professional.
        
        **Instructions:**  
        - Extract the **Project Title** directly from the codebase or determine it from the folder structure (e.g., the name of the repository). Do not use placeholders or generic titles like "[PROJECT TITLE]".  
        - Include only the **relevant sections** that provide value to someone who may want to understand or use this project.  
        - Use markdown formatting to organize the README professionally.  

        Key sections to include if applicable:  
        - **Project Title**  
        - **Description** (Provide a summary of the project and its purpose)  
        - **Installation Instructions** (Step-by-step instructions to set up and install the project)  
        - **Usage Instructions** (How to run the project or use the features)  
        - **Key Features** (List of important functionalities or benefits of the project)  
        - **Technologies Used** (Include badges and mention frameworks, libraries, and tools used, if applicable)  
        - **License** (If there is any license information in the codebase, include it)  
        - **Contact Information** (If applicable)  
        - **API Documentation** (If there are APIs, list endpoints and functionality)

        **Important Formatting Guidelines:**  
        - Use **relevant technology badges** (e.g., for Node.js, Python, React, etc.) formatted with shields.io. Example:  
          ```markdown
          ![Node.js](https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=node.js&logoColor=white)
          ```  
        - Ensure clear and professional markdown formatting throughout the README.

        Here is the content of the project files:  
        **Project Name:** {repo}  
        {summary_text}
        """

        try:
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "system", "content": "You are an AI that specializes in generating professional README files for GitHub repositories."},
                          {"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=6000,
                top_p=1
            )

            all_summaries.append(completion.choices[0].message.content)
        except Exception as e:
            print(f"Error: {e}")
    
    final_readme = '\n\n'.join(all_summaries)
    
    # Final refinement prompt
    final_refinement_prompt = f"""
    You are an AI assistant specializing in generating clear, concise, and professional README files for open-source projects. Based solely on the project files provided below, create a comprehensive README that includes only the relevant information. Your goal is to make the README as informative and easy to follow as possible while ensuring that it is accurate, well-organized, and professional.

    ## Instructions
    - Extract the **Project Title** directly from the codebase or infer it from the folder structure (e.g., the name of the repository).
    - Include only **relevant sections** that provide value to users who may want to understand or use the project.
    - Format the README using clean and consistent markdown.

    ### Essential Sections to Include:
    - **Project Title**
    - **Description** (Summarize the project's purpose and functionality)
    - **Installation Instructions** (Provide step-by-step setup guidance)
    - **Usage Instructions** (Explain how to run or use the project)
    - **Key Features** (List the main functionalities or benefits)
    - **Technologies Used** (Include shields.io badges for tools, frameworks, and languages)
    - **License** (Include license details if applicable)
    - **Contact Information** (Provide ways for users to reach out for support or collaboration)
    - **API Documentation** (List any endpoints with descriptions)

    ## Markdown Formatting Guidelines
    - Use **shields.io badges** for relevant technologies. Example:
    ```markdown
    ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
    ```
    - Maintain clear, organized sections with descriptive headings.
    - Ensure consistent formatting for code blocks and inline code using triple backticks.
    - Provide clear explanations without redundancy.

    ## Example Prompt
    ```plaintext
    Based on the following project files, generate a comprehensive README for an open-source project named `{repo}`.

    Here are the summarized file contents:

    {summary_text}

    Please ensure the README includes all essential sections while maintaining clarity and professionalism.
    ```

    ## Refinement Prompt
    ```plaintext
    Please refine the following README to ensure it's well-structured, consistent, and professional. Make necessary improvements for readability, clarity, and organization. Ensure proper markdown formatting with clean sectioning and correct use of shields.io badges.

    Only provide the final README content with no additional comments or explanations.

    {final_readme}
    """
    
    try:
        refinement_completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "system", "content": "You are an AI that specializes in generating professional README files for GitHub repositories."},
                      {"role": "user", "content": final_refinement_prompt.replace("[Insert your final README content here]", final_readme)}],
            temperature=0.5,
            max_tokens=6000,
            top_p=1
        )
        refined_readme = refinement_completion.choices[0].message.content


        return refined_readme

    except Exception as e:
        print(f"Error: {e}")
