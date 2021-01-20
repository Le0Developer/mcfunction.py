
from dataclasses import dataclass

from .. import Command, ParsedCommand, Parser
from ...nodes import RawNode
from ...parser_types import Any, Literal, Union


@dataclass()
class ParsedTimeCommand(ParsedCommand):
    command: str

    action: RawNode
    time: RawNode

    def __str__(self):
        return f'{self.command} {self.action} {self.time}'


time = Command('time', parsed=ParsedTimeCommand)

# time add <time>
time.add_variation(
    Parser(Literal('add'), 'action'),
    Parser(Any(), 'time'),
)
# time query (daytime|gametime)
time.add_variation(
    Parser(Literal('query'), 'action'),
    Parser(Union('daytime', 'gametime'), 'time'),
)
# time set <time>
time.add_variation(
    Parser(Literal('set'), 'action'),
    Parser(Any(), 'time'),
)
# time set (day|night)
time.add_variation(
    Parser(Literal('set'), 'action'),
    Parser(Union('day', 'night'), 'time'),
)
