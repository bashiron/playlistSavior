from cli import cli
from unittest import TestCase
from click.testing import CliRunner

class TestCLI(TestCase):

    # TODO dont call setup without first backing up the `.env` file
    def test_setup(self):
        runner = CliRunner()
        inp_1 = 'blablabla'
        inp_2 = 'N'
        res = runner.invoke(cli, ['setup'], input='\n'.join([inp_1, inp_2]))
        assert res.exit_code == 0
        assert 'setup complete' in res.output

    def test_add_playlist(self):
        runner = CliRunner()
        res = runner.invoke(cli, ['add-playlist', 'SMASH', 'https://youtube.com/playlist?list=PL_hXMzbIDwY6JUkTmCCoL1BwVIDHQpnRb'])
        assert res.exit_code == 0
        assert 'playlist id is PL_hXMzbIDwY6JUkTmCCoL1BwVIDHQpnRb' in res.output

    def test_save_all(self):
        runner = CliRunner()
        res = runner.invoke(cli, ['save'])
        assert res.exit_code == 0
        assert 'saving all playlists' in res.output

    def test_save_some(self):
        runner = CliRunner()
        res = runner.invoke(cli, ['save', '-p', 'SMASH', 'music'])
        assert res.exit_code == 0
        assert 'saving specified playlists' in res.output
