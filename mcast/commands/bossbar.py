
from dataclasses import dataclass

from . import Command, ParsedCommand, Parser
from ..exceptions import ConstructionException
from ..nodes import EntityNode, IntegerNode, JSONNode, NamespaceIDNode, RawNode
from ..parser_types import Entity, Integer, JSON, Literal, NamespaceID, Union
from ..util import ensure_nodes


@dataclass()
class ParsedBossbarCommand(ParsedCommand):
    command: str

    action: RawNode

    id: NamespaceIDNode = None
    name: JSONNode = None
    setting: RawNode = None
    color: RawNode = None
    max: IntegerNode = None
    players: EntityNode = None
    style: RawNode = None
    value: IntegerNode = None
    visible: RawNode = None

    def __str__(self):
        base = f'{self.command} {self.action}'
        if self.action.value == 'add':
            ensure_nodes(self, 'id', 'name')
            return f'{base} {self.id} {self.name}'

        elif self.action.value == 'get':
            ensure_nodes(self, 'id', 'setting')
            return f'{base} {self.id} {self.setting}'

        elif self.action.value == 'list':
            return base

        elif self.action.value == 'remove':
            ensure_nodes(self, 'id')
            return f'{base} {self.id}'

        elif self.action.value == 'set':
            ensure_nodes(self, 'id', 'setting')
            value = getattr(self, self.setting.value)
            if value is None:
                return f'{base} {self.id} {self.setting.value}'
            return f'{base} {self.id} {self.setting.value} {value}'

        else:
            raise ConstructionException(
                f'expected action to be one \'add\', \'get\', \'list\', '
                f'\'remove\' or \'set\', not {self.action.value!r}'
            )


bossbar = Command('bossbar', parsed=ParsedBossbarCommand)

# bossbar add <id> <name>
bossbar.add_variation(
    Parser(Literal('add'), 'action'),
    Parser(NamespaceID(), 'id'),
    Parser(JSON(), 'name'),
)

# bossbar get <id> (max|players|value|visible)
bossbar.add_variation(
    Parser(Literal('get'), 'action'),
    Parser(NamespaceID(), 'id'),
    Parser(Union('max', 'players', 'value', 'visible'), 'setting'),
)

# bossbar list
bossbar.add_variation(
    Parser(Literal('list'), 'action'),
)

# bossbar remove <id>
bossbar.add_variation(
    Parser(Literal('remove'), 'action'),
    Parser(NamespaceID(), 'id'),
)

# bossbar set <id> color (blue|green|pink|purple|red|white|yellow)
bossbar.add_variation(
    Parser(Literal('set'), 'action'),
    Parser(NamespaceID(), 'id'),
    Parser(Literal('color'), 'setting'),
    Parser(Union('blue', 'green', 'pink', 'purple', 'red', 'white', 'yellow'),
           'color')
)

# bossbar set <id> max <max>
bossbar.add_variation(
    Parser(Literal('set'), 'action'),
    Parser(NamespaceID(), 'id'),
    Parser(Literal('max'), 'setting'),
    Parser(Integer(), 'max')
)

# bossbar set <id> name <name>
bossbar.add_variation(
    Parser(Literal('set'), 'action'),
    Parser(NamespaceID(), 'id'),
    Parser(Literal('name'), 'setting'),
    Parser(JSON(), 'name'),
)

# bossbar set <id> players [<targets>]
#  - bossbar set <id> players <targets>
bossbar.add_variation(
    Parser(Literal('set'), 'action'),
    Parser(NamespaceID(), 'id'),
    Parser(Literal('players'), 'setting'),
    Parser(Entity(), 'players'),
)
#  - bossbar set <id> players
bossbar.add_variation(
    Parser(Literal('set'), 'action'),
    Parser(NamespaceID(), 'id'),
    Parser(Literal('players'), 'setting'),
)

# bossbar set <id> style (notched_6|notched_10|notched_12|notched_20|progress)
bossbar.add_variation(
    Parser(Literal('set'), 'action'),
    Parser(NamespaceID(), 'id'),
    Parser(Literal('style'), 'setting'),
    Parser(
        Union('notched_6', 'notched_10', 'notched_12', 'notched_20',
              'progress'),
        'style'
    ),
)

# bossbar set <id> value <value>
bossbar.add_variation(
    Parser(Literal('set'), 'action'),
    Parser(NamespaceID(), 'id'),
    Parser(Literal('value'), 'setting'),
    Parser(Integer(), 'value'),
)

# bossbar set <id> visible <visible>
bossbar.add_variation(
    Parser(Literal('set'), 'action'),
    Parser(NamespaceID(), 'id'),
    Parser(Literal('visible'), 'setting'),
    Parser(Union('true', 'false'), 'visible'),
)
