
from dataclasses import dataclass
import typing as t

from .. import Command, ParsedCommand, Parser
from ...exceptions import ConstructionException
from ...nodes import EntityNode, IntegerNode, ItemNode, PositionNode, RawNode
from ...parser_types import Any, Entity, Integer, Item, Literal, Position
from ...util import ensure_nodes


@dataclass()
class ParsedItemCommand(ParsedCommand):
    command: str

    target_type: RawNode
    target: t.Union[PositionNode, EntityNode]
    slot: RawNode
    action: RawNode

    source_type: RawNode = None
    source: t.Union[PositionNode, EntityNode] = None
    source_slot: RawNode = None
    modifier: RawNode = None
    item: ItemNode = None
    count: IntegerNode = None

    def __str__(self):
        base = (f'{self.command} {self.target_type} {self.target} {self.slot} '
                f'{self.action}')

        if self.action.value == 'copy':
            ensure_nodes(self, 'source_type', 'source', 'source_slot')
            command = f'{base} {self.source_type} {self.source} ' \
                      f'{self.source_slot}'
            if self.modifier is not None:
                return f'{command} {self.modifier}'
            return command

        elif self.action.value == 'modify':
            ensure_nodes(self, 'modifier')
            return f'{base} {self.modifier}'

        elif self.action.value == 'replace':
            ensure_nodes(self, 'item')
            if self.count is not None:
                return f'{base} {self.item} {self.count}'
            return f'{base} {self.item}'

        else:
            raise ConstructionException(
                f'expected action to be \'copy\', \'modfiy\' or \'replace\', '
                f'not {self.action.value!r}'
            )


item = Command('item', parsed=ParsedItemCommand)

TYPES = (('block', Position()), ('entity', Entity()))

for target_type, target in TYPES:
    # item <TARGET> <slot> copy <SOURCE> <slot> [<modifier>]
    for source_type, source in TYPES:
        #  - item <TARGET> <slot> copy <SOURCE> <slot> <modifier>
        item.add_variation(
            Parser(Literal(target_type), 'target_type'),
            Parser(target, 'target'),
            Parser(Any(), 'slot'),
            Parser(Literal('copy'), 'action'),
            Parser(Literal(source_type), 'source_type'),
            Parser(source, 'source'),
            Parser(Any(), 'source_slot'),
            Parser(Any(), 'modifier')
        )
        #  - item <TARGET> <slot> copy <SOURCE> <slot>
        item.add_variation(
            Parser(Literal(target_type), 'target_type'),
            Parser(target, 'target'),
            Parser(Any(), 'slot'),
            Parser(Literal('copy'), 'action'),
            Parser(Literal(source_type), 'source_type'),
            Parser(source, 'source'),
            Parser(Any(), 'source_slot')
        )
    # item <TARGET> <slot> modify <modifier>
    item.add_variation(
        Parser(Literal(target_type), 'target_type'),
        Parser(target, 'target'),
        Parser(Any(), 'slot'),
        Parser(Literal('modify'), 'action'),
        Parser(Any(), 'modifier')
    )
    # item <TARGET> <slot> replace <item> [<count>]
    #  - item <TARGET> <slot> replace <item> <count>
    item.add_variation(
        Parser(Literal(target_type), 'target_type'),
        Parser(target, 'target'),
        Parser(Any(), 'slot'),
        Parser(Literal('replace'), 'action'),
        Parser(Item(), 'item'),
        Parser(Integer(), 'count')
    )
    #  - item <TARGET> <slot> replace <item>
    item.add_variation(
        Parser(Literal(target_type), 'target_type'),
        Parser(target, 'target'),
        Parser(Any(), 'slot'),
        Parser(Literal('replace'), 'action'),
        Parser(Item(), 'item')
    )
