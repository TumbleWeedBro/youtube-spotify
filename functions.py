import requests
import streamlit as st
import time
import os
from datetime import datetime, timedelta
import spotifyapi
import json
import classes

REDIRECT_URI = 'http://localhost:5000/callback'
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'


client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def create_playlist(playlist_name):
    session_obj = classes.SpotifySession()
    session_obj = session_obj.load_from_file('spotify_session.pkl')

    url = f"https://api.spotify.com/v1/users/{session_obj.user_id}/playlists"
    request_body = {
        'name': playlist_name,
        'description': "This is a public playlist made by youtube-spotify",
        'public': True
    }
    headers = spotifyapi.get_auth_header(session_obj.access_token)
    response = requests.post(url=url, headers=headers, json=request_body)
    json_result = json.loads(response.content)
    session_obj.get_playlist_id(json_result['id'])
    session_obj.save_to_file('spotify_session.pkl')
    print(json_result)
    if response.status_code == 201:
        st.write("Playlist created successfully") 
        return True
    else:
        st.write(f"Error creating playlist: {response.text}")
        return False

def add_to_playlist(track_ids):
    session_obj = classes.SpotifySession()
    session_obj = session_obj.load_from_file('spotify_session.pkl')
    url = f"https://api.spotify.com/v1/playlists/{session_obj.playlist_id}/tracks"
    headers = spotifyapi.get_auth_header(session_obj.access_token)
    request_body = {
        "uris": track_ids
    }
    response = requests.post(url=url, headers=headers, json=request_body)
    if response.ok:
        st.write("Songs added to playlist successfully")
        st.write(f"Songs added - {len(track_ids)} ") 
        return True
    else:
        st.write(f"Error creating playlist: {response.text}")
        return False