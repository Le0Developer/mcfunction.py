
from dataclasses import dataclass

from . import Command, ParsedCommand, Parser
from ..nodes import EntityNode, PositionNode, RotationNode
from ..parser_types import Entity, Position, Rotation


@dataclass()
class ParsedSpawnpointCommand(ParsedCommand):
    command: str

    target: EntityNode = None
    position: PositionNode = None
    angle: RotationNode = None

    def __str__(self):
        if self.target is not None:
            if self.position is not None:
                if self.angle is not None:
                    return f'{self.command} {self.target} {self.position}' \
                           f' {self.angle}'
                return f'{self.command} {self.target} {self.position}'
            return f'{self.command} {self.target}'
        return self.command


spawnpoint = Command('spawnpoint', parsed=ParsedSpawnpointCommand)

# spawnpoint [<targets>] [<pos>] [<angle>]
#  - spawnpoint <targets> <pos> <angle>
spawnpoint.add_variation(
    Parser(Entity(), 'target'),
    Parser(Position(), 'position'),
    Parser(Rotation(), 'angle')
)
#  - spawnpoint <targets> <pos>
spawnpoint.add_variation(
    Parser(Entity(), 'target'),
    Parser(Position(), 'position'),
)
#  - spawnpoint <targets>
spawnpoint.add_variation(
    Parser(Entity(), 'target'),
)
#  - spawnpoint
spawnpoint.add_variation()
