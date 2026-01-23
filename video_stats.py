import requests
import json

import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")

# global variables
API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLER = 'MrBeast'
maxResults = 50

def get_playlist_id():

    try:
        url = f'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLER}&key={API_KEY}'
        response = requests.get(url)
        response.raise_for_status
        data = response.json()
        print(data)
        # print(json.dumps(data,indent=4))
        channel_items = data["items"][0]
        channel_playlistId = channel_items["contentDetails"]["relatedPlaylists"]["uploads"]
        print(channel_playlistId)
        return channel_playlistId

    except requests.exceptions.RequestException as e:
        raise e

def get_video_ids(playlistId):

    # initialize variables
    videoIds = []
    pageToken = None
    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResults}&playlistId={playlistId}&key={API_KEY}"

    # call api via requests
    try:
        while True:
            # create url
            url = base_url
            if pageToken:
                url += f"&pageToken={pageToken}" 

            # fetch data via api 
            response = requests.get(url)
            response.raise_for_status
            data = response.json()

            # extract video ids from data
            for item in data.get('items',[]):
                videoId = item['contentDetails']['videoId']
                videoIds.append(videoId)

            # get nextPageToken from data
            pageToken = data.get('nextPageToken',[])

            if not pageToken:
                break
        
        # print(videoIds)
        return videoIds

    # handle exception
    except requests.exceptions.RequestException as e:
        
        raise e

if __name__ == '__main__':
    # get_playlist_id()

    playlistId = get_playlist_id()
    print(get_video_ids(playlistId))
