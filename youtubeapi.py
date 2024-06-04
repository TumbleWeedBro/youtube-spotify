from dotenv import load_dotenv
import os
from googleapiclient.discovery import build

load_dotenv()

# functions
def get_requestItems(playlistId_source):
    requestItems = youtube.playlistItems().list(
        part='contentDetails',
        playlistId=playlistId_source,
        maxResults=5)
    response = requestItems.execute()
    # print(response)
    return response

def get_requestItems_nextPage(playlistId_source, nextPageToken):
    requestItems = youtube.playlistItems().list(
    part='contentDetails',
    playlistId=playlistId_source,
    maxResults=5,
    pageToken = nextPageToken)
    response = requestItems.execute()
    # print(response)
    return response

def get_playlistItems(playlistId_source):
    response = get_requestItems(playlistId_source)

    playlistItems = response['items']
    nextPageToken = response.get('nextPageToken')

    while nextPageToken:
        response = get_requestItems_nextPage(playlistId_source, nextPageToken)
        playlistItems.extend(response['items'])
        nextPageToken = response.get('nextPageToken')
    return playlistItems


def get_videoTitle():
    song_titles = []
    for item in playlist_Items:
        # get video id
        item_id = item['contentDetails']['videoId']
        requestVideo = youtube.videos().list(part='snippet', id=item_id)
        response = requestVideo.execute()
        # get song title
        try:
            song_titles.append(response['items'][0]['snippet']['title'])
        except:
            next

    return song_titles

api_key = os.getenv("YOUTUBE_API_KEY")
youtube = build('youtube', 'v3', developerKey=api_key)

playlistId_source = 'PLs7ijEcGOG01Su9hxoclK6WO-HIagz_V5'
playlist_Items = get_playlistItems(playlistId_source)



