
from dataclasses import dataclass

from .. import Command, ParsedCommand, Parser
from ...nodes import EntityNode, IntegerNode, ItemNode, RawNode
from ...parser_types import Any, Entity, Integer, Item


@dataclass()
class ParsedClearCommand(ParsedCommand):
    command: str

    target: EntityNode = None
    item: ItemNode = None
    data: RawNode = None
    count: IntegerNode = None

    def __str__(self):
        if self.target is not None:
            if self.item is not None:
                if self.data is not None:
                    if self.count is not None:
                        return f'{self.command} {self.target} {self.item} ' \
                               f'{self.data} {self.count}'
                    return f'{self.command} {self.target} {self.item} ' \
                           f'{self.data}'
                return f'{self.command} {self.target} {self.item}'
            return f'{self.command} {self.target}'
        return self.command


clear = Command('clear', parsed=ParsedClearCommand)


# clear [<targets>] [<item>] [<data>] [<count>]
#  - clear <targets> <item> <data> <count>
clear.add_variation(
    Parser(Entity(), 'target'),
    Parser(Item(), 'item'),
    Parser(Any(), 'data'),
    Parser(Integer(), 'count'),
)
#  - clear <targets> <item> <data>
clear.add_variation(
    Parser(Entity(), 'target'),
    Parser(Item(), 'item'),
    Parser(Any(), 'data'),
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
