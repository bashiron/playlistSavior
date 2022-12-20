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

def save(pl):
    next_token = False
    part_request = partial(youtube.playlistItems().list, part='contentDetails', playlistId=pl['id'], maxResults=50)

    while True:
        # playlist list items request
        pl_request = part_request(pageToken=next_token) if next_token else part_request()
        pl_response = pl_request.execute()
        vid_ids = [item['contentDetails']['videoId'] for item in pl_response['items']]

        # list videos request
        vid_request = youtube.videos().list(
            part='snippet,contentDetails',
            id=','.join(vid_ids)
        )

        logger.debug('requesting videos...', kind='regular')
        vid_response = vid_request.execute()
        # relation -> (db_id, item)
        relation = map(lambda x: (get_db_id(x), x), vid_response['items'])
        # remove tuples with no db_id
        relation = list(filter(lambda x: x[0] is not None, relation))
        insert_data(relation)
        next_token = pl_response.get('nextPageToken')
        if not next_token:
            break

def get_db_id(item):
    cursor.execute('SELECT (vid_id) FROM "MetaRaw" WHERE title = %s', (item['snippet']['title'],))
    try:
        db_id = cursor.fetchone()[0]
    except TypeError:
        db_id = None
    return db_id

def insert_data(relation):
    for db_id, item in relation:
        snp = improve_snippet(item['snippet'])
        cdt = item['contentDetails']
        cursor.execute(
            ''' UPDATE "Videos"
                SET apvid = %s,
                    duration = %s
                WHERE id = %s
            ''',
            (item['id'], cdt['duration'], db_id)
        )
        cursor.execute(
            ''' UPDATE "MetaRaw"
                SET description = %s,
                    tags = %s,
                    upload_date = %s,
                    channel = %s
                WHERE vid_id = %s
            ''',
            (snp['description'], snp['tags'], snp['publishedAt'], snp['channelTitle'], db_id)
        )

def improve_snippet(snp):
    try:
        fixed_tags = snp['tags']
    except KeyError:
        fixed_tags = ['<none>']
    snp['tags'] = ', '.join(fixed_tags)[0:499]
    return snp


if __name__ == '__main__':
    with psycopg.connect('dbname=playlist user=bashiron') as conn:
        with conn.cursor() as cursor:
            save(SMASH)
            save(MUSIC)
            save(FAVS)
