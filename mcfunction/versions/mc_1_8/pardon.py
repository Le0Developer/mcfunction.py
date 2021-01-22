
from dataclasses import dataclass

from .. import Command, ParsedCommand, Parser
from ...nodes import EntityNode
from ...parser_types import Entity


@dataclass()
class ParsedPardonCommand(ParsedCommand):
    command: str

    target: EntityNode

    def __str__(self):
        return f'{self.command} {self.target}'


pardon = Command('pardon', parsed=ParsedPardonCommand, oplevel=3)

# pardon <target>
pardon.add_variation(
    Parser(Entity(), 'target'),
)
