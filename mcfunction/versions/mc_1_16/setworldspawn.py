
from dataclasses import dataclass

from .. import Command, ParsedCommand, Parser
from ...nodes import PositionNode, RotationNode
from ...parser_types import Position, Rotation


@dataclass()
class ParsedSetworldspawnCommand(ParsedCommand):
    command: str

    position: PositionNode = None
    angle: RotationNode = None

    def __str__(self):
        if self.position is not None:
            if self.angle is not None:
                return f'{self.command} {self.position} {self.angle}'
            return f'{self.command} {self.position}'
        return self.command


setworldspawn = Command('setworldspawn', parsed=ParsedSetworldspawnCommand)

# setworldspawn [<pos>] [<angle>]
#  - setworldspawn <pos> <angle>
setworldspawn.add_variation(
    Parser(Position(), 'position'),
    Parser(Rotation(), 'angle')
)
#  - setworldspawn <pos>
setworldspawn.add_variation(
    Parser(Position(), 'position'),
)
#  - setworldspawn
setworldspawn.add_variation()
