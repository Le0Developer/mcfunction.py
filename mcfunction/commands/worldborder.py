
from dataclasses import dataclass

from . import Command, ParsedCommand, Parser
from ..exceptions import ConstructionException
from ..nodes import IntegerNode, Position2dNode, RawNode
from ..parser_types import Integer, Literal, Position2d, Union
from ..util import ensure_nodes


@dataclass()
class ParsedWordborderCommand(ParsedCommand):
    command: str

    action: RawNode

    distance: IntegerNode = None
    time: IntegerNode = None
    center: Position2dNode = None
    name: RawNode = None
    value: IntegerNode = None

    def __str__(self):
        base = f'{self.command} {self.action}'
        if self.action.value in ('add', 'set'):
            ensure_nodes(self, 'distance')
            if self.time is not None:
                return f'{base} {self.distance} {self.time}'
            return f'{base} {self.distance}'
        elif self.action.value == 'center':
            ensure_nodes(self, 'center')
            return f'{base} {self.center}'
        elif self.action.value == 'get':
            return base
        elif self.action.value in ('damage', 'warning'):
            ensure_nodes(self, 'name', 'value')
            return f'{base} {self.name} {self.value}'
        else:
            raise ConstructionException(
                f'expected action to be \'add\', \'set\', \'center\', '
                f'\'get\', \'damage\' or \'warning\', '
                f'not {self.action.value!r}'
            )


worldborder = Command('worldborder', parsed=ParsedWordborderCommand)
# worldborder add <distance> [<time>]
# worldborder set <distance> [<time>]
#  - worldborder (add|set) <distance> <time>
worldborder.add_variation(
    Parser(Union('add', 'set'), 'action'),
    Parser(Integer(), 'distance'),
    Parser(Integer(), 'time')
)
#  - worldborder (add|set) <distance>
worldborder.add_variation(
    Parser(Union('add', 'set'), 'action'),
    Parser(Integer(), 'distance'),
)
# worldborder center <pos>
worldborder.add_variation(
    Parser(Literal('center'), 'action'),
    Parser(Position2d(), 'center'),
)
# worldborder damage amount <damagePerBlock>
# worldborder damage buffer <distance>
worldborder.add_variation(
    Parser(Literal('damage'), 'action'),
    Parser(Union('amount', 'buffer'), 'name'),
    Parser(Integer(), 'value'),
)
# worldborder get
worldborder.add_variation(
    Parser(Literal('get'), 'action'),
)
# worldborder warning distance <distance>
# worldborder warning time <time>
worldborder.add_variation(
    Parser(Literal('warning'), 'action'),
    Parser(Union('distance', 'time'), 'name'),
    Parser(Integer(), 'value'),
)
