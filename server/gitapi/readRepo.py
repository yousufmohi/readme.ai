import requests

def extractRepo(link):
  print(link)

def getInfo(username, token):
  
  url = f"https://api.github.com/repos/{username}/codestore"
  headers = {
    "Authorization": f"token {token}"
  } 
  
  response = requests.get(url, headers=headers)
  
  if response.status_code == 200:
      return response.json()
  else:
      print(f"Error: {response.status_code} - {response.json()}")