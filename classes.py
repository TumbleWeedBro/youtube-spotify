from datetime import datetime, timedelta
import requests
import pickle

class SpotifySession:
    def __init__(self):
        self.access_token = None
        self.refresh_token = None
        self.expires_at = None
        self.user_id = None
        self.headers = None
        self.playlist_id = None

    
    def set_tokens(self, token_info):
        self.access_token = token_info['access_token']
        self.refresh_token = token_info['refresh_token']
        self.expires_at = datetime.now().timestamp() + token_info['expires_in']

    def set_user_id(self, headers):
        self.headers = headers
        self.user_id = self.get_user_id()

    def get_user_id(self):
        response = requests.get('https://api.spotify.com/v1/me', headers=self.headers)
        if response.status_code == 200:
            return response.json()['id']
        else:
            return None
            
    def get_playlist_id(self, playlist_id):
        self.playlist_id = playlist_id

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self, file)

    @staticmethod
    def load_from_file(filename):
        with open(filename, 'rb') as file:
            return pickle.load(file)

class PlaylistInfo:
    def __init__(self, playlist_link, playlist_name):
        self.playlist_link = playlist_link
        self.playlist_name = playlist_name

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self, file)

    @staticmethod
    def load_from_file(filename):
        with open(filename, 'rb') as file:
            playlist_info = pickle.load(file)
        return playlist_info

