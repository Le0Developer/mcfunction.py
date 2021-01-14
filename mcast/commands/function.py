
from dataclasses import dataclass

from . import Command, ParsedCommand, Parser
from ..nodes import FunctionNode
from ..parser_types import Function


@dataclass()
class ParsedFunctionCommand(ParsedCommand):
    command: str

    name: FunctionNode

    def __str__(self):
        return f'{self.command} {self.name}'


function = Command('function', parsed=ParsedFunctionCommand)

# function <name>
function.add_variation(
    Parser(Function(), 'name'),
)
