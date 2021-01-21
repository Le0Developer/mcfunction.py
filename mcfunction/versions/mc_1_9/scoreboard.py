
from dataclasses import dataclass

from .. import Command, ParsedCommand, Parser
from ...exceptions import ConstructionException
from ...nodes import EntityNode, IntegerNode, JSONNode, RawNode
from ...parser_types import (
    Any, Entity, Integer, Union, JSON, Literal, Objective, ScoreboardEntity
)
from ...util import ensure_nodes


@dataclass()
class ParsedScoreboardCommand(ParsedCommand):
    command: str

    category: RawNode
    action: RawNode

    objective: RawNode = None
    criterion: RawNode = None
    name: JSONNode = None
    mode: RawNode = None
    slot: RawNode = None
    target: EntityNode = None
    value: IntegerNode = None
    operation: RawNode = None
    source_target: EntityNode = None
    source_objective: RawNode = None
    team: RawNode = None
    option: RawNode = None

    def __str__(self):
        base = f'{self.command} {self.category} {self.action}'
        if self.category.value == 'objectives':
            if self.action.value == 'add':
                ensure_nodes(self, 'objective', 'criterion')
                command = f'{base} {self.objective} {self.criterion}'
                if self.name is not None:
                    return f'{command} {self.name}'
                return command

            elif self.action.value == 'list':
                return base

            elif self.action.value == 'modify':
                ensure_nodes(self, 'mode', 'objective')
                if self.mode.value == 'displayname':
                    ensure_nodes(self, 'name')
                    return f'{base} {self.objective} {self.mode} {self.name}'
                elif self.mode.value == 'rendertype':
                    ensure_nodes(self, 'value')
                    return f'{base} {self.objective} {self.mode} {self.value}'
                else:
                    raise ConstructionException(
                        f'expected mode to be \'displayname\' or '
                        f'\'rendertype\', not {self.mode.value!r}'
                    )

            elif self.action.value == 'remove':
                ensure_nodes(self, 'objective')
                return f'{base} {self.objective}'

            elif self.action.value == 'setdisplay':
                ensure_nodes(self, 'slot')
                if self.objective is not None:
                    return f'{base} {self.slot} {self.objective}'
                return f'{base} {self.slot}'

            else:
                raise ConstructionException(
                    f'expected action to be \'add\', \'list\', \'modify\', '
                    f'\'remove\' or \'setdisplay\', not {self.action.value!r}'
                )

        elif self.category.value == 'players':
            if self.action.value in ('add', 'remove', 'set'):
                ensure_nodes(self, 'target', 'objective', 'value')
                return f'{base} {self.target} {self.objective} {self.value}'

            elif self.action.value in ('enable', 'get'):
                ensure_nodes(self, 'target', 'objective')
                return f'{base} {self.target} {self.objective}'

            elif self.action.value == 'list':
                if self.target is not None:
                    return f'{base} {self.target}'
                return base

            elif self.action.value == 'operation':
                ensure_nodes(self, 'target', 'objective', 'operation',
                             'source_target', 'source_objective')
                return (
                    f'{base} {self.target} {self.objective} {self.operation} '
                    f'{self.source_target} {self.source_objective}'
                )

            elif self.action.value == 'reset':
                ensure_nodes(self, 'target')
                if self.objective is not None:
                    return f'{base} {self.target} {self.objective}'
                return f'{base} {self.target}'

            elif self.action.value == 'tag':
                if self.mode.value in ('add', 'remove'):
                    ensure_nodes(self, 'name')
                    return f'{base} {self.target} {self.mode} {self.name}'
                return f'{base} {self.target} {self.mode}'

            else:
                raise ConstructionException(
                    f'expected action to be \'add\', \'remove\', \'set\', '
                    f'\'enable\', \'get\', \'list\', \'operation\' or '
                    f'\'reset\', \'tag\', not {self.action.value!r}'
                )

        elif self.category.value == 'teams':
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

            elif self.action.value == 'option':
                ensure_nodes(self, 'team', 'option', 'value')
                return f'{base} {self.team} {self.option} {self.value}'

            else:
                raise ConstructionException(
                    f'expected action to be \'add\', \'empty\', \'remove\', '
                    f'\'join\', \'leave\' or \'option\', '
                    f'not {self.action.value!r}'
                )

        else:
            raise ConstructionException(
                f'expected category to be \'objectives\', \'players\' or '
                f'\'teams\', not {self.category.value!r}'
            )


scoreboard = Command('scoreboard', parsed=ParsedScoreboardCommand)

# scoreboard objectives add <objective> <criterion> [<displayName>]
#  - scoreboard objectives add <objective> <criterion> <displayName>
scoreboard.add_variation(
    Parser(Literal('objectives'), 'category'),
    Parser(Literal('add'), 'action'),
    Parser(Objective(), 'objective'),
    Parser(Any(), 'criterion'),
    Parser(JSON(), 'name'),
)
#  - scoreboard objectives add <objective> <criterion>
scoreboard.add_variation(
    Parser(Literal('objectives'), 'category'),
    Parser(Literal('add'), 'action'),
    Parser(Objective(), 'objective'),
    Parser(Any(), 'criterion'),
)
# scoreboard objectives list
scoreboard.add_variation(
    Parser(Literal('objectives'), 'category'),
    Parser(Literal('list'), 'action'),
)
# scoreboard objectives modify <objective> displayname <displayName>
scoreboard.add_variation(
    Parser(Literal('objectives'), 'category'),
    Parser(Literal('modify'), 'action'),
    Parser(Objective(), 'objective'),
    Parser(Literal('displayname'), 'mode'),
    Parser(JSON(), 'name'),
)
# scoreboard objectives modify <objective> rendertype (hearts|integer)
scoreboard.add_variation(
    Parser(Literal('objectives'), 'category'),
    Parser(Literal('modify'), 'action'),
    Parser(Objective(), 'objective'),
    Parser(Literal('rendertype'), 'mode'),
    Parser(Union('hearts', 'integer'), 'value'),
)
# scoreboard objectives remove <objective>
scoreboard.add_variation(
    Parser(Literal('objectives'), 'category'),
    Parser(Literal('remove'), 'action'),
    Parser(Objective(), 'objective'),
)
# scoreboard objectives setdisplay <slot> [<objective>]
#  - scoreboard objectives setdisplay <slot> <objective>
scoreboard.add_variation(
    Parser(Literal('objectives'), 'category'),
    Parser(Literal('setdisplay'), 'action'),
    Parser(Any(), 'slot'),
    Parser(Objective(), 'objective'),
)
#  - scoreboard objectives setdisplay <slot>
scoreboard.add_variation(
    Parser(Literal('objectives'), 'category'),
    Parser(Literal('setdisplay'), 'action'),
    Parser(Any(), 'slot'),
)
# scoreboard players add <targets> <objective> <score>
scoreboard.add_variation(
    Parser(Literal('players'), 'category'),
    Parser(Literal('add'), 'action'),
    Parser(ScoreboardEntity(), 'target'),
    Parser(Objective(), 'objective'),
    Parser(Integer(), 'value'),
)
# scoreboard players enable <targets> <objective>
scoreboard.add_variation(
    Parser(Literal('players'), 'category'),
    Parser(Literal('enable'), 'action'),
    Parser(ScoreboardEntity(), 'target'),
    Parser(Objective(), 'objective'),
)
# scoreboard players get <target> <objective>
scoreboard.add_variation(
    Parser(Literal('players'), 'category'),
    Parser(Literal('get'), 'action'),
    Parser(ScoreboardEntity(), 'target'),
    Parser(Objective(), 'objective'),
)
# scoreboard players list [<target>]
#  - scoreboard players list <target>
scoreboard.add_variation(
    Parser(Literal('players'), 'category'),
    Parser(Literal('list'), 'action'),
    Parser(ScoreboardEntity(), 'target'),
)
#  - scoreboard players list
scoreboard.add_variation(
    Parser(Literal('players'), 'category'),
    Parser(Literal('list'), 'action'),
)
# scoreboard players operation <targets> <targetObjective> <operation>
#   <source> <sourceObjective>
scoreboard.add_variation(
    Parser(Literal('players'), 'category'),
    Parser(Literal('operation'), 'action'),
    Parser(ScoreboardEntity(), 'target'),
    Parser(Objective(), 'objective'),
    Parser(Union('+=', '-=', '*=', '/=', '%=', '=', '<', '>', '><'),
           'operation'),
    Parser(ScoreboardEntity(), 'source_target'),
    Parser(Objective(), 'source_objective'),
)
# scoreboard players remove <targets> <objective> <score>
scoreboard.add_variation(
    Parser(Literal('players'), 'category'),
    Parser(Literal('remove'), 'action'),
    Parser(ScoreboardEntity(), 'target'),
    Parser(Objective(), 'objective'),
    Parser(Integer(), 'value'),
)
# scoreboard players reset <targets> [<objective>]
#  - scoreboard players reset <targets> <objective>
scoreboard.add_variation(
    Parser(Literal('players'), 'category'),
    Parser(Literal('reset'), 'action'),
    Parser(ScoreboardEntity(), 'target'),
    Parser(Objective(), 'objective'),
)
#  - scoreboard players reset <targets>
scoreboard.add_variation(
    Parser(Literal('players'), 'category'),
    Parser(Literal('reset'), 'action'),
    Parser(ScoreboardEntity(), 'target'),
)
# scoreboard players set <targets> <objective> <score>
scoreboard.add_variation(
    Parser(Literal('players'), 'category'),
    Parser(Literal('set'), 'action'),
    Parser(ScoreboardEntity(), 'target'),
    Parser(Objective(), 'objective'),
    Parser(Integer(), 'value'),
)

