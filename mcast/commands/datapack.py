
from dataclasses import dataclass

from . import Command, ParsedCommand, Parser
from ..exceptions import ConstructionException
from ..nodes import RawNode
from ..parser_types import Any, Literal, Union
from ..util import ensure_nodes


@dataclass()
class ParsedDatapackCommand(ParsedCommand):
    command: str

    action: RawNode

    name: RawNode = None
    mode: RawNode = None  # re-used quite a lot
    existing: RawNode = None

    def __str__(self):
        base = f'{self.command} {self.action}'
        if self.action.value == 'enable':
            if self.mode is not None:
                if self.mode.value in ('before', 'after'):
                    ensure_nodes(self, 'existing')
                    return f'{base} {self.name} {self.mode} {self.existing}'
                return f'{base} {self.name} {self.mode}'
            return f'{base} {self.name}'

        elif self.action.value == 'disable':
            return f'{base} {self.name}'

        elif self.action.value == 'list':
            if self.mode is not None:
                return f'{base} {self.mode}'
            return base

        else:
            raise ConstructionException(
                f'expected action to be \'enable\', \'disable\' or \'list\', '
                f'not {self.action.value!r}'
            )


datapack = Command('datapack', parsed=ParsedDatapackCommand)

# datapack enable <name>
# datapack disable <name>
datapack.add_variation(
    Parser(Union('enable', 'disable'), 'action'),
    Parser(Any(), 'name'),
)

# datapack enable <name> (first|last)
datapack.add_variation(
    Parser(Literal('enable'), 'action'),
    Parser(Any(), 'name'),
    Parser(Union('first', 'last'), 'mode'),
)

# datapack enable <name> (before|after) <existing>
datapack.add_variation(
    Parser(Literal('enable'), 'action'),
    Parser(Any(), 'name'),
    Parser(Union('before', 'after'), 'mode'),
    Parser(Any(), 'existing'),
)

# datapack list [available|enabled]
#  - datapack list (available|enabled)
datapack.add_variation(
    Parser(Literal('list'), 'action'),
    Parser(Union('available', 'enabled'), 'mode'),
)
#  - datapack list
datapack.add_variation(
    Parser(Literal('list'), 'action'),
)
