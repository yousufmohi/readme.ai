import os
import re
import requests
from dotenv import load_dotenv
from .llm import llm_prompt

load_dotenv()

def extract_summary(content, max_length=500):
    comments = re.findall(r'#.*|//.*|/\*.*?\*/', content, re.DOTALL)
    functions = re.findall(r'def\s+(\w+)\s*\(|function\s+(\w+)\s*\(', content)
    classes = re.findall(r'class\s+(\w+)\s*\(?', content)

    comment_text = '\n'.join(comments[:5])
    function_names = ', '.join([f[0] or f[1] for f in functions[:10]])
    class_names = ', '.join(classes[:5])

    summary = f"Comments: {comment_text}\nFunctions: {function_names}\nClasses: {class_names}"
    return summary[:max_length]

def extract_link_information(link):
    if "https://" in link:
        link_data = link.replace("https://github.com/", "").split('/')
    else:
        link_data = link.replace("github.com/", "").split('/')
    return link_data[0], link_data[1]

def is_valid_github_url(url: str) -> bool:
    pattern = r"^https?://(www\.)?github\.com/[\w-]+/[\w.-]+/?$"
    if re.match(pattern, url) is not None:
        return True
    else:
        return False

def get_info(link, token):
    if not is_valid_github_url(link):
        return False

    username, repo = extract_link_information(link)
    url = f"https://api.github.com/repos/{username}/{repo}/contents"
    headers = {"Authorization": f"token {token}"}

    relevant_extensions = {'.py', '.js', '.java', '.cpp', '.c', '.cs', '.html', '.css', '.ts', '.rb', '.go', '.rs', '.jsx', '.tsx'}
    important_files = {'requirements.txt', 'package.json', 'setup.py', 'pyproject.toml'}
    ignored_dirs = {'venv', '.venv', 'lib_site', 'node_modules', '__pycache__', '.next', '.github', 'test'}

    def fetch_files(directory_url):
        response = requests.get(directory_url, headers=headers)
        if response.status_code == 200:
            contents = response.json()
            files_data = []
            for item in contents:
                if item['type'] == 'dir' and item['name'] not in ignored_dirs:
                    files_data.extend(fetch_files(item['url']))
                elif item['type'] == 'file' and (item['name'].endswith(tuple(relevant_extensions)) or item['name'] in important_files):
                    file_content = requests.get(item['download_url'], headers=headers).text
                    file_summary = extract_summary(file_content) if item['name'] not in important_files else file_content[:500]
                    files_data.append({"path": item['path'], "summary": file_summary})
            return files_data
        else:
            print(f"Error: {response.status_code} - {response.json()}")
            return []

    data = fetch_files(url)
    return llm_prompt(data, repo)