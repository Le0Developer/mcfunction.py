
from dataclasses import dataclass

from . import Command, ParsedCommand, Parser
from ..nodes import EntityNode, RawNode
from ..parser_types import Entity, GreedyAny


@dataclass()
class ParsedTellCommand(ParsedCommand):
    command: str

    target: EntityNode
    message: RawNode

    def __str__(self):
        return f'{self.command} {self.target} {self.message}'


tell = Command('tell', aliases=['msg', 'w'], parsed=ParsedTellCommand)

# tell <target> <message>
tell.add_variation(
    Parser(Entity(), 'target'),
    Parser(GreedyAny(), 'message'),
)
