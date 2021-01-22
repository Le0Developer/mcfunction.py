
from dataclasses import dataclass

from .. import Command, ParsedCommand, Parser
from ...nodes import RawNode
from ...parser_types import Any


@dataclass()
class ParsedHelpCommand(ParsedCommand):
    command: str

    cmd: RawNode = None

    def __str__(self):
        if self.cmd is not None:
            return f'{self.command} {self.cmd}'
        return self.command


help = Command('help', parsed=ParsedHelpCommand, oplevel=0)

# help
help.add_variation()

# help <command>
help.add_variation(
    Parser(Any(), 'cmd'),
)
