
from dataclasses import dataclass

from .. import Command, ParsedCommand, Parser
from ...nodes import EntityNode, NamespaceIDNode, RawNode
from ...parser_types import Entity, NamespaceID, Union


@dataclass()
class ParsedStopsoundCommand(ParsedCommand):
    command: str

    target: EntityNode

    source: RawNode = None
    sound: NamespaceIDNode = None

    def __str__(self):
        base = f'{self.command} {self.target}'
        if self.source is not None:
            if self.sound is not None:
                return f'{base} {self.source} {self.sound}'
            return f'{base} {self.source}'
        return base


stopsound = Command('stopsound', parsed=ParsedStopsoundCommand)

# stopsound <targets> [<source>] [<sound>]
#  - stopsound <targets> <source> <sound>
stopsound.add_variation(
    Parser(Entity(), 'target'),
    Parser(Union('master', 'music', 'record', 'weather', 'block', 'hostile',
                 'neutral', 'player', 'ambient', 'voice', '*'), 'source'),
    Parser(NamespaceID(), 'sound'),
)
#  - stopsound <targets> <source>
stopsound.add_variation(
    Parser(Entity(), 'target'),
    Parser(Union('master', 'music', 'record', 'weather', 'block', 'hostile',
                 'neutral', 'player', 'ambient', 'voice', '*'), 'source'),
)
#  - stopsound <targets>
stopsound.add_variation(
    Parser(Entity(), 'target'),
)
