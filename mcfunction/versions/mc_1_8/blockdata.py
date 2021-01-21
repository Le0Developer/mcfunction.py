
from dataclasses import dataclass

from .. import Command, ParsedCommand, Parser
from ...nodes import PositionNode, RawNode
from ...parser_types import Any, Position


@dataclass()
class ParsedBlockdataCommand(ParsedCommand):
    command: str

    position: PositionNode
    data: RawNode

    def __str__(self):
        return f'{self.command} {self.position} {self.data}'


blockdata = Command('blockdata', parsed=ParsedBlockdataCommand)

# blockdata <position> <data>
blockdata.add_variation(
    Parser(Position(), 'position'),
    Parser(Any(), 'data'),
)
