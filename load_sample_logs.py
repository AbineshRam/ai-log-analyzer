import json
import requests

URL = "http://127.0.0.1:8000/logs"

with open("sample_logs.json") as f:
    logs = json.load(f)

for log in logs:
    r = requests.post(URL, json=log)
    print(r.status_code, r.json())
