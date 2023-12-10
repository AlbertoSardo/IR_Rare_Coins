import requests

url = "http://localhost:8000/search/"
params = {"query": "euro"}

response = requests.post(url, params=params)

print(response.text)
