
from dataclasses import dataclass

from .. import Command, ParsedCommand, Parser
from ...nodes import EntityNode, PositionNode, RotationNode
from ...parser_types import Entity, Position, Rotation


@dataclass()
class ParsedTeleportCommand(ParsedCommand):
    command: str

    target: EntityNode
    position: PositionNode = None
    rotation: RotationNode = None

    def __str__(self):
        base = f'{self.command} {self.target}'
        if self.position is not None:
            if self.rotation is not None:
                return f'{base} {self.position} {self.rotation}'
            return f'{base} {self.position}'
        return base


teleport = Command('teleport', parsed=ParsedTeleportCommand)

# teleport <entity> [<x> <y> <z>] [<y-rot> <x-rot>]
# - teleport <entity> (<x> <y> <z>) (<y-rot> <x-rot>)
teleport.add_variation(
    Parser(Entity(), 'target'),
    Parser(Position(), 'position'),
    Parser(Rotation(), 'rotation')
)
# - teleport <entity> (<x> <y> <z>)
teleport.add_variation(
    Parser(Entity(), 'target'),
    Parser(Position(), 'position')
)
# - teleport <entity>
teleport.add_variation(
    Parser(Entity(), 'target'),
)
