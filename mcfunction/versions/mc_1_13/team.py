
from dataclasses import dataclass

from .. import Command, ParsedCommand, Parser
from ...exceptions import ConstructionException
from ...nodes import EntityNode, JSONNode, RawNode
from ...parser_types import Any, Entity, JSON, Literal
from ...util import ensure_nodes


@dataclass()
class ParsedTeamCommand(ParsedCommand):
    command: str

    action: RawNode

    team: RawNode = None
    name: JSONNode = None
    target: EntityNode = None
    option: RawNode = None
    value: RawNode = None

    def __str__(self):
        base = f'{self.command} {self.action}'
        if self.action.value == 'add':
            ensure_nodes(self, 'team')
            if self.name is not None:
                return f'{base} {self.team} {self.name}'
            return f'{base} {self.team}'

        elif self.action.value in ('empty', 'remove'):
            ensure_nodes(self, 'team')
            return f'{base} {self.team}'

        elif self.action.value == 'join':
            ensure_nodes(self, 'team')
            if self.target is not None:
                return f'{base} {self.team} {self.target}'
            return f'{base} {self.team}'

        elif self.action.value == 'leave':
            ensure_nodes(self, 'target')
            return f'{base} {self.target}'

        elif self.action.value == 'list':
            if self.team is not None:
                return f'{base} {self.team}'
            return base

        elif self.action.value == 'modify':
            ensure_nodes(self, 'team', 'option', 'value')
            return f'{base} {self.team} {self.option} {self.value}'

        else:
            raise ConstructionException(
                f'expected action to be \'add\', \'empty\', \'remove\', '
                f'\'join\', \'leave\' or \'modify\', not {self.action.value!r}'
            )


team = Command('team', parsed=ParsedTeamCommand)

# team add <team> [<displayName>]
#  - team add <team> <displayName>
team.add_variation(
    Parser(Literal('add'), 'action'),
    Parser(Any(), 'team'),
    Parser(JSON(), 'name'),
)
#  - team add <team>
team.add_variation(
    Parser(Literal('add'), 'action'),
    Parser(Any(), 'team'),
)
# team empty <team>
team.add_variation(
    Parser(Literal('empty'), 'action'),
    Parser(Any(), 'team'),
)
# team join <team> [<members>]
#  - team join <team> <members>
team.add_variation(
    Parser(Literal('join'), 'action'),
    Parser(Any(), 'team'),
    Parser(Entity(), 'target'),
)
#  - team join <team>
team.add_variation(
    Parser(Literal('join'), 'action'),
    Parser(Any(), 'team'),
)
# team leave <members>
team.add_variation(
    Parser(Literal('leave'), 'action'),
    Parser(Entity(), 'target'),
)
# team list [<team>]
#  - team list <team>
team.add_variation(
    Parser(Literal('list'), 'action'),
    Parser(Any(), 'team'),
)
#  - team list
team.add_variation(
    Parser(Literal('list'), 'action'),
)
# team modify <team> <option> <value>
team.add_variation(
    Parser(Literal('modify'), 'action'),
    Parser(Any(), 'team'),
    Parser(Any(), 'option'),
    Parser(Any(), 'value'),
)
# team remove <team>
team.add_variation(
    Parser(Literal('remove'), 'action'),
    Parser(Any(), 'team'),
)
