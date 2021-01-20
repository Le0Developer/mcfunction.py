
from dataclasses import dataclass
import typing as t

from .. import Command, ParsedCommand, Parser
from ...exceptions import ConstructionException
from ...nodes import EntityNode, PositionNode, RawNode, RotationNode
from ...parser_types import Entity, Literal, Position, Union, Rotation


@dataclass()
class ParsedTpCommand(ParsedCommand):
    command: str

    destination: t.Union[EntityNode, PositionNode] = None
    target: EntityNode = None
    rotation: RotationNode = None

    def __str__(self):
        if self.target is None:
            if self.rotation is None:
                return f'{self.command} {self.destination}'
            return f'{self.command} {self.destination} {self.rotation}'

        if self.rotation is None:
            return f'{self.command} {self.target} {self.destination}'
        return f'{self.command} {self.target} {self.destination} ' \
               f'{self.rotation}'


tp = Command('tp', parsed=ParsedTpCommand)

# tp <destination player>
tp.add_variation(
    Parser(Entity(), 'destination')
)

# tp <x> <y> <z> [<yaw> <pitch>]
#  - tp <x> <y> <z> (<yaw> <pitch>)
tp.add_variation(
    Parser(Position(), 'destination'),
    Parser(Rotation(), 'rotation')
)
#  - tp <x> <y> <z>
tp.add_variation(
    Parser(Position(), 'destination')
)

# tp <target player> <destination player>
tp.add_variation(
    Parser(Entity(), 'target'),
    Parser(Entity(), 'destination')
)
# tp <target player> <x> <y> <z> [<yaw> <pitch>]
#  - tp <target player> <x> <y> <z> (<yaw> <pitch>)
tp.add_variation(
    Parser(Entity(), 'target'),
    Parser(Position(), 'destination'),
    Parser(Rotation(), 'rotation')
)
#  - tp <target player> <x> <y> <z>
tp.add_variation(
    Parser(Entity(), 'target'),
    Parser(Position(), 'destination')
)
