import os, psycopg
from functools import partial
from collections.abc import Callable

from googleapiclient.discovery import build
from dotenv import load_dotenv

from src.log_prep import *

load_dotenv()
api_key = os.environ["DEV_KEY"]

youtube = build('youtube', 'v3', developerKey=api_key)

conn_conf = {'dbname': 'playlist', 'user': 'bashiron'}

class Savior:

    def run_db_op(self, op: Callable[[psycopg.Cursor], None]):
        """Run a Savior database operation by first initializing the connection vars and then passing them to the op.

        Examples
        -----
        Run the `save` function:

        >>> Savior.run_db_op(partial(Savior.save, ['smash', 'music']))
        None

        Parameters
        -----
        op
            Database operation to execute. Partial function with every argument except 'cursor' already defined.

        """
        logger.debug('connecting to postgres...', kind='regular')
        with psycopg.connect("dbname={} user={}".format(conn_conf['dbname'], conn_conf['user'])) as conn:
            with conn.cursor() as cursor:
                op(cursor)

    # def init_and_save(self, pl):
    #     logger.debug('connecting to postgres...', kind='regular')
    #     with psycopg.connect("dbname={} user={}".format(conn_conf['dbname'], conn_conf['user'])) as conn:
    #         with conn.cursor() as cursor:
    #             self.save(pl, cursor)

    def save(self, pls, cursor):
        """Perform the main save operation. Naturally saves every playlist in the database but has the option to save only
        the ones specified by the `pls` argument.

        Parameters
        -----
        pls : `list` of `str`
            Playlists to be saved and ONLY these will be saved. Empty list to save every playlist in db.
        cursor : `psycopg.Cursor`
            Postgres cursor.
        """
        match pls:
            case []:
                # save everything
                fetched_pls = cursor.execute('SELECT * FROM "Playlists"').fetchall()
                fetched_pls = list(map(lambda t: {'name': t[0], 'id': t[1]}, fetched_pls))
                for pl in fetched_pls:
                    self.save_playlist(pl, cursor)

            case _:
                # save only listed playlists
                fetched_pls = cursor.execute('SELECT * FROM "Playlists" WHERE name = ANY(%s)', [pls]).fetchall()
                fetched_pls = list(map(lambda t: {'name': t[0], 'id': t[1]}, fetched_pls))
                for pl in fetched_pls:
                    self.save_playlist(pl, cursor)

    def save_playlist(self, pl, cursor):
        """Fetch video data from playlist and store in database.

        Parameters
        -----
        pl : `dict`
            Playlist to store video data from.
        cursor : `psycopg.Cursor`
            Postgres cursor.
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

        logger.info('received request to save {} playlist', pl['name'], kind='playlist')
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
            self.insert_data(pl, vid_response['items'], cursor)

            next_token = pl_response.get('nextPageToken')
            page += 1
            if not next_token:
                break

    def insert_data(self, pl, items, cursor):
        """Insert video data into "Videos" and "MetaRaw". If an entry with that `apvid` (video id inside youtube) already exists
        it updates the `playlist` column to also include the one where the video was found in, this is because a video can be
        in several playlists.

        Parameters
        -----
        pl : `dict`
            Playlist to store videos from.
        items : `dict`
            Api video objects.
        cursor : `psycopg.Cursor`
            Postgres cursor.
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

    def add_playlist(self, pl, cursor):
        """Takes playlist (dict with name and id) and saves it to database
        """
        cursor.execute('INSERT INTO "Playlists" (name, aplid) VALUES (%s, %s)', (pl['name'], pl['id']))

    def add_multi_playlist(self, pls: list[tuple], cursor: psycopg.Cursor):
        """Takes list of playlists and saves them to database
        """
        cursor.executemany(
            ''' INSERT INTO "Playlists" (name, aplid)
                VALUES (%s, %s)
            ''',
            pls
        )
