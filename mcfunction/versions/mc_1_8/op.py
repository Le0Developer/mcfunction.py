
from dataclasses import dataclass

from .. import Command, ParsedCommand, Parser
from ...nodes import EntityNode
from ...parser_types import Entity


@dataclass()
class ParsedOpCommand(ParsedCommand):
    command: str

    target: EntityNode

    def __str__(self):
        return f'{self.command} {self.target}'


op = Command('op', parsed=ParsedOpCommand, oplevel=3)

# op <target>
op.add_variation(
    Parser(Entity(), 'target'),
)
