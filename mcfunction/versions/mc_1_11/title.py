
from dataclasses import dataclass

from .. import Command, ParsedCommand, Parser
from ...exceptions import ConstructionException
from ...nodes import EntityNode, IntegerNode, JSONNode, RawNode
from ...parser_types import Entity, Integer, JSON, Literal, Union


@dataclass()
class ParsedTitleCommand(ParsedCommand):
    command: str

    target: EntityNode
    action: RawNode

    title: JSONNode = None
    fadein: IntegerNode = None
    stay: IntegerNode = None
    fadeout: IntegerNode = None

    def __str__(self):
        base = f'{self.command} {self.target} {self.action}'
        if self.action.value in ('clear', 'reset'):
            return base
        elif self.action.value in ('title', 'subtitle', 'actionbar'):
            return f'{base} {self.title}'
        elif self.action.value == 'times':
            return f'{base} {self.fadein} {self.stay} {self.fadeout}'
        else:
            raise ConstructionException(
                f'expected action to be \'clear\', \'reset\', \'title\', '
                f'\'subtitle\', \'actionbar\' or \'times\', '
                f'not {self.action.value!r}'
            )


title = Command('title', parsed=ParsedTitleCommand)

# title <targets> (clear|reset)
title.add_variation(
    Parser(Entity(), 'target'),
    Parser(Union('clear', 'reset'), 'action'),
)
# title <targets> (title|subtitle|actionbar) <title>
title.add_variation(
    Parser(Entity(), 'target'),
    Parser(Union('title', 'subtitle', 'actionbar'), 'action'),
    Parser(JSON(), 'title'),
)
# title <targets> times <fadeIn> <stay> <fadeOut>
title.add_variation(
    Parser(Entity(), 'target'),
    Parser(Literal('times'), 'action'),
    Parser(Integer(), 'fadein'),
    Parser(Integer(), 'stay'),
    Parser(Integer(), 'fadeout'),
)
