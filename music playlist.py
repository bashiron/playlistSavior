from googleapiclient.discovery import build
from datetime import date
import json

api_key = 'AIzaSyDsYE8KPNDbcVcC5Sfog1uTS8VvZj3RCNY'

youtube = build('youtube', 'v3', developerKey=api_key)

titulos = []
nextPageToken = None

while True:
    pl_request = youtube.playlistItems().list(
        part='contentDetails',
        playlistId='PL_hXMzbIDwY4II8UXP93yd7n_HvcFg8rF',
        maxResults=50,
        pageToken=nextPageToken
    )

    pl_response = pl_request.execute()
    vid_ids = [item['contentDetails']['videoId'] for item in pl_response['items']]

    vid_request = youtube.videos().list(
        part="snippet",
        id=','.join(vid_ids)
    )

    vid_response = vid_request.execute()
    for item in vid_response['items']:
        titulos.append(item['snippet']['title'])

    nextPageToken = pl_response.get('nextPageToken')

    if not nextPageToken:
        break

numeracion = []
num = 1
while num < len(titulos) + 1:
    numeracion.append(f'{num}) ')
    num += 1

# newlines = ['\n' for x in numeracion]
parejas = tuple(zip(numeracion, titulos))
parejas = list(map(lambda x: ''.join(x), parejas))

with open(f'C:/bashi/playlists/generated/music {date.today()}.txt', 'xb') as fp:
    fp.write('\n'.join(parejas).encode('UTF-8'))

print('<<music file created successfully>>')
# test git
