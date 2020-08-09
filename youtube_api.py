from googleapiclient.discovery import build

api_key = "AIzaSyC9hoonEPFgrOyOcZOH3i8iDRw2AeTJ4m0"

youtube = build("youtube", "v3", developerKey=api_key)
nextPageToken = None

# ch_request = youtube.videos().list(
#     part="snippet",
#     id="EiItLWWxgOI"
# )
# ch_response = ch_request.execute()
# print(ch_response['items'][0]['snippet']['title'])
pl_request = youtube.playlistItems().list(
    part="contentDetails", 
    playlistId="PL-osiE80TeTt2d9bfVyTiXJA-UTHn6WwU",
    maxResults=50,
    pageToken = nextPageToken
    )
pl_response = pl_request.execute()
# print(pl_response)
vid_ids = []
for item in pl_response["items"]:
    vid_ids.append(item['contentDetails']['videoId'])
print(len(vid_ids))

vid_request = youtube.videos().list(
    part="snippet",
    id = ','.join(vid_ids)
)
vid_response = vid_request.execute()
print(vid_response['items'][0]['snippet']['title'])
