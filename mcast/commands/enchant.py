
from dataclasses import dataclass

from . import Command, ParsedCommand, Parser
from ..nodes import EntityNode, IntegerNode, NamespaceIDNode
from ..parser_types import Entity, Integer, NamespaceID


@dataclass()
class ParsedEnchantCommand(ParsedCommand):
    command: str

    target: EntityNode
    enchantment: NamespaceIDNode

    level: IntegerNode = None

    def __str__(self):
        base = f'{self.command} {self.target} {self.enchantment}'
        if self.level is not None:
            return f'{base} {self.level}'
        return base


enchant = Command('enchant', parsed=ParsedEnchantCommand)

# enchant <targets> <enchantment> [<level>]
#  - enchant <targets> <enchantment> <level>
enchant.add_variation(
    Parser(Entity(), 'target'),
    Parser(NamespaceID(), 'enchantment'),
    Parser(Integer(), 'level'),
)
#  - enchant <targets> <enchantment>
enchant.add_variation(
    Parser(Entity(), 'target'),
    Parser(NamespaceID(), 'enchantment'),
)
