# llm.py
import os
from dotenv import load_dotenv
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

        prompt = f"""
You are an expert technical writer and GitHub maintainer. Based solely on the files and metadata provided, write a clean, complete, and professional `README.md`.

### STRICT RULES:
- Use only factual information from the actual codebase. Do NOT invent features, descriptions, or commands.
- Never repeat the project title or sections.
- ⚠️ DO NOT use placeholders such as:
  - [project description]
  - [username], [email address]
  - [LICENSE]
  - [list key technologies or frameworks]
- You must not insert any placeholders. If the real data is not in the provided codebase, SKIP that section entirely.
- Avoid merge markers like `===` or repeated headers.

### STRUCTURE:
1. **Project Title**: One `# {repo}` heading
2. **Technology Badges**: Immediately under the title, display all shields.io tech badges horizontally in one line
3. **Description**: 2–5 sentence summary of what the project actually does
4. **Installation**: Based only on setup files or clearly defined instructions in the codebase
5. **Usage**: Actual commands used to start or run the project
6. **Features**: Bullet points of real features from the project
7. **APIs**: Include only if defined in the code (e.g. Express routes or FastAPI endpoints)
8. **Dependencies**: Major libraries/tools used
9. **License**: Include only if the license file exists
10. **Contributing/Contact**: Only if found in the codebase

### Style Rules:
- Output clean GitHub Markdown only
- Keep badge icons inline (horizontally), not stacked
- No commentary, placeholders, or repeated sections

### Project Name: `{repo}`

### Codebase Summary:
{summary_text.strip()}
"""

        try:
            completion = client.chat.completions.create(
                model = "llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are an AI that generates professional GitHub README files using real information from the codebase only. You must not guess, add placeholders, or create fictional content. If something is missing from the code, omit it entirely."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=6000,
                top_p=1
            )

            all_summaries.append(completion.choices[0].message.content)
        except Exception as e:
            print(f"Error: {e}")
            return "Error generating README. Please try again."

    final_readme = '\n\n'.join(all_summaries).strip()

    refinement_prompt = f"""
You are an AI assistant that merges partial `README.md` drafts into a single, professional, and coherent GitHub README file.

### Your goals:
- ✅ Output a SINGLE complete README.md
- ✅ No repeated headers or duplicate sections
- ✅ Use ONLY information extracted from the codebase
- ✅ Keep badge layout inline under the title
- ✅ Remove placeholders like [username], [email address], or [project description]

### Final Output Instructions:
- Use clean GitHub Markdown formatting
- Preserve logical section order: title → badges → description → install → usage → features → APIs → dependencies → license → contact

## Input Drafts:
{final_readme}

Return only the final README.md markdown content — clean, deduplicated, and polished.
"""

    try:
        refinement = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You refine and clean up partial README drafts into one complete file, removing placeholders and cleaning markdown. Only output one final README."},
                {"role": "user", "content": refinement_prompt}
            ],
            temperature=0.3,
            max_tokens=6000,
            top_p=1
        )
        return refinement.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error: {e}")
        return final_readme