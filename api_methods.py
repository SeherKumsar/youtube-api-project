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