
from .commands import Command, command_lookup
from .exceptions import ParserException
from .util import tokenize


def parse_command(command: str):
    parts = list(tokenize(command, ' '))

    if parts[0] not in command_lookup:
        raise ParserException(f'unknown command {parts[0]}')
    cmd = command_lookup[parts[0]]  # type: Command

    return cmd.parse(command)
