
from dataclasses import dataclass

from .. import Command, ParsedCommand, Parser
from ...nodes import PositionNode, RawNode
from ...parser_types import Literal, Position, Union


@dataclass()
class ParsedDebugCommand(ParsedCommand):
    command: str

    action: RawNode
    position: PositionNode = None

    def __str__(self):
        if self.action.value == 'chunk':
            return f'{self.command} {self.action} {self.position}'
        return f'{self.command} {self.action}'


debug = Command('debug', commandblock=False, parsed=ParsedDebugCommand)

# debug start
# debug stop
debug.add_variation(
    Parser(Union('start', 'stop'), 'action')
)

# debug chunk <postion>
debug.add_variation(
    Parser(Literal('chunk'), 'action'),
    Parser(Position(), 'position')
)
