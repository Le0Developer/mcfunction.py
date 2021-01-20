
from dataclasses import dataclass

from .. import Command, ParsedCommand, Parser
from ...nodes import EntityNode, RawNode
from ...parser_types import Entity, GreedyAny


@dataclass()
class ParsedKickCommand(ParsedCommand):
    command: str

    target: EntityNode

    reason: RawNode = None

    def __str__(self):
        base = f'{self.command} {self.target}'
        if self.reason is not None:
            return f'{base} {self.reason}'
        return base


kick = Command('kick', commandblock=False, parsed=ParsedKickCommand)

# kick <targets> [<reason>]
#  - kick <targets> <reason>
kick.add_variation(
    Parser(Entity(), 'target'),
    Parser(GreedyAny(), 'reason'),
)
#  - kick <targets>
kick.add_variation(
    Parser(Entity(), 'target'),
)
