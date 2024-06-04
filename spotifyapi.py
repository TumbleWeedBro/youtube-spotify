from dotenv import load_dotenv
import requests
import os
import base64
import json
import re
from youtubeapi import get_videoTitle

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization":"Basic " + auth_base64,
        "Content-Type":"application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = requests.post(url=url, headers=headers, data=data)
    json_result = json.loads(result.content)

    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


def get_track_id(token, song_name):
    url = "https://api.spotify.com/v1/search/"
    headers = get_auth_header(token)
    query = f"?q={song_name}&type=track&limit=1"

    query_url = url + query
    result = requests.get(query_url, headers=headers)
    json_result = json.loads(result.content)
    track_id = json_result['tracks']['items'][0]['id']
    return track_id
    # print(json_results)

token = get_token()
song_titles = get_videoTitle()
print(song_titles)
track_ids = []
# # Original string
for title in song_titles:
    # Removing the text within brackets
    song_name = re.sub(r'\s*\([^)]*\)', '', title)
    track_ids.append(get_track_id(token, song_name))

print(track_ids)
#done
