
from dataclasses import dataclass
import typing as t

from .. import Command, ParsedCommand, Parser
from ...nodes import EntityNode, IntegerNode, RawNode
from ...parser_types import Any, Entity, Integer


@dataclass()
class ParsedExperienceCommand(ParsedCommand):
    command: str

    amount: t.Union[IntegerNode, RawNode]
    target: EntityNode = None

    def __str__(self):
        base = f'{self.command} {self.amount}'
        if self.target is not None:
            return f'{base} {self.target}'
        return base


experience = Command('experience', aliases=['xp'],
                     parsed=ParsedExperienceCommand)

# xp <amount> [player]
#  - xp <amount> <player>
experience.add_variation(
    Parser(Integer(), 'amount'),
    Parser(Entity(), 'target')
)
#  - xp <amount>
experience.add_variation(
    Parser(Integer(), 'amount'),
)

# xp <amount>L [player]
#  - xp <amount>L <player>
experience.add_variation(
    Parser(Any(), 'amount'),
    Parser(Entity(), 'target')
)
#  - xp <amount>L
experience.add_variation(
    Parser(Any(), 'amount'),
)
