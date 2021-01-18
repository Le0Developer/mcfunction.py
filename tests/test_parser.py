
import pytest

from mcfunction.exceptions import ParserException
from mcfunction.parser import parse_command


def test_parse_command():
    command = parse_command('help')

    assert command.command == 'help'

    with pytest.raises(ParserException, match='unknown command .*'):
        parse_command('this-command-does-not-exist')
