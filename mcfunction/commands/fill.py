
from dataclasses import dataclass

from . import Command, ParsedCommand, Parser
from ..nodes import BlockNode, PositionNode, RawNode
from ..parser_types import Block, Literal, Union, Position


@dataclass()
class ParsedFillCommand(ParsedCommand):
    command: str

    start: PositionNode
    end: PositionNode
    block: BlockNode

    action: RawNode = None
    filter: BlockNode = None

    def __str__(self):
        base = f'{self.command} {self.start} {self.end} {self.block}'
        if self.action is None:
            return base
        elif self.action.value == 'replace' and self.filter is not None:
            return f'{base} {self.action} {self.filter}'
        return f'{base} {self.action}'


fill = Command('fill', parsed=ParsedFillCommand)

# fill <from> <to> <block> [destroy|hollow|keep|outline]
#  - fill <from> <to> <block> (destroy|hollow|keep|outline)
fill.add_variation(
    Parser(Position(), 'start'),  # from is a keyword, use start instead
    Parser(Position(), 'end'),  # consistency with start
    Parser(Block(), 'block'),
    Parser(Union('destroy', 'hollow', 'keep', 'outline'), 'action'),
)
#  - fill <from> <to> <block>
fill.add_variation(
    Parser(Position(), 'start'),
    Parser(Position(), 'end'),
    Parser(Block(), 'block'),
)

# fill <from> <to> <block> replace [<filter>]
#  - fill <from> <to> <block> replace <filter>
fill.add_variation(
    Parser(Position(), 'start'),
    Parser(Position(), 'end'),
    Parser(Block(), 'block'),
    Parser(Literal('replace'), 'action'),
    Parser(Block(), 'filter'),
)

#  - fill <from> <to> <block> replace
fill.add_variation(
    Parser(Position(), 'start'),
    Parser(Position(), 'end'),
    Parser(Block(), 'block'),
    Parser(Literal('replace'), 'action'),
)
