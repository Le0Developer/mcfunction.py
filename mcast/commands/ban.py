
from dataclasses import dataclass

from . import Command, ParsedCommand, Parser
from ..nodes import EntityNode, RawNode
from ..parser_types import Entity, GreedyAny


@dataclass()
class ParsedBanCommand(ParsedCommand):
    command: str

    target: EntityNode

    reason: RawNode = None

    def __str__(self):
        base = f'{self.command} {self.target}'
        if self.reason is not None:
            return f'{base} {self.reason}'
        return base


ban = Command('ban', commandblock=False, parsed=ParsedBanCommand)

# ban <targets> [<reason>]
#  - ban <targets> <reason>
ban.add_variation(
    Parser(Entity(), 'target'),
    Parser(GreedyAny(), 'reason'),
)
#  - ban <targets>
ban.add_variation(
    Parser(Entity(), 'target'),
)
