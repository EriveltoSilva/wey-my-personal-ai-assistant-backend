import json

import requests

url = "http://localhost:8000/api/v1/chat/quick_response"
message = "Hello, how are you?"
data = {"content": message}

headers = {"Content-Type": "application/json"}

with requests.post(url, data=json.dumps(data), headers=headers, stream=True) as response:
    for chunk in response.iter_content(1024):
        print(chunk.decode("utf-8"))
