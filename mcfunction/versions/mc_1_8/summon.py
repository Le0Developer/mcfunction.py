
from dataclasses import dataclass

from .. import Command, ParsedCommand, Parser
from ...nodes import NamespaceIDNode, PositionNode, RawNode
from ...parser_types import Any, NamespaceID, Position


@dataclass()
class ParsedSummonCommand(ParsedCommand):
    command: str

    entity: NamespaceIDNode

    position: PositionNode = None
    nbt: RawNode = None

    def __str__(self):
        base = f'{self.command} {self.entity}'
        if self.position is not None:
            if self.nbt is not None:
                return f'{base} {self.position} {self.nbt}'
            return f'{base} {self.position}'
        return base


summon = Command('summon', parsed=ParsedSummonCommand)

# summon <entity> [<pos>] [<nbt>]
#  - summon <entity> <pos> <nbt>
summon.add_variation(
    Parser(NamespaceID(), 'entity'),
    Parser(Position(), 'position'),
    Parser(Any(), 'nbt'),
)
#  - summon <entity> <pos>
summon.add_variation(
    Parser(NamespaceID(), 'entity'),
    Parser(Position(), 'position'),
)
#  - summon <entity>
summon.add_variation(
    Parser(NamespaceID(), 'entity'),
)
