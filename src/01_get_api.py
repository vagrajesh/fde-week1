import requests

url = "https://jsonplaceholder.typicode.com/posts/1"
response = requests.get(url)
print(response.json())
print(response.status_code)
print(response.json()["title"])