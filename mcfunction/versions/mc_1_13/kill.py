
from dataclasses import dataclass

from .. import Command, ParsedCommand, Parser
from ...nodes import EntityNode
from ...parser_types import Entity


@dataclass()
class ParsedKillCommand(ParsedCommand):
    command: str

    target: EntityNode

    def __str__(self):
        return f'{self.command} {self.target}'


kill = Command('kill', parsed=ParsedKillCommand)

# kill <targets>
kill.add_variation(
    Parser(Entity(), 'target'),
)
