import sys, os, psycopg, re

from loguru import logger

def grab_pls():
    with psycopg.connect('dbname=playlist user=bashiron') as conn:
        with conn.cursor() as cursor:
            grab_titles(smash, cursor, 'smash')
            logger.success('smash titles stored', kind='playlist')
            grab_titles(music, cursor, 'music')
            logger.success('music titles stored', kind='playlist')
            grab_titles(favs, cursor, 'favs')
            logger.success('favs titles stored', kind='playlist')


def grab_titles(playlist, cursor, pl_type):
    for dir_entry in playlist:
        logger.info('<{}>', dir_entry.name, kind='directory')
        with open(dir_entry.path, 'rt', encoding='utf-8') as file:
            while True:
                line = file.readline()
                if line == "":
                    break
                line = clean_line(line)
                try:
                    logger.info('<{}>', line, kind='display')
                    logger.debug('attempting video insert...', kind='regular')
                    insert_video(cursor, line, pl_type)
                except psycopg.errors.Error:
                    raise Exception("error")
                else:
                    ret = cursor.fetchone()
                    if ret is not None:  # when there was no conflict/duplicate and a new entry was added
                        logger.success('video entry added', kind='regular')
                        insert_data(cursor, ret[0], line, pl_type)
                    else:
                        logger.warning('duplicate found, no entry added', kind='regular')


def insert_video(cursor, line, pl_type):
    cursor.execute(
        'INSERT INTO "Videos" (name, playlist) VALUES (%s, %s) ON CONFLICT (name) DO NOTHING RETURNING id',
        (line, pl_type))


def insert_data(cursor, v_id, line, pl_type):
    if pl_type != 'favs':
        cursor.execute(
            'INSERT INTO "MetaOST" (vid_id, title) VALUES (%s, %s)',
            (v_id, line)
        )
    cursor.execute(
        'INSERT INTO "MetaRaw" (vid_id, title) VALUES (%s, %s)',
        (v_id, line)
    )
    logger.success('extra data entries added', kind='regular')


def clean_line(line):
    return re.search(r" (.*)", line).group(1)

# LOG FILTERS

def reg_filter(record):
    return record['extra']['kind'] == 'regular'

def dir_filter(record):
    return record['extra']['kind'] == 'directory'

def pl_filter(record):
    return record['extra']['kind'] == 'playlist'

def disp_filter(record):
    return record['extra']['kind'] == 'display'


if __name__ == '__main__':
    # configure loggers
    logger.remove()
    logger.add(sys.stderr, format='<w><green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level></w>', filter=reg_filter, level=0)
    logger.add(sys.stderr, format='<w><green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <y>{message}</y></w>', filter=dir_filter, level=0)
    logger.add(sys.stderr, format='<w><green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <m>{message}</m></w>', filter=pl_filter, level=0)
    logger.add(sys.stderr, format='<w><green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <fg #6C66BA>{message}</fg #6C66BA></w>', filter=disp_filter, level=0)

    items = os.scandir('/home/bashiron/playlists/generated')
    files = filter(lambda i: i.is_file(), items)
    # alternative
    # files = [i for i in its if i.is_file()]
    smash, music, favs = [], [], []
    for f in files:
        if 'smash' in f.name:
            smash.append(f)
        elif 'music' in f.name:
            music.append(f)
        elif 'favorites' in f.name:
            favs.append(f)

    grab_pls()
