import os, psycopg, re
from time import sleep


def grab_pls():
    with psycopg.connect('dbname=playlist user=bashiron') as conn:
        with conn.cursor() as cursor:
            grab_titles(smash, cursor, 'smash')
            print('--smash titles stored--')
            sleep(3)
            grab_titles(music, cursor, 'music')
            print('--music titles stored--')
            sleep(3)
            grab_titles(favs, cursor, 'favs')
            print('favs titles stored')


def grab_titles(playlist, cursor, pl_type):
    for dir_entry in playlist:
        print(f'<{dir_entry.name}>')
        with open(dir_entry.path, 'rt', encoding='utf-8') as file:
            while True:
                line = file.readline()
                if line == "":
                    break
                line = clean_line(line)
                try:
                    print(f'<{line}>')
                    print('--- attempting video insert...')
                    insert_video(cursor, line, pl_type)
                except psycopg.errors.Error:
                    raise Exception("error")
                else:
                    ret = cursor.fetchone()
                    if ret is not None:  # when there was no conflict/duplicate and a new entry was added
                        print('--- video entry added')
                        insert_data(cursor, ret[0], line, pl_type)
                    else:
                        print('--- duplicate found, no entry added')
                sleep(0.7)


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
    print('--- extra data entries added')


def clean_line(line):
    return re.search(r" (.*)", line).group(1)


if __name__ == '__main__':
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
