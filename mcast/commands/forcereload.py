
from dataclasses import dataclass
import typing as t

from . import Command, ParsedCommand, Parser
from ..exceptions import ConstructionException
from ..nodes import Position2dNode, RawNode
from ..parser_types import Literal, Position2d, Union
from ..util import ensure_nodes


@dataclass()
class ParsedForcereloadCommand(ParsedCommand):
    command: str

    action: RawNode

    start: t.Union[Position2dNode, RawNode] = None
    end: Position2dNode = None

    def __str__(self):
        base = f'{self.command} {self.action}'
        if self.action.value in ('add', 'remove'):
            ensure_nodes(self, 'start')
            if self.end is not None:
                return f'{base} {self.start} {self.end}'
            return f'{base} {self.start}'

        elif self.action.value == 'query':
            if self.start is not None:
                return f'{base} {self.start}'
            return base

        else:
            raise ConstructionException(
                f'expected action to be \'add\', \'remove\' or \'query\', '
                f'not {self.action.value!r}'
            )


forcereload = Command('forcereload', parsed=ParsedForcereloadCommand)

# forceload (add|remove) <from> [<to>]
#  - forceload (add|remove) <from> <to>
forcereload.add_variation(
    Parser(Union('add', 'remove'), 'action'),
    Parser(Position2d(), 'start'),  # from is a keyword, so use start instead
    Parser(Position2d(), 'end'),  # consistency with start
)
#  - forceload (add|remove) <from>
forcereload.add_variation(
    Parser(Union('add', 'remove'), 'action'),
    Parser(Position2d(), 'start'),
)

# forceload remove all
forcereload.add_variation(
    Parser(Literal('remove'), 'action'),
    Parser(Literal('all'), 'start')
)

# forceload query [<pos>]
#  - forceload query <pos>
forcereload.add_variation(
    Parser(Literal('query'), 'action'),
    Parser(Position2d(), 'start')
)
#  - forceload query
forcereload.add_variation(
    Parser(Literal('query'), 'action'),
)
