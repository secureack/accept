import requests
import json

body = { "test" : "1", "test1" : "2", "test3" : "3" }

response = requests.post("http://127.0.0.1:5657/?auth=123", data=json.dumps(body))
print(response.status_code)
