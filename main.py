import functions
import youtubeapi
import streamlit as st
from flask import session
import subprocess
import webbrowser
import pickle
import classes
import spotifyapi



if st.button("Login to spotify"):
    webbrowser.open_new_tab('http://192.168.9.199:5000/login')
    subprocess.run(['python', 'authorization.py'])

st.title("YOUTUBE PLAYLIST TO SPOTIFY PLAYLIST")

playlist_link = st.text_input("Enter Playlist Link:")
playlist_name = st.text_input("Enter Playlist Name:")

# Submit button

track_ids = []
if st.button("Create Playlist"):
    st.write('creating playlist...')
    if functions.create_playlist(playlist_name):
        track_ids = spotifyapi.run_spotifyapi(playlist_link)
        functions.add_to_playlist(track_ids)

    

