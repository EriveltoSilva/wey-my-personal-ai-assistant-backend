import json

import requests

url = "http://localhost:8000/api/v1/chat/conversation"
headers = {"Content-Type": "application/json"}


message = "Hello, i'm Clénio, how are you?"
data = {
    "streaming_mode": True,
    "search_mode": False,
    "model_name": "gpt-3.5-turbo",
    "temperature": 0.0,
    "messages": [{"role": "user", "content": message}],
}


response_message_before = ""
with requests.post(url, data=json.dumps(data), headers=headers, stream=True) as response:
    for chunk in response.iter_content(1024):
        response_message_before += chunk.decode("utf-8")
        # print(chunk)


new_message = "Do you know what is my name?"
data = {
    "streaming_mode": True,
    "search_mode": False,
    "model_name": "gpt-3.5-turbo",
    "temperature": 0.0,
    "messages": [
        {"role": "user", "content": message},
        {"role": "agent", "content": response_message_before},
        {"role": "user", "content": new_message},
    ],
}


with requests.post(url, data=json.dumps(data), headers=headers, stream=True) as response:
    final_response = ""
    for chunk in response.iter_content(1024):
        final_response += chunk.decode("utf-8")
        # print(chunk, end="")

    final_response = final_response.replace("\n\n", "")
    final_response = final_response.replace("<br/>", "\n")
    final_response = final_response.replace("data: ", "")
    print(final_response)
