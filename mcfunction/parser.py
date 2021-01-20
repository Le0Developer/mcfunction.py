
import typing as t

from .versions import VERSIONS, Command, MinecraftVersion
from .exceptions import ParserException
from .mcfunction import McFunction
from .util import tokenize


def parse_command(command: str, version: MinecraftVersion = None):
    if version is None:
        version = VERSIONS[0]

    name = list(tokenize(command, ' '))[0]

    cmd = version.get_command(name)  # type: Command
    if cmd is None:
        raise ParserException(f'unknown command {name}')

    return cmd.parse(command)


def parse_mcfuntion(commands: t.List[str]) -> McFunction:
    return McFunction.parse(commands)
