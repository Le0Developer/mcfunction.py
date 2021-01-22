
from dataclasses import dataclass

from .. import Command, ParsedCommand, Parser
from ...nodes import IntegerNode
from ...parser_types import Integer


@dataclass()
class ParsedSetidletimeoutCommand(ParsedCommand):
    command: str

    minutes: IntegerNode

    def __str__(self):
        return f'{self.command} {self.minutes}'


setidletimeout = Command('setidletimeout', parsed=ParsedSetidletimeoutCommand,
                         oplevel=3)

# setidletimeout <minutes>
setidletimeout.add_variation(
    Parser(Integer(), 'minutes')
)
