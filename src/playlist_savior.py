import os, psycopg
from functools import partial

from googleapiclient.discovery import build
from dotenv import load_dotenv

from src.log_prep import *

load_dotenv()
api_key = os.environ["DEV_KEY"]

youtube = build('youtube', 'v3', developerKey=api_key)

smash_id = 'PL_hXMzbIDwY6JUkTmCCoL1BwVIDHQpnRb'
music_id = 'PL_hXMzbIDwY4II8UXP93yd7n_HvcFg8rF'
favs_id = 'FLtpm7glO-bH0NlP2mxldq4g'

SMASH = {'name': 'smash', 'id': smash_id}
MUSIC = {'name': 'music', 'id': music_id}
FAVS = {'name': 'favs', 'id': favs_id}

conn_conf = {'dbname': 'playlist', 'user': 'bashiron'}

class Savior:

    def init_and_save(self, pl):
        logger.info('received request to save {} playlist', pl['name'], kind='playlist')
        logger.debug('connecting to postgres...', kind='regular')
        with psycopg.connect("dbname={} user={}".format(conn_conf['dbname'], conn_conf['user'])) as conn:
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
        page = 1
        part_request = partial(youtube.playlistItems().list, part='contentDetails', playlistId=pl['id'], maxResults=50)

        while True:
            pl_request = part_request(pageToken=next_token) if next_token else part_request()
            pl_response = pl_request.execute()
            vid_ids = [item['contentDetails']['videoId'] for item in pl_response['items']]

            vid_request = youtube.videos().list(
                part='snippet,contentDetails',
                id=','.join(vid_ids)
            )

            logger.debug('requesting raw video data... | page {}', page, kind='regular')
            vid_response = vid_request.execute()
            self.insert_data(cursor, pl, vid_response['items'])

            next_token = pl_response.get('nextPageToken')
            page += 1
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
            logger.info('<{}>', item['snippet']['title'], kind='display')
            snp = self.improve_snippet(item['snippet'])
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
                    (snp['title'], [pl['name']], item['id'], cdt['duration'])
                )
            except psycopg.errors.Error:
                raise Exception('error')
            else:  # the insertion succeded which means it either created a new entry or updated the `playlist` on an existing one
                vid_id = cursor.fetchone()[0]  # grab the returned auto-gen id
                cursor.execute(
                    ''' INSERT INTO "MetaRaw" (vid_id, title, description, tags, upload_date, channel)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (vid_id) DO NOTHING
                    ''',
                    (vid_id, snp['title'], snp['description'], snp['tags'], snp['publishedAt'], snp['channelTitle'])
                )

    def improve_snippet(self, snp):
        try:
            fixed_tags = snp['tags']
        except KeyError:
            fixed_tags = ['<none>']
        snp['tags'] = ', '.join(fixed_tags)[0:499]
        return snp

def add_playlist(pl):
    pass
