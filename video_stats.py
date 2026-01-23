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
        response.raise_for_status()
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


def extract_video_data(video_ids):

    
    extracted_data = []
    
    # helper function to extract videos in batch
    def batch_list(video_id_list,batch_size):
        for video_id in range(0, len(video_id_list),batch_size):
            yield video_id_list[video_id: video_id + batch_size]
    
    try:
        for batch in batch_list(video_ids,maxResults):
            video_ids_str = ",".join(batch)

            url = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_ids_str}&key={API_KEY}"

            # fetch data via api
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            for item in data.get('items',[]):
                video_id = item['id']
                snippet = item['snippet']
                contentDetails = item['contentDetails']
                statistics = item['statistics']

                # print(snippet)

                video_data = {
                    "video_id": video_id,
                    "title": snippet['title'],
                    "publishedAt": snippet['publishedAt'],
                    "duration": contentDetails['duration'],
                    "viewCount": statistics.get("viewCount", None),
                    "likeCount": statistics.get("likeCount", None),
                    "commentCount": statistics.get("commentCount", None)
                }

                extracted_data.append(video_data)

        return extracted_data

    except requests.exceptions.RequestException as e:
        raise e


if __name__ == '__main__':
    # get_playlist_id()

    playlistId = get_playlist_id()
    video_ids = get_video_ids(playlistId)
    # print(video_ids)
    print(extract_video_data(video_ids))
    # print(extract_video_data(video_ids))
