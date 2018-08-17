import requests
import json

req_rec = requests.post("http://127.0.0.1:5000/recommend", params={'user_id': 35})
req_rel = requests.post("http://127.0.0.1:5000/related", params={'submission_id': 10})

print(req_rec.status_code, req_rec.reason)
print(req_rel.status_code, req_rel.reason)

# json_data_rec = json.loads(req_rec.text)
# json_data_rel = json.loads(req_rel.text)

# print(json_data_rec)
# print(json_data_rel)