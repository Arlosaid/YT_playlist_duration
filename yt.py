import re
from datetime import timedelta
from googleapiclient.discovery import build

API_KEY = open('api_key','r').read()

youtube = build('youtube', 'v3', developerKey= API_KEY)

hours_pattern = re.compile(r'(\d+)H')
minutes_pattern = re.compile(r'(\d+)M')
seconds_pattern = re.compile(r'(\d+)S')

input_id = input("Type playlist ID: ")
total_seconds = 0

nextPageToken = None
while True:
    pl_request = youtube.playlistItems().list(
        part='contentDetails',
        playlistId= input_id,
        maxResults = 50,
        pageToken= nextPageToken
    )

    pl_response = pl_request.execute()

    video_id = []
    for item in pl_response['items']:
        video_id.append(item['contentDetails']['videoId'])

    vid_request = youtube.videos().list(
        part='contentDetails',
        id=','.join(video_id)
    )

    video_response = vid_request.execute()

    for item in video_response['items']:
        duration = item['contentDetails']['duration']
        
        hours = hours_pattern.search(duration)
        minutes = minutes_pattern.search(duration)
        seconds = seconds_pattern.search(duration)
        
        hours = int(hours.group(1)) if hours else 0
        minutes = int(minutes.group(1)) if minutes else 0
        seconds = int(seconds.group(1)) if seconds else 0
        
        video_seconds = timedelta(
            hours= hours,
            minutes = minutes,
            seconds = seconds
        ).total_seconds()
        
        total_seconds += video_seconds
    
        
    nextPageToken = pl_response.get('nextPageToken')
    
    if not nextPageToken:
        break

total_seconds = int(total_seconds)

minutes, seconds =divmod(total_seconds, 60) 
hours, minutes = divmod(minutes, 60)

print(f'{hours}h {minutes}m {seconds}s' )

     