import os, psycopg
from functools import partial

from googleapiclient.discovery import build
from dotenv import load_dotenv

from log_prep import *

load_dotenv()
api_key = os.environ["DEV_KEY"]

youtube = build('youtube', 'v3', developerKey=api_key)

smash_id = 'PL_hXMzbIDwY6JUkTmCCoL1BwVIDHQpnRb'
music_id = 'PL_hXMzbIDwY4II8UXP93yd7n_HvcFg8rF'
favs_id = 'FLtpm7glO-bH0NlP2mxldq4g'

SMASH = {'name': 'smash', 'id': smash_id}
MUSIC = {'name': 'music', 'id': music_id}
FAVS = {'name': 'favs', 'id': favs_id}

class Savior:

    def init_and_save(self, pl):
        with psycopg.connect('dbname=playlist user=bashiron') as conn:
            with conn.cursor() as cursor:
                self.save(pl, cursor)

    def save(self, pl, cursor):
        """Fetch video data from playlist and store in database.
        :param pl: playlist to store videos from
        :param cursor: postgres cursor
        """
        # name <- snippet.title
        # playlist <- set from the pl.name
        # apvid <- id
        # duration <- contentDetails.duration
        # ---
        # title <- snippet.title
        # description <- snippet.description
        # tags <- snippet.tags[]
        # upload_date <- snippet.publishedAt
        # channel <- snippet.channelTitle
        # thumbnail <- snippet.thumbnails.medium.url TODO dont set thumbnail yet, i have to find a way to grab the pic binary from the url and store it

        next_token = False
        part_request = partial(youtube.playlistItems().list, part='contentDetails', playlistId=pl['id'], maxResults=50)

        while True:
            pl_request = part_request(pageToken=next_token) if next_token else part_request()
            pl_response = pl_request.execute()
            vid_ids = [item['contentDetails']['videoId'] for item in pl_response['items']]

            vid_request = youtube.videos().list(
                part='snippet,contentDetails',
                id=','.join(vid_ids)
            )

            logger.debug('requesting videos...', kind='regular')
            vid_response = vid_request.execute()
            self.insert_data(cursor, pl, vid_response['items'])

            next_token = pl_response.get('nextPageToken')
            if not next_token:
                break

    def insert_data(self, cursor, pl, items):
        """Insert video data into "Videos" and "MetaRaw". If an entry with that `apvid` (video id inside youtube) already exists
        it updates the `playlist` column to also include the one where the video was found in, this is because a video can be
        in several playlists.
        :param cursor: postgres cursor
        :param pl: playlist to store videos from
        :param items: api video objects
        """
        for item in items:
            snp = item['snippet']
            cdt = item['contentDetails']
            try:
                cursor.execute(
                    ''' INSERT INTO "Videos" as vid (name, playlist, apvid, duration)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (apvid) DO UPDATE
                            SET playlist = CASE
                                WHEN NOT vid.playlist @> excluded.playlist THEN array_cat(vid.playlist,excluded.playlist)
                                ELSE vid.playlist
                                END
                        RETURNING id
                    ''',
                    (snp['title'], pl['name'], item['id'], cdt['duration'])
                )
            except psycopg.errors.Error:
                raise Exception('error')
            else:  # the insertion succeded which means it either created a new entry or updated the `playlist` on an existing one
                vid_id = cursor.fetchone()  # grab the returned auto-gen id
                cursor.execute(
                    ''' INSERT INTO "MetaRaw" (id, title, description, tags, upload_date, channel)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (vid_id) DO NOTHING
                    ''',
                    (vid_id, snp['title'], snp['description'], snp['tags'], snp['publishedAt'], snp['channelTitle'])
                )
