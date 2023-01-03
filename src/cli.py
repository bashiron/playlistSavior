import click

from src.playlist_savior import Savior

@click.group()
def cli():
    pass

@cli.command()
def setup():
    click.echo('Let''s start setting up')
    api_key = click.prompt('Input your personal Youtube API key')
    with open('/home/bashiron/bashi/projects/youtubePlaylistSavior/.env', 'wt', encoding='utf-8') as env:
        env.write('DEV_KEY=%s' % api_key)
    # ...

    if click.confirm('Do you want to add some playlists now?'):
        # proceed with add_playlist function
        # i think i can use click.Context.invoke() - https://click.palletsprojects.com/en/8.1.x/advanced/#invoking-other-commands
        pass

@cli.command()
@click.argument('name', nargs=1)
@click.argument('url', nargs=1)
def add_playlist(name, url):
    print(f'save playlist {name} with url {url}')









# ARGPARSE CODE (DEPRECATED)
# def extract_pl_id(url):
#     return re.search(r"(?<==)(.*)", url).group(1)

# savior = Savior()
# parser = argparse.ArgumentParser(prog='Playlist Savior', description='Save playlists')
# parser.add_argument('-n', '--new', action='store_true')
# parser.add_argument('--save', dest='save', action='store_const', const=savior.init_and_save,
#                     help='save playlists to database')
# parser.add_argument('playlists', type=str, nargs='+', help='list of playlist urls')
#
# args = parser.parse_args()
#
# if args.new:
#     print('we will create a new playlist object')
#     pl_name = input('insert playlist name: ')
#
# elif args.save:
#     for pl in args.playlists:
#         args.save(extract_pl_id(pl))
