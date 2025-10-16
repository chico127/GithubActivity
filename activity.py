import requests, json
from collections import defaultdict

username = input("Enter GitHub username: ")
token = "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"

url = f"https://api.github.com/users/{username}/events"
headers = {"Authorization": f"Bearer {token}"}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    data.sort(key=lambda item: [item["repo"]["id"], item["type"], item["created_at"]])
    for i in data:





        print(i) #print(json.dumps(data, indent=4))
else:
    print(f"Error: {response.status_code}")


