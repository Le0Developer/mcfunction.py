
from dataclasses import dataclass

from .. import Command, ParsedCommand, Parser
from ...nodes import EntityNode, RawNode
from ...parser_types import Any, Entity


@dataclass()
class ParsedEntitydataCommand(ParsedCommand):
    command: str

    target: EntityNode
    data: RawNode

    def __str__(self):
        return f'{self.command} {self.target} {self.data}'


entitydata = Command('entitydata', parsed=ParsedEntitydataCommand)

# entitydata <entity> <data>
entitydata.add_variation(
    Parser(Entity(), 'target'),
    Parser(Any(), 'data'),
)
