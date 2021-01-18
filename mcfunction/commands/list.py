
from dataclasses import dataclass

from . import Command, ParsedCommand, Parser
from ..nodes import RawNode
from ..parser_types import Literal


@dataclass()
class ParsedListCommand(ParsedCommand):
    command: str

    uuids: RawNode = None

    def __str__(self):
        if self.uuids is not None:
            return f'{self.command} {self.uuids}'
        return self.command


list = Command('list', parsed=ParsedListCommand)

# list uuids
list.add_variation(
    Parser(Literal('uuids'), 'uuids'),
)
# list
list.add_variation()
