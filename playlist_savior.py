import os
from googleapiclient.discovery import build
from datetime import date
from functools import partial
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ["DEV_KEY"]

youtube = build('youtube', 'v3', developerKey=api_key)

smash_id = 'PL_hXMzbIDwY6JUkTmCCoL1BwVIDHQpnRb'
music_id = 'PL_hXMzbIDwY4II8UXP93yd7n_HvcFg8rF'
favs_id = 'FLtpm7glO-bH0NlP2mxldq4g'

SMASH = {'name': 'smash', 'id': smash_id}
MUSIC = {'name': 'music', 'id': music_id}
FAVS = {'name': 'favorites', 'id': favs_id}

class Savior:

    def save_playlist(self, tipo):
        titulos = self.obtain_titles(tipo['id'])
        self.save_titles(titulos, tipo['name'])

    def obtain_titles(self, pl_id):
        titulos = []
        next_token = False
        part_request = partial(youtube.playlistItems().list, part='contentDetails', playlistId=pl_id, maxResults=50)

        while True:
            pl_request = part_request(pageToken=next_token) if next_token else part_request()
            pl_response = pl_request.execute()
            vid_ids = [item['contentDetails']['videoId'] for item in pl_response['items']]

            vid_request = youtube.videos().list(
                part="snippet",
                id=','.join(vid_ids)
            )

            vid_response = vid_request.execute()
            for item in vid_response['items']:
                titulos.append(item['snippet']['title'])

            next_token = pl_response.get('nextPageToken')

            if not next_token:
                break

        return titulos

    def save_titles(self, titulos, nombre):
        numeracion = []
        num = 1
        while num < len(titulos) + 1:
            numeracion.append(f'{num}) ')
            num += 1

        # newlines = ['\n' for x in numeracion]
        parejas = tuple(zip(numeracion, titulos))
        parejas = list(map(lambda x: ''.join(x), parejas))

        with open(f'C:/bashi/playlists/generated/{nombre} {date.today()}.txt', 'xb') as fp:
            fp.write('\n'.join(parejas).encode('UTF-8'))

        print(f'<<{nombre} file created successfully>>')
