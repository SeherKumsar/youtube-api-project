import pandas as pd

def get_chanel_stats(youtube, channel_ids):
    # Bir liste oluşturarak verileri bu listeye ekle
    all_data = []

    request = youtube.channels().list(
        part="snippet, contentDetails, statistics", # part parametresi ile verileri seçmek zorunlu
        id=','.join(channel_ids) # id parametresi ile kanal id'lerini virgül ile ayırarak gönderiyoruz
    )

    response = request.execute()

    for item in response["items"]:
        data = {
            'channelName': item["snippet"]["title"],
            'subscribers': item["statistics"]["subscriberCount"],
            'views': item["statistics"]["viewCount"],
            'totalVideos': item["statistics"]["videoCount"],
            'playlistId': item["contentDetails"]["relatedPlaylists"]["uploads"]
        }
        all_data.append(data)

    return pd.DataFrame(all_data)

def get_video_ids(youtube, playlist_id):
    video_ids = []

    request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=playlist_id,
            maxResults=50
        )
    response = request.execute()

    for item in response['items']:
        video_ids.append(item['contentDetails']['videoId'])

    next_page_token = response.get('nextPageToken')
    
    while next_page_token is not None:
        request = youtube.playlistItems().list(
                part="snippet,contentDetails",
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token
            )
        response = request.execute()

        for item in response['items']:
            video_ids.append(item['contentDetails']['videoId'])

        next_page_token = response.get('nextPageToken')    

        
    return video_ids

