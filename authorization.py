import requests
import subprocess
import threading
import time
import os
import urllib.parse
from datetime import datetime, timedelta
from flask import Flask, redirect, request, jsonify, session, url_for
import spotifyapi
import json
import pickle
import classes

REDIRECT_URI = 'http://localhost:5000/callback'
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

app = Flask(__name__)
app.secret_key = '8491ert4er8-498sdgs-498dbdfgh1r8'



def shutdown_server():
    os._exit(0)

def run_streamlit():
    subprocess.run(["streamlit", "run", "main.py", "--server.port", "8502", "--server.headless", "true"])

def start_streamlit():
    streamlit_thread = threading.Thread(target=run_streamlit)
    streamlit_thread.start()
    time.sleep(2)

def get_user_id(headers):
    user_profile_url = f"{API_BASE_URL}me"
    response = requests.get(user_profile_url, headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        return user_data['id']
    else:
        return None

@app.route('/')
def index():
    return redirect('/login ')

@app.route('/login')
def login():
    scope = 'user-read-private user-read-email playlist-modify-public playlist-modify-private '

    params = {
        'client_id': client_id,
        'response_type': 'code',
        'scope': scope,
        'redirect_uri': REDIRECT_URI,
        'show_dialog': True
    }

    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    return redirect(auth_url)

@app.route('/callback')
def callback():
    if 'error' in request.args:
        return jsonify({"error": request.args['error']})

    if 'code' in request.args:
        request_body = {
            'code': request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI,
            'client_id': client_id,
            'client_secret': client_secret
        }

    response = requests.post(TOKEN_URL, data=request_body)
    token_info = response.json()

    headers = {'Authorization': f"Bearer {token_info['access_token']}"}
    session_obj = classes.SpotifySession()
    session_obj.set_tokens(token_info)
    session_obj.set_user_id(headers)
    session_obj.save_to_file('spotify_session.pkl')

    return redirect("http://localhost:8501")


@app.route('/playlists')
def get_playlist():
    if 'access_token' not in session:
        return redirect('/login')

    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')

    headers = {'authorization': f"Bearer {session['access_token']}"}
    response = requests.get(API_BASE_URL + 'me/playlist', headers=headers)
    playlists = response.json()

    return jsonify(playlists)

@app.route('/refresh-token')
def refresh_token():
    if 'refresh_token' not in session:
        return redirect('/login')

    if datetime.now().timestamp() > session['expires_at']:
        request_body = {
            'grant_type': 'refresh_token',
            'refresh_token': session['refresh_token'],
            'client_id': client_id,
            'client_secret': client_secret
        }

    response = requests.post(TOKEN_URL, data=request_body)
    new_token_info = response.json()

    session['access_token'] = new_token_info['access_token']
    session['expires_at'] = datetime.now().timestamp(
    ) + new_token_info['expires_in']

    return redirect('/playlists')



@app.route('/main')
def redirect_to_main():
    exec(open('main.py').read())
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    shutdown_server()


# done