# scoreboard teams add <team> [<displayName>]
#  - scoreboard teams add <team> <displayName>
scoreboard.add_variation(
    Parser(Literal('teams'), 'category'),
    Parser(Literal('add'), 'action'),
    Parser(Any(), 'team'),
    Parser(JSON(), 'name'),
)
#  - scoreboard teams add <team>
scoreboard.add_variation(
    Parser(Literal('teams'), 'category'),
    Parser(Literal('add'), 'action'),
    Parser(Any(), 'team'),
)
# scoreboard teams empty <team>
scoreboard.add_variation(
    Parser(Literal('teams'), 'category'),
    Parser(Literal('empty'), 'action'),
    Parser(Any(), 'team'),
)
# scoreboard teams join <team> [<members>]
#  - scoreboard teams join <team> <members>
scoreboard.add_variation(
    Parser(Literal('teams'), 'category'),
    Parser(Literal('join'), 'action'),
    Parser(Any(), 'team'),
    Parser(Entity(), 'target'),
)
#  - scoreboard teams join <team>
scoreboard.add_variation(
    Parser(Literal('teams'), 'category'),
    Parser(Literal('join'), 'action'),
    Parser(Any(), 'team'),
)
# scoreboard teams leave <members>
scoreboard.add_variation(
    Parser(Literal('teams'), 'category'),
    Parser(Literal('leave'), 'action'),
    Parser(Entity(), 'target'),
)
# scoreboard teams list [<team>]
#  - scoreboard teams list <team>
scoreboard.add_variation(
    Parser(Literal('teams'), 'category'),
    Parser(Literal('list'), 'action'),
    Parser(Any(), 'team'),
)
#  - scoreboard teams list
scoreboard.add_variation(
    Parser(Literal('teams'), 'category'),
    Parser(Literal('list'), 'action'),
)
# scoreboard teams option <team> <option> <value>
scoreboard.add_variation(
    Parser(Literal('teams'), 'category'),
    Parser(Literal('option'), 'action'),
    Parser(Any(), 'team'),
    Parser(Any(), 'option'),
    Parser(Any(), 'value'),
)
# scoreboard teams remove <team>
scoreboard.add_variation(
    Parser(Literal('teams'), 'category'),
    Parser(Literal('remove'), 'action'),
    Parser(Any(), 'team'),
)

# scoreboard players tag <targets> (add|remove) <name>
scoreboard.add_variation(
    Parser(Literal('players'), 'category'),
    Parser(Literal('tag'), 'action'),
    Parser(Entity(), 'target'),
    Parser(Union('add', 'remove'), 'mode'),
    Parser(Any(), 'name'),
)
# scoreboard players tag <targets> list
scoreboard.add_variation(
    Parser(Literal('players'), 'category'),
    Parser(Literal('tag'), 'action'),
    Parser(Entity(), 'target'),
    Parser(Literal('list'), 'mode')
)
