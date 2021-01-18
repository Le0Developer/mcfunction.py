
from dataclasses import dataclass

from . import Command, ParsedCommand, Parser
from ..nodes import RawNode
from ..parser_types import Any


@dataclass()
class ParsedLocateCommand(ParsedCommand):
    command: str

    structure: RawNode

    def __str__(self):
        return f'{self.command} {self.structure}'


locate = Command('locate', parsed=ParsedLocateCommand)

# locate <structure>
locate.add_variation(
    Parser(Any(), 'structure'),
)
