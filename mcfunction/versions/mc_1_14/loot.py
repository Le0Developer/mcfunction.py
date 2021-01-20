
from dataclasses import dataclass
import typing as t

from .. import Command, ParsedCommand, Parser
from ...exceptions import ConstructionException
from ...nodes import (
    EntityNode, IntegerNode, ItemNode, NamespaceIDNode, PositionNode, RawNode
)
from ...parser_types import (
    Any, Entity, Integer, Item, Literal, NamespaceID, Position, Union
)


@dataclass()
class ParsedLootCommand(ParsedCommand):
    command: str

    target_type: RawNode
    target: t.Union[EntityNode, PositionNode]
    source_type: RawNode
    source: t.Union[EntityNode, NamespaceIDNode, PositionNode]

    target_type2: RawNode = None
    slot: RawNode = None
    count: IntegerNode = None
    source_position: PositionNode = None
    source_tool: t.Union[ItemNode, RawNode] = None

    def __str__(self):
        if self.target_type.value in ('spawn', 'give', 'insert'):
            target = f'{self.target_type} {self.target}'
        elif self.target_type.value == 'replace':
            target = (f'{self.target_type} {self.target_type2} {self.target} '
                      f'{self.slot}')
            if self.count is not None:
                target = f'{target} {self.count}'
        else:
            raise ConstructionException(
                f'expected target_type to be \'spawn\', \'replace\', \'give\' '
                f'or \'insert\', not {self.target_type.value!r}'
            )

        source = f'{self.source_type} {self.source}'
        if self.source_type.value == 'fish':
            source = f'{source} {self.source_position}'
            if self.source_tool is not None:
                source = f'{source} {self.source_tool}'
        elif self.source_type.value == 'mine' and self.source_tool is not None:
            source = f'{source} {self.source_tool}'

        return f'{self.command} {target} {source}'


loot = Command('loot', parsed=ParsedLootCommand)


TARGETS = (
    # ... spawn <targetPos> ...
    (Parser(Literal('spawn'), 'target_type'),
     Parser(Position(), 'target'),),
    # ... replace entity <entities> <slot> [<count>] ...
    #  - ... replace entity <entities> <slot> <count> ...
    (Parser(Literal('replace'), 'target_type'),
     Parser(Literal('entity'), 'target_type2'),
     Parser(Entity(), 'target'),
     Parser(Any(), 'slot'),
     Parser(Integer(), 'count'),),
    #  - ... replace entity <entities> <slot> ...
    (Parser(Literal('replace'), 'target_type'),
     Parser(Literal('entity'), 'target_type2'),
     Parser(Entity(), 'target'),
     Parser(Any(), 'slot'),),
    # ... replace block <targetPos> <slot> [<count>] ...
    #  - ... replace block <targetPos> <slot> <count> ...
    (Parser(Literal('replace'), 'target_type'),
     Parser(Literal('block'), 'target_type2'),
     Parser(Position(), 'target'),
     Parser(Any(), 'slot'),
     Parser(Integer(), 'count'),),
    #  - ... replace block <targetPos> <slot> ...
    (Parser(Literal('replace'), 'target_type'),
     Parser(Literal('block'), 'target_type2'),
     Parser(Position(), 'target'),
     Parser(Any(), 'slot'),),
    # ... give <players> ...
    (Parser(Literal('give'), 'target_type'),
     Parser(Entity(), 'target'),),
    # ... insert <targetPos> ...
    (Parser(Literal('insert'), 'target_type'),
     Parser(Position(), 'target'),)
)

SOURCES = (
    # ... fish <loot_table> <pos> [<tool>|mainhand|offhand]
    #  - ... fish <loot_table> <pos> (<tool>|mainhand|offhand)
    (Parser(Literal('fish'), 'source_type'),
     Parser(NamespaceID(), 'source'),
     Parser(Position(), 'source_position'),
     Parser(Union('mainhand', 'offhand'), 'source_tool'),),
    (Parser(Literal('fish'), 'source_type'),
     Parser(NamespaceID(), 'source'),
     Parser(Integer(), 'source_position'),
     Parser(Item(), 'source_tool'),),
    #  - ... fish <loot_table> <pos>
    (Parser(Literal('fish'), 'source_type'),
     Parser(NamespaceID(), 'source'),
     Parser(Position(), 'source_position'),),
    # ... loot <loot_table>
    (Parser(Literal('loot'), 'source_type'),
     Parser(NamespaceID(), 'source'),),
    # ... kill <target>
    (Parser(Literal('kill'), 'source_type'),
     Parser(Entity(), 'source'),),
    # ... mine <pos> [<tool>|mainhand|offhand]
    #  - ... mine <pos> (<tool>|mainhand|offhand)
    (Parser(Literal('mine'), 'source_type'),
     Parser(Position(), 'source'),
     Parser(Union('mainhand', 'offhand'), 'source_tool'),),
    (Parser(Literal('mine'), 'source_type'),
     Parser(Position(), 'source'),
     Parser(Item(), 'source_tool'),),
    #  - ... mine <pos>
    (Parser(Literal('mine'), 'source_type'),
     Parser(Position(), 'source'),),
)

for target in TARGETS:
    for source in SOURCES:
        loot.add_variation(*target, *source)
