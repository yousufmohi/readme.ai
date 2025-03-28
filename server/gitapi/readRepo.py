import requests

def extract_link_information(link: str):
  if "https://" in link:
    link_data = link.replace("https://github.com/", "").split('/')
    username = link_data[0]
    repo = link_data[1]
  else:
    link_data = link.replace("github.com/", "").split('/')
    username = link_data[0]
    repo = link_data[1] 
  return username,repo



def get_info(link, token):
  username,repo = extract_link_information(link)
  url = f"https://api.github.com/repos/{username}/{repo}/contents"
  headers = {
    "Authorization": f"token {token}"
  } 

  relevant_extensions = {'.py', '.js', '.java', '.cpp', '.c', '.cs', '.html', '.css', '.ts', '.rb', '.go', '.rs','.jsx','.tsx'}

  ignored_dirs = {'venv', '.venv', 'lib_site', 'node_modules', '__pycache__'}

  def fetch_files(directory_url):
      response = requests.get(directory_url, headers=headers)

      if response.status_code == 200:
          contents = response.json()
          files_data = []
          for item in contents:
              if item['type'] == 'dir':
                  if item['name'] not in ignored_dirs:
                      print(f"Directory: {item['path']}")
                      files_data.extend(fetch_files(item['url']))
              elif item['type'] == 'file':
                  if any(item['name'].endswith(ext) for ext in relevant_extensions):
                      file_content = requests.get(item['download_url'], headers=headers).text
                      files_data.append({"path": item['path'], "content": file_content})
                      print(f"File: {item['path']} downloaded.")
          return files_data
      else:
          print(f"Error: {response.status_code} - {response.json()}")
          return []

  fetch_files(url)


