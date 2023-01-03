import cli
from unittest import TestCase
from click.testing import CliRunner

class TestCLI(TestCase):

    def test_setup(self):
        runner = CliRunner()
        res = runner.invoke(cli.setup)
        assert res.exit_code == 0
        assert res.output == 'something'
