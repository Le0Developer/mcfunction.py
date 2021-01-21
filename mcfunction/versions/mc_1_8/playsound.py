
from dataclasses import dataclass

from .. import Command, ParsedCommand, Parser
from ...nodes import DoubleNode, EntityNode, NamespaceIDNode, PositionNode
from ...parser_types import Double, Entity, NamespaceID, Position


@dataclass()
class ParsedPlaysoundCommand(ParsedCommand):
    command: str

    sound: NamespaceIDNode
    target: EntityNode

    position: PositionNode = None
    volume: DoubleNode = None
    pitch: DoubleNode = None
    minimum_volume: DoubleNode = None

    def __str__(self):
        base = f'{self.command} {self.sound} {self.target}'
        if self.position is None:
            return base
        if self.volume is None:
            return f'{base} {self.position}'
        if self.pitch is None:
            return f'{base} {self.position} {self.volume}'
        if self.minimum_volume is None:
            return f'{base} {self.position} {self.volume} {self.pitch}'
        return f'{base} {self.position} {self.volume} {self.pitch} ' \
               f'{self.minimum_volume}'


playsound = Command('playsound', parsed=ParsedPlaysoundCommand)

# playsound <sound> <targets> [<pos>] [<volume>] [<pitch>] [<minVolume>]
#  - playsound <sound> <targets> <pos> <volume> <pitch> <minVolume>
playsound.add_variation(
    Parser(NamespaceID(), 'sound'),
    Parser(Entity(), 'target'),
    Parser(Position(), 'position'),
    Parser(Double(), 'volume'),
    Parser(Double(), 'pitch'),
    Parser(Double(), 'minimum_volume'),
)
#  - playsound <sound> <targets> <pos> <volume> <pitch>
playsound.add_variation(
    Parser(NamespaceID(), 'sound'),
    Parser(Entity(), 'target'),
    Parser(Position(), 'position'),
    Parser(Double(), 'volume'),
    Parser(Double(), 'pitch'),
)
#  - playsound <sound> <targets> <pos> <volume>
playsound.add_variation(
    Parser(NamespaceID(), 'sound'),
    Parser(Entity(), 'target'),
    Parser(Position(), 'position'),
    Parser(Double(), 'volume'),
)
#  - playsound <sound> <targets> <pos>
playsound.add_variation(
    Parser(NamespaceID(), 'sound'),
    Parser(Entity(), 'target'),
    Parser(Position(), 'position'),
)
#  - playsound <sound> <targets>
playsound.add_variation(
    Parser(NamespaceID(), 'sound'),
    Parser(Entity(), 'target'),
)
