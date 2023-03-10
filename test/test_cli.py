import os.path

from definitions import PROJECT_ROOT
import cli
from cli import cli as cli_app
from unittest import TestCase
from unittest.mock import patch, MagicMock
from click.testing import CliRunner

class TestCLI(TestCase):

    def test_integral_cli(self):
        """Test multiple cli commands and their impact on each other, simulating a typical use case.
        """
        runner = CliRunner()
        # ...

    # TODO dont call setup without first backing up the `.env` file. Or make the cli read the file name from a module variable and patch that for the tests
    def test_setup(self):
        runner = CliRunner()
        inp_1 = 'blablabla'
        inp_2 = 'N'
        res = runner.invoke(cli_app, ['setup'], input='\n'.join([inp_1, inp_2]))
        env = open(os.path.join(PROJECT_ROOT, '.env'), 'rt', encoding='utf-8')
        assert env.readline() == 'DEV_KEY=%s' % inp_1
        env.close()
        assert res.exit_code == 0
        assert 'setup complete' in res.output

    @patch("cli.Savior")
    def test_add_playlist(self, MockSavior):
        m_savior = MockSavior()
        cli.savior = m_savior
        # TODO change method behavior
        m_savior.add_playlist = MagicMock(...)
        runner = CliRunner()
        res = runner.invoke(cli_app, ['add-playlist', 'SMASH', 'https://youtube.com/playlist?list=PL_hXMzbIDwY6JUkTmCCoL1BwVIDHQpnRb'])
        assert res.exit_code == 0
        assert 'playlist id is PL_hXMzbIDwY6JUkTmCCoL1BwVIDHQpnRb' in res.output

    def test_save_all(self):
        runner = CliRunner()
        res = runner.invoke(cli_app, ['save'])
        assert res.exit_code == 0
        assert 'saving all playlists' in res.output

    def test_save_some(self):
        runner = CliRunner()
        res = runner.invoke(cli_app, ['save', '-p', 'SMASH', 'music'])
        assert res.exit_code == 0
        assert 'saving specified playlists' in res.output
