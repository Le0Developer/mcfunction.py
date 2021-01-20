
from dataclasses import dataclass

from .. import Command, ParsedCommand, Parser
from ...nodes import BlockNode, PositionNode, RawNode
from ...parser_types import Block, Position, Union


@dataclass()
class ParsedSetblockCommand(ParsedCommand):
    command: str

    position: PositionNode
    block: BlockNode

    action: RawNode = None

    def __str__(self):
        base = f'{self.command} {self.position} {self.block}'
        if self.action is not None:
            return f'{base} {self.action}'
        return base


setblock = Command('setblock', parsed=ParsedSetblockCommand)

# setblock <pos> <block> [destroy|keep|replace]
#  - setblock <pos> <block> (destroy|keep|replace)
setblock.add_variation(
    Parser(Position(), 'position'),
    Parser(Block(), 'block'),
    Parser(Union('destroy', 'keep', 'replace'), 'action'),
)
#  - setblock <pos> <block>
setblock.add_variation(
    Parser(Position(), 'position'),
    Parser(Block(), 'block'),
)
