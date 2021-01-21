
from dataclasses import dataclass

from .. import Command, ParsedCommand, Parser
from ...exceptions import ConstructionException
from ...nodes import EntityNode, IntegerNode, RawNode
from ...parser_types import Entity, Integer, Literal, Union
from ...util import ensure_nodes


@dataclass()
class ParsedExperienceCommand(ParsedCommand):
    command: str

    action: RawNode
    target: EntityNode

    amount: IntegerNode = None
    unit: RawNode = None

    def __str__(self):
        base = f'{self.command} {self.action} {self.target}'
        if self.action.value in ('add', 'set'):
            ensure_nodes(self, 'amount')
            if self.unit is not None:
                return f'{base} {self.amount} {self.unit}'
            return f'{base} {self.amount}'

        elif self.action.value == 'query':
            ensure_nodes(self, 'unit')
            return f'{base} {self.unit}'

        else:
            raise ConstructionException(
                f'expected action to be \'add\', \'set\' or \'query\', '
                f'not {self.action.value!r}'
            )


experience = Command('experience', aliases=['xp'],
                     parsed=ParsedExperienceCommand)

# experience add <targets> <amount> [levels|points]
# experience set <targets> <amount> [levels|points]
#  - experience (add|set) <targets> <amount> (levels|points)
experience.add_variation(
    Parser(Union('add', 'set'), 'action'),
    Parser(Entity(), 'target'),
    Parser(Integer(), 'amount'),
    Parser(Union('levels', 'points'), 'unit'),
)
#  - experience (add|set) <targets> <amount>
experience.add_variation(
    Parser(Union('add', 'set'), 'action'),
    Parser(Entity(), 'target'),
    Parser(Integer(), 'amount'),
)

# experience query <targets> (levels|points)
experience.add_variation(
    Parser(Literal('query'), 'action'),
    Parser(Entity(), 'target'),
    Parser(Union('levels', 'points'), 'unit'),
)
