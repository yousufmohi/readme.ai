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
  
  response = requests.get(url, headers=headers)
  
  if response.status_code == 200:
      return response.json()
  else:
      print(f"Error: {response.status_code} - {response.json()}")