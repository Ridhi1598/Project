import requests
import json

from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning


webhook_url = "http://localhost:5000/"

data = {"name": "himanshu"}

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
r = requests.post(webhook_url, data=json.dumps(data), headers= {"Content-Type": "application/json"}, verify=False)

# r = requests.get(webhook_url)

print(r)
