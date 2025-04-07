import requests

url = "http://localhost:5000/shorten"
data = {"url": "https://www.google.com"}

response = requests.post(url, json=data)
print(response.json())  # Print the shortened URL response
