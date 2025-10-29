import requests

url = "http://127.0.0.1:8000/sentiment/"
headers = {"x-api-key": "12345SECRET"}  
data = {"text": "Today was amazing"}

response = requests.post(url, headers=headers, json=data)
print(response.json())
