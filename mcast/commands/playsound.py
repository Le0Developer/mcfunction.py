
from dataclasses import dataclass

from . import Command, ParsedCommand, Parser
from ..nodes import (
    DoubleNode, EntityNode, NamespaceIDNode, PositionNode, RawNode
)
from ..parser_types import Double, Entity, NamespaceID, Position, Union


@dataclass()
class ParsedPlaysoundCommand(ParsedCommand):
    command: str

    sound: NamespaceIDNode
    source: RawNode
    target: EntityNode

    position: PositionNode = None
    volume: DoubleNode = None
    pitch: DoubleNode = None
    minimum_volume: DoubleNode = None

    def __str__(self):
        base = f'{self.command} {self.sound} {self.source} {self.target}'
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

# playsound <sound> <source> <targets> [<pos>] [<volume>] [<pitch>]
#   [<minVolume>]
#  - playsound <sound> <source> <targets> <pos> <volume> <pitch> <minVolume>
playsound.add_variation(
    Parser(NamespaceID(), 'sound'),
    Parser(Union('master', 'music', 'record', 'weather', 'block', 'hostile',
                 'neutral', 'player', 'ambient', 'voice'), 'source'),
    Parser(Entity(), 'target'),
    Parser(Position(), 'position'),
    Parser(Double(), 'volume'),
    Parser(Double(), 'pitch'),
    Parser(Double(), 'minimum_volume'),
)
#  - playsound <sound> <source> <targets> <pos> <volume> <pitch>
playsound.add_variation(
    Parser(NamespaceID(), 'sound'),
    Parser(Union('master', 'music', 'record', 'weather', 'block', 'hostile',
                 'neutral', 'player', 'ambient', 'voice'), 'source'),
    Parser(Entity(), 'target'),
    Parser(Position(), 'position'),
    Parser(Double(), 'volume'),
    Parser(Double(), 'pitch'),
)
#  - playsound <sound> <source> <targets> <pos> <volume>
playsound.add_variation(
    Parser(NamespaceID(), 'sound'),
    Parser(Union('master', 'music', 'record', 'weather', 'block', 'hostile',
                 'neutral', 'player', 'ambient', 'voice'), 'source'),
    Parser(Entity(), 'target'),
    Parser(Position(), 'position'),
    Parser(Double(), 'volume'),
)
#  - playsound <sound> <source> <targets> <pos>
playsound.add_variation(
    Parser(NamespaceID(), 'sound'),
    Parser(Union('master', 'music', 'record', 'weather', 'block', 'hostile',
                 'neutral', 'player', 'ambient', 'voice'), 'source'),
    Parser(Entity(), 'target'),
    Parser(Position(), 'position'),
)
#  - playsound <sound> <source> <targets>
playsound.add_variation(
    Parser(NamespaceID(), 'sound'),
    Parser(Union('master', 'music', 'record', 'weather', 'block', 'hostile',
                 'neutral', 'player', 'ambient', 'voice'), 'source'),
    Parser(Entity(), 'target'),
)
