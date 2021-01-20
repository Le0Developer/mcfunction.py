
from dataclasses import dataclass
import typing as t

from .. import Command, ParsedCommand, Parser
from ...exceptions import ConstructionException
from ...nodes import EntityNode, PositionNode, RawNode, RotationNode
from ...parser_types import Entity, Literal, Position, Union, Rotation


@dataclass()
class ParsedTeleportCommand(ParsedCommand):
    command: str

    destination: t.Union[EntityNode, PositionNode] = None
    target: EntityNode = None
    rotation: RotationNode = None
    facing: t.Union[EntityNode, PositionNode] = None
    anchor: RawNode = None

    def __str__(self):
        if self.target is None:
            return f'{self.command} {self.destination}'
        base = f'{self.command} {self.target} {self.destination}'
        if self.rotation is not None:
            if not isinstance(self.destination, PositionNode):
                raise ConstructionException(
                    'conflicting information; rotation without position'
                )
            return f'{base} {self.rotation}'
        if self.facing is not None:
            if isinstance(self.facing, EntityNode):
                # was unable to think of names for 'facing' and 'entity' part
                command = f'{base} facing entity {self.facing}'
                if self.anchor is not None:
                    return f'{command} {self.anchor}'
                return command
            else:
                return f'{base} facing {self.facing}'
        return base


teleport = Command('teleport', aliases=['tp'], parsed=ParsedTeleportCommand)

# teleport <destination>
teleport.add_variation(
    Parser(Entity(), 'destination'),
)
# teleport <location>
teleport.add_variation(
    Parser(Position(), 'destination')
)
# teleport <targets> <destination>
teleport.add_variation(
    Parser(Entity(), 'target'),
    Parser(Entity(), 'destination'),
)
# teleport <targets> <location> [<rotation>]
#  - teleport <targets> <location> <rotation>
teleport.add_variation(
    Parser(Entity(), 'target'),
    Parser(Position(), 'destination'),
    Parser(Rotation(), 'rotation'),
)
#  - teleport <targets> <location>
teleport.add_variation(
    Parser(Entity(), 'target'),
    Parser(Position(), 'destination'),
)
# teleport <targets> <location> facing <facingLocation>
teleport.add_variation(
    Parser(Entity(), 'target'),
    Parser(Position(), 'destination'),
    Parser(Literal('facing'), None),
    Parser(Position(), 'facing'),
)
# teleport <targets> <location> facing entity <facingEntity> [<facingAnchor>]
#  - teleport <targets> <location> facing entity <facingEntity> <facingAnchor>
teleport.add_variation(
    Parser(Entity(), 'target'),
    Parser(Position(), 'destination'),
    Parser(Literal('facing'), None),
    Parser(Literal('entity'), None),
    Parser(Entity(), 'facing'),
    Parser(Union('eyes', 'feet'), 'anchor'),
)
#  - teleport <targets> <location> facing entity <facingEntity>
teleport.add_variation(
    Parser(Entity(), 'target'),
    Parser(Position(), 'destination'),
    Parser(Literal('facing'), None),
    Parser(Literal('entity'), None),
    Parser(Entity(), 'facing'),
)
