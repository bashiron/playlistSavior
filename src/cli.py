import click, re
from functools import partial

from src.playlist_savior import Savior

savior = Savior()

@click.group()
def cli():
    pass

@cli.command()
def setup():
    """Perform first-time setup. You will be asked for data necessary to operate
    """
    click.echo("Let's start setting up")
    api_key = click.prompt('Input your personal Youtube API key')
    with open('/home/bashiron/bashi/projects/youtubePlaylistSavior/.env', 'wt', encoding='utf-8') as env:
        env.write('DEV_KEY=%s' % api_key)
    # ...

    if click.confirm('Do you want to add some playlists now?'):
        # proceed with add_playlist function
        # i think i can use click.Context.invoke() - https://click.palletsprojects.com/en/8.1.x/advanced/#invoking-other-commands
        pass
    else:
        click.echo('setup complete')

@cli.command()
@click.argument('name', nargs=1)
@click.argument('url', nargs=1)
def add_playlist(name, url):
    """Add a playlist to the database by providing a name and a url
    """
    pl_id = re.search(r"(?<==)(.*)", url).group(1)
    savior.run_db_op(partial(savior.add_playlist, pl={'name': name, 'id': pl_id}))
    click.echo(f'playlist id is {pl_id}')

@cli.command()
def multi_add_playlist():
    """Add multiple playlists to the database interactively
    """
    click.echo('''Started interactive playlist creation\nUse names that are easy to type and remember, it doesn't need to be
    the real playlist name on Youtube\nFor the URL just copy and paste the playlist URL as it shows on Youtube''')
    pls = []
    while True:
        name = click.prompt('Type the playlist name')
        url = click.prompt('Type the playlist URL')
        pl_id = re.search(r"(?<==)(.*)", url).group(1)
        pls.append((name, pl_id))
        if not click.confirm('Add more?', default=True):
            break
    savior.run_db_op(partial(savior.add_multi_playlist, pls))

@cli.command()
@click.option('-p', '--playlists', 'f_pls', is_flag=True, help='flag that indicates whether to save only specified playlists')
@click.argument('pls', type=str, nargs=-1)
def save(f_pls, pls):
    """Save all playlists's data or only the ones defined in the arguments\n
    The arguments should contain the playlists to save while ignoring others
    """
    click.echo('saving %s' % 'all playlists' if not f_pls else 'specified playlists')
    final_pls = list(pls) if f_pls else []
    savior.run_db_op(partial(savior.save, final_pls))
    # try:
    #     savior.run_db_op(partial(savior.save, final_pls))
    # except Exception as exc:
    #     click.echo('error in operation')
    #     raise exc
    # else:
    #     click.echo('operation successful')







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
