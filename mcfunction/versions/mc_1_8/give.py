
from dataclasses import dataclass

from .. import Command, ParsedCommand, Parser
from ...nodes import EntityNode, IntegerNode, ItemNode
from ...parser_types import Entity, Integer, Item


@dataclass()
class ParsedGiveCommand(ParsedCommand):
    command: str

    target: EntityNode
    item: ItemNode

    count: IntegerNode = None

    def __str__(self):
        base = f'{self.command} {self.target} {self.item}'
        if self.count is not None:
            return f'{base} {self.count}'
        return base


give = Command('give', parsed=ParsedGiveCommand)

# give <target> <item> [<count>]
#  - give <target> <item> <count>
give.add_variation(
    Parser(Entity(), 'target'),
    Parser(Item(), 'item'),
    Parser(Integer(), 'count'),
)
#  - give <target> <item>
give.add_variation(
    Parser(Entity(), 'target'),
    Parser(Item(), 'item'),
)
