
from dataclasses import dataclass

from .. import Command, ParsedCommand, Parser
from ...nodes import EntityNode
from ...parser_types import Entity


@dataclass()
class ParsedDeopCommand(ParsedCommand):
    command: str

    target: EntityNode

    def __str__(self):
        return f'{self.command} {self.target}'


deop = Command('deop', parsed=ParsedDeopCommand, commandblock=False)

# deop <target>
deop.add_variation(
    Parser(Entity(), 'target'),
)
