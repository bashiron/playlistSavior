import os
import sys, psycopg
import playlist_savior
from loguru import logger
from dotenv import load_dotenv
from googleapiclient.discovery import build


if __name__ == '__main__':

    api_key = os.environ['DEV_KEY']

    youtube = build('youtube', 'v3', developerKey=api_key)

    with psycopg.connect('dbname=playlist user=bashiron') as conn:
        with conn.cursor() as cursor:
            pass