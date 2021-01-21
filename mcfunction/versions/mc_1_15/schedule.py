
from dataclasses import dataclass

from .. import Command, ParsedCommand, Parser
from ...exceptions import ConstructionException
from ...nodes import FunctionNode, RawNode
from ...parser_types import Any, Function, Literal, Union


@dataclass()
class ParsedScheduleCommand(ParsedCommand):
    command: str

    action: RawNode
    name: FunctionNode

    time: RawNode = None
    mode: RawNode = None

    def __str__(self):
        base = f'{self.command} {self.action} {self.name}'
        if self.action.value == 'function':
            if self.mode is not None:
                return f'{base} {self.time} {self.mode}'
            return f'{base} {self.time}'

        elif self.action.value == 'clear':
            return base

        else:
            raise ConstructionException(
                f'expected action expected to be \'function\' or \'clear\', '
                f'not {self.action.value!r}'
            )


schedule = Command('schedule', parsed=ParsedScheduleCommand)

# schedule function <function> <time> [append|replace]
#  - schedule function <function> <time> (append|replace)
schedule.add_variation(
    Parser(Literal('function'), 'action'),
    Parser(Function(), 'name'),
    # can't use Integer because of -d, -s, and -t suffixes
    Parser(Any(), 'time'),
    Parser(Union('append', 'replace'), 'mode'),
)
#  - schedule function <function> <time>
schedule.add_variation(
    Parser(Literal('function'), 'action'),
    Parser(Function(), 'name'),
    Parser(Any(), 'time'),
)

# schedule clear <function>
schedule.add_variation(
    Parser(Literal('clear'), 'action'),
    Parser(Function(), 'name'),
)
