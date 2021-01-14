
from dataclasses import dataclass

from . import Command, ParsedCommand, Parser
from ..nodes import EntityNode, IntegerNode, ItemNode
from ..parser_types import Entity, Integer, Item


@dataclass()
class ParsedClearCommand(ParsedCommand):
    command: str

    target: EntityNode = None
    item: ItemNode = None
    count: IntegerNode = None

    def __str__(self):
        if self.target is not None:
            if self.item is not None:
                if self.count is not None:
                    return f'{self.command} {self.target} {self.item} ' \
                           f'{self.count}'
                return f'{self.command} {self.target} {self.item}'
            return f'{self.command} {self.target}'
        return self.command


clear = Command('clear', parsed=ParsedClearCommand)


# clear [<targets>] [<item>] [<maxCount>]
#  - clear <targets> <item> <maxCount>
clear.add_variation(
    Parser(Entity(), 'target'),
    Parser(Item(), 'item'),
    Parser(Integer(), 'count'),
)
#  - clear <targets> <item>
clear.add_variation(
    Parser(Entity(), 'target'),
    Parser(Item(), 'item'),
)
#  - clear <targets>
clear.add_variation(
    Parser(Entity(), 'target'),
)
#  - clear
clear.add_variation()
