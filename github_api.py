import requests, pprint, json
pprint.pp(requests.get("https://api.github.com").headers["X-GitHub-Media-Type"])