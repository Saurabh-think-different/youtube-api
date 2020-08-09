import re
from datetime import timedelta

from googleapiclient.discovery import build

api_key = "AIzaSyC9hoonEPFgrOyOcZOH3i8iDRw2AeTJ4m0"

youtube = build("youtube", "v3", developerKey=api_key)


hrs_pattern = re.compile(r'(\d+)H')
min_pattern = re.compile(r'(\d+)M')
sec_pattern = re.compile(r'(\d+)S')

nextPageToken = None

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
            part = 'contentDetails',
            id = ','.join(vid_ids)
        )   
    vid_response = vid_request.execute() 
    total_duration = 0
    for item in vid_response['items']:
        vid_duration =item['contentDetails']['duration']
        
        hours = hrs_pattern.search(vid_duration)
        mins = min_pattern.search(vid_duration) 
        secs = sec_pattern.search(vid_duration)
        # some of the videos might not have hours/mins/secs which return None, 
        #  this takes care of those
        hours = int(hours.group(1)) if hours else 0
        mins = int(mins.group(1)) if mins else 0
        secs = int(secs.group(1)) if secs else 0
        vid_secs = timedelta(
            hours= hours,
            minutes=mins,
            seconds=secs
        ).total_seconds()

        total_duration += vid_secs

    nextPageToken = pl_response.get('nextPageToken')
    #print(nextPageToken)

    if not nextPageToken:
        break

total_duration = str(timedelta(seconds=total_duration))
print(total_duration)
