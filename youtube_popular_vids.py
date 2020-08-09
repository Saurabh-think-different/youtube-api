from googleapiclient.discovery import build
from tabulate import tabulate

api_key = "AIzaSyC9hoonEPFgrOyOcZOH3i8iDRw2AeTJ4m0"

youtube = build("youtube", "v3", developerKey=api_key)
nextPageToken = None

videos = []
while True:
    pl_request = youtube.playlistItems().list(
        part="contentDetails", 
        playlistId="PL-osiE80TeTt2d9bfVyTiXJA-UTHn6WwU",
        maxResults=50,
        pageToken = nextPageToken
        )
    pl_response = pl_request.execute()
    
    vid_ids = []
    for item in pl_response["items"]:
        vid_ids.append(item['contentDetails']['videoId'])


    vid_request = youtube.videos().list(
        part="statistics, snippet", 
        id = ','.join(vid_ids)
    )
    vid_response = vid_request.execute()
    
    for item in vid_response['items']:
        view_count = item['statistics']['viewCount']
        vid_id = item['id']
        yt_link = f'https://youtu.be/{vid_id}'
        title = item['snippet']['title']
        videos.append(
            {   
                "title": title,
                "view_count": int(view_count),
                "yt_link": yt_link
            }
        )
    nextPageToken = pl_response.get('nextPageToken')
    if not nextPageToken:
        break

videos.sort(key=lambda vid: vid['view_count'], reverse=True)
table_videos = []

for vid in videos:
    table_videos.append([vid['title'], vid['yt_link'], vid['view_count']])

print(tabulate(table_videos))