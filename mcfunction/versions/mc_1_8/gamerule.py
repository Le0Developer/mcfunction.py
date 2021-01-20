
from dataclasses import dataclass
import typing as t

from .. import Command, ParsedCommand, Parser
from ...nodes import IntegerNode, RawNode
from ...parser_types import Any, Integer, Union


@dataclass()
class ParsedGameruleCommand(ParsedCommand):
    command: str

    rule: RawNode

    value: t.Union[IntegerNode, RawNode] = None

    def __str__(self):
        base = f'{self.command} {self.rule}'
        if self.value is not None:
            return f'{base} {self.value}'
        return base


gamerule = Command('gamerule', parsed=ParsedGameruleCommand)

# gamerule <rule name> [<value>]
#  - gamerule <rule name> <value>
# some gamerules take booleans, others integers
gamerule.add_variation(
    Parser(Any(), 'rule'),
    Parser(Union('true', 'false'), 'value'),
)
gamerule.add_variation(
    Parser(Any(), 'rule'),
    Parser(Integer(), 'value'),
)
#  - gamerule <rule name>
gamerule.add_variation(
    Parser(Any(), 'rule'),
)
