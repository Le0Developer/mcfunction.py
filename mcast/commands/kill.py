
from dataclasses import dataclass

from . import Command, ParsedCommand, Parser
from ..nodes import EntityNode
from ..parser_types import Entity


@dataclass()
class ParsedKillCommand(ParsedCommand):
    command: str

    target: EntityNode = None

    def __str__(self):
        if self.target is not None:
            return f'{self.command} {self.target}'
        return self.command


kill = Command('kill', parsed=ParsedKillCommand)

# kill [<targets>]
#  - kill [<targets>]
kill.add_variation(
    Parser(Entity(), 'target'),
)
#  - kill
kill.add_variation()
