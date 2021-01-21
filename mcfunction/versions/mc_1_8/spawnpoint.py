
from dataclasses import dataclass

from .. import Command, ParsedCommand, Parser
from ...nodes import EntityNode, PositionNode
from ...parser_types import Entity, Position


@dataclass()
class ParsedSpawnpointCommand(ParsedCommand):
    command: str

    target: EntityNode = None
    position: PositionNode = None

    def __str__(self):
        if self.target is not None:
            if self.position is not None:
                return f'{self.command} {self.target} {self.position}'
            return f'{self.command} {self.target}'
        return self.command


spawnpoint = Command('spawnpoint', parsed=ParsedSpawnpointCommand)

# spawnpoint [<targets>] [<pos>]
spawnpoint.add_variation(
    Parser(Entity(), 'target'),
    Parser(Position(), 'position'),
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
