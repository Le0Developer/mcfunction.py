
from dataclasses import dataclass
import typing as t

from .. import Command, ParsedCommand, Parser
from ...exceptions import ConstructionException
from ...nodes import EntityNode, PositionNode, RawNode
from ...parser_types import (
    Entity, Literal, Objective, Position, ScoreboardEntity, Union
)
from ...util import ensure_nodes


@dataclass()
class ParsedStatsCommand(ParsedCommand):
    command: str

    target_type: RawNode
    target: t.Union[EntityNode, PositionNode]
    mode: RawNode
    stat: RawNode
    selector: EntityNode = None
    objective: RawNode = None

    def __str__(self):
        base = f'{self.command} {self.target_type} {self.target} ' \
               f'{self.mode} {self.stat}'
        if self.mode.value == 'clear':
            return base
        elif self.mode.value == 'set':
            ensure_nodes(self, 'selector', 'objective')
            return f'{base} {self.selector} {self.objective}'
        else:
            raise ConstructionException(
                f'expected mode to be \'clear\' or \'set\', '
                f'not {self.mode.value!r}'
            )


stats = Command('stats', parsed=ParsedStatsCommand)

STATS = Union('AffectedBlocks', 'AffectedEntities', 'AffectedItems',
              'QueryResult', 'SuccessCount')

# stats block <x> <y> <z> clear <stat>
stats.add_variation(
    Parser(Literal('block'), 'target_type'),
    Parser(Position(), 'target'),
    Parser(Literal('clear'), 'mode'),
    Parser(STATS, 'stat')
)
# stats block <x> <y> <z> set <stat> <selector> <objective>
stats.add_variation(
    Parser(Literal('block'), 'target_type'),
    Parser(Position(), 'target'),
    Parser(Literal('set'), 'mode'),
    Parser(STATS, 'stat'),
    Parser(ScoreboardEntity(), 'selector'),
    Parser(Objective(), 'objective')
)
# stats entity <selector2> clear <stat>
stats.add_variation(
    Parser(Literal('entity'), 'target_type'),
    Parser(Entity(), 'target'),
    Parser(Literal('clear'), 'mode'),
    Parser(STATS, 'stat')
)
# stats entity <selector2> set <stat> <selector> <objective>
stats.add_variation(
    Parser(Literal('entity'), 'target_type'),
    Parser(Entity(), 'target'),
    Parser(Literal('set'), 'mode'),
    Parser(STATS, 'stat'),
    Parser(ScoreboardEntity(), 'selector'),
    Parser(Objective(), 'objective')
)
