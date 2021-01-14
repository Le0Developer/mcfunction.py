
from dataclasses import dataclass

from . import Command, ParsedCommand, Parser
from ..nodes import EntityNode, JSONNode
from ..parser_types import Entity, JSON


@dataclass()
class ParsedTellrawCommand(ParsedCommand):
    command: str

    target: EntityNode
    message: JSONNode

    def __str__(self):
        return f'{self.command} {self.target} {self.message}'


tellraw = Command('tellraw', parsed=ParsedTellrawCommand)

# tellraw <target> <message>
tellraw.add_variation(
    Parser(Entity(), 'target'),
    Parser(JSON(), 'message'),
)
