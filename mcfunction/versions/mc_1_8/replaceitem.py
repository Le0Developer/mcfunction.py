
from dataclasses import dataclass

from .. import Command, ParsedCommand, Parser
from ...exceptions import ConstructionException
from ...nodes import EntityNode, IntegerNode, ItemNode, PositionNode, RawNode
from ...parser_types import Any, Entity, Integer, Item, Literal, Position


@dataclass()
class ParsedReplaceitemCommand(ParsedCommand):
    command: str

    action: RawNode
    slot: RawNode
    item: ItemNode

    position: PositionNode = None
    target: EntityNode = None
    count: IntegerNode = None

    def __str__(self):
        base = f'{self.command} {self.action}'
        if self.action.value == 'block':
            base = f'{base} {self.position} {self.slot} {self.item}'
        elif self.action.value == 'entity':
            base = f'{base} {self.target} {self.slot} {self.item}'
        else:
            raise ConstructionException(
                f'expected action to be \'block\' or \'entity\', '
                f'not {self.action.value!r}'
            )

        if self.count is not None:
            return f'{base} {self.count}'
        return base


replaceitem = Command('replaceitem', parsed=ParsedReplaceitemCommand)

# replaceitem block <pos> <slot> <item> [<count>]
#  - replaceitem block <pos> <slot> <item> <count>
replaceitem.add_variation(
    Parser(Literal('block'), 'action'),
    Parser(Position(), 'position'),
    Parser(Any(), 'slot'),
    Parser(Item(), 'item'),
    Parser(Integer(), 'count'),
)
#  - replaceitem block <pos> <slot> <item>
replaceitem.add_variation(
    Parser(Literal('block'), 'action'),
    Parser(Position(), 'position'),
    Parser(Any(), 'slot'),
    Parser(Item(), 'item'),
)

# replaceitem entity <targets> <slot> <item> [<count>]
#  - replaceitem entity <targets> <slot> <item> <count>
replaceitem.add_variation(
    Parser(Literal('entity'), 'action'),
    Parser(Entity(), 'target'),
    Parser(Any(), 'slot'),
    Parser(Item(), 'item'),
    Parser(Integer(), 'count'),
)
#  - replaceitem entity <targets> <slot> <item>
replaceitem.add_variation(
    Parser(Literal('entity'), 'action'),
    Parser(Entity(), 'target'),
    Parser(Any(), 'slot'),
    Parser(Item(), 'item'),
)
