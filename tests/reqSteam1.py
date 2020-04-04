import requests
import re


url = "http://192.168.1.12:8050/video_feed"


req = requests.get(url, stream=True)

response = req.raw.read(100000)

match = re.findall(b"\xff\xd8",response)

print(len(match))
