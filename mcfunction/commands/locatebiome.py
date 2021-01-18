
from dataclasses import dataclass
import typing as t

from . import Command, ParsedCommand, Parser
from ..nodes import IntegerNode, NamespaceIDNode
from ..parser_types import Integer, NamespaceID


@dataclass()
class ParsedLocatebiomeCommand(ParsedCommand):
    command: str

    biome: t.Union[IntegerNode, NamespaceIDNode]

    def __str__(self):
        return f'{self.command} {self.biome}'


locatebiome = Command('locatebiome', parsed=ParsedLocatebiomeCommand)

# locatebiome <biome>
locatebiome.add_variation(
    Parser(Integer(), 'biome'),
)
locatebiome.add_variation(
    Parser(NamespaceID(), 'biome'),
)
