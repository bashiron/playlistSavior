import os, psycopg
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

    def save_playlist(self, pl_type):
        titles = self.obtain_titles(pl_type['id'])
        self.save_titles(titles, pl_type['name'])

    # TODO fetch video tags (snippet.tags[])
    # TODO fetch channel title (snippet.channelTitle)
    def obtain_titles(self, pl_id):
        """Fetch video titles from playlist.

        Parameters
        ----------
        pl_id : `str`
            Youtube ID of the playlist.

        Returns
        -------
        titles : `list`
            List containing titles of all videos.
        """
        titles = []
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

            print('requesting videos...')
            vid_response = vid_request.execute()
            for item in vid_response['items']:
                titles.append(item['snippet']['title'])

            next_token = pl_response.get('nextPageToken')

            if not next_token:
                break

        return titles

    def save_titles(self, titles, name):
        enum = []
        num = 1
        while num < len(titles) + 1:
            enum.append(f'{num}) ')
            num += 1

        pairs = zip(enum, titles)
        pairs = list(map(lambda x: ''.join(x), pairs))

        with open(f'/home/bashiron/playlists/generated/{name} {date.today()}.txt', 'xb') as fp:
            fp.write('\n'.join(pairs).encode('UTF-8'))

        print(f'<<{name} file created successfully>>')
