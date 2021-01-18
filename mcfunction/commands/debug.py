
from dataclasses import dataclass

from . import Command, ParsedCommand, Parser
from ..nodes import RawNode
from ..parser_types import Union


@dataclass()
class ParsedDebugCommand(ParsedCommand):
    command: str

    action: RawNode

    def __str__(self):
        return f'{self.command} {self.action}'


debug = Command('debug', commandblock=False, parsed=ParsedDebugCommand)

# debug start
# debug stop
# debug report
debug.add_variation(
    Parser(Union('start', 'stop', 'report'), 'action')
)
