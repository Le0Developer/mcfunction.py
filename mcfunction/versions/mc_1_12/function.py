
from dataclasses import dataclass

from .. import Command, ParsedCommand, Parser
from ...nodes import EntityNode, FunctionNode, RawNode
from ...parser_types import Entity, Function, Union


@dataclass()
class ParsedFunctionCommand(ParsedCommand):
    command: str

    name: FunctionNode
    condition: RawNode = None
    selector: EntityNode = None

    def __str__(self):
        if self.condition is not None:
            return f'{self.command} {self.name} {self.condition} ' \
                   f'{self.selector}'
        return f'{self.command} {self.name}'


function = Command('function', parsed=ParsedFunctionCommand)

# function <name> [if|unless] [selector]
#  - function <name> (if|unless) <selector>
function.add_variation(
    Parser(Function(), 'name'),
    Parser(Union('if', 'unless'), 'condition'),
    Parser(Entity(), 'selector')
)
#  - function <name>
function.add_variation(
    Parser(Function(), 'name'),
)
