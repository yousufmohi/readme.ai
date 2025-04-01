import os
import re
import requests
from dotenv import load_dotenv
from .llm import llm_prompt
import re

load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")

if not groq_key:
    raise ValueError("GROQ_API_KEY is missing. Please check your .env file.")

def extract_summary(content, max_length=500):
    comments = re.findall(r'#.*|//.*|/\*.*?\*/', content, re.DOTALL)
    functions = re.findall(r'def\s+(\w+)\s*\(|function\s+(\w+)\s*\(', content)
    classes = re.findall(r'class\s+(\w+)\s*\(?', content)

    comment_text = '\n'.join(comments[:5])  # Limit to 5 comments
    function_names = ', '.join([f[0] or f[1] for f in functions[:10]])  # Limit to 10 functions
    class_names = ', '.join(classes[:5])  # Limit to 5 classes

    summary = f"Comments: {comment_text}\nFunctions: {function_names}\nClasses: {class_names}"
    return summary[:max_length]  # Ensure the summary doesn't exceed max_length

def extract_link_information(link):
    if "https://" in link:
        link_data = link.replace("https://github.com/", "").split('/')
    else:
        link_data = link.replace("github.com/", "").split('/')

    return link_data[0], link_data[1]


def get_info(link, token):
    username, repo = extract_link_information(link)
    url = f"https://api.github.com/repos/{username}/{repo}/contents"
    headers = {"Authorization": f"token {token}"}

    relevant_extensions = {'.py', '.js', '.java', '.cpp', '.c', '.cs', '.html', '.css', '.ts', '.rb', '.go', '.rs', '.jsx', '.tsx'}
    ignored_dirs = {'venv', '.venv', 'lib_site', 'node_modules', '__pycache__', '.next', '.github', 'test'}

    def fetch_files(directory_url):
        response = requests.get(directory_url, headers=headers)

        if response.status_code == 200:
            contents = response.json()
            files_data = []
            for item in contents:
                if item['type'] == 'dir' and item['name'] not in ignored_dirs:
                    files_data.extend(fetch_files(item['url']))
                elif item['type'] == 'file' and any(item['name'].endswith(ext) for ext in relevant_extensions):
                    file_content = requests.get(item['download_url'], headers=headers).text
                    file_summary = extract_summary(file_content)
                    files_data.append({"path": item['path'], "summary": file_summary})
            return files_data
        else:
            print(f"Error: {response.status_code} - {response.json()}")
            return []
    data = fetch_files(url)
    return llm_prompt(data,repo)
