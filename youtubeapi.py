from dotenv import load_dotenv
import os
from googleapiclient.discovery import build

load_dotenv()

api_key = os.getenv("YOUTUBE_API_KEY")
youtube = build('youtube', 'v3', developerKey=api_key)
# functions
def get_requestItems(playlist_link):
    requestItems = youtube.playlistItems().list(
        part='contentDetails',
        playlistId=playlist_link,
        maxResults=5)
    response = requestItems.execute()
    # print(response)
    return response

def get_requestItems_nextPage(playlist_link, nextPageToken):
    requestItems = youtube.playlistItems().list(
    part='contentDetails',
    playlistId=playlist_link,
    maxResults=5,
    pageToken = nextPageToken)
    response = requestItems.execute()
    # print(response)
    return response

def get_playlistItems(playlist_link):
    response = get_requestItems(playlist_link)

    playlistItems = response['items']
    nextPageToken = response.get('nextPageToken')

    while nextPageToken:
        response = get_requestItems_nextPage(playlist_link, nextPageToken)
        playlistItems.extend(response['items'])
        nextPageToken = response.get('nextPageToken')
    return playlistItems


def get_videoTitle(playlist_Items):
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





