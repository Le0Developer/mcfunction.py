
from dataclasses import dataclass

from .. import Command, ParsedCommand, Parser
from ...nodes import PositionNode
from ...parser_types import Position


@dataclass()
class ParsedSetworldspawnCommand(ParsedCommand):
    command: str

    position: PositionNode = None

    def __str__(self):
        if self.position is not None:
            return f'{self.command} {self.position}'
        return self.command


setworldspawn = Command('setworldspawn', parsed=ParsedSetworldspawnCommand)

# setworldspawn [<pos>]
#  - setworldspawn <pos>
setworldspawn.add_variation(
    Parser(Position(), 'position'),
)
#  - setworldspawn
setworldspawn.add_variation()
