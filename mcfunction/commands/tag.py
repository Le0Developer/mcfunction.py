
from dataclasses import dataclass

from . import Command, ParsedCommand, Parser
from ..nodes import EntityNode, RawNode
from ..parser_types import Any, Entity, Literal, Union
from ..util import ensure_nodes


@dataclass()
class ParsedTagCommand(ParsedCommand):
    command: str

    target: EntityNode
    action: RawNode

    name: RawNode = None

    def __str__(self):
        base = f'{self.command} {self.target} {self.action}'
        if self.action.value in ('add', 'remove'):
            ensure_nodes(self, 'name')
            return f'{base} {self.name}'
        return base


tag = Command('tag', parsed=ParsedTagCommand)

# tag <targets> (add|remove) <name>
tag.add_variation(
    Parser(Entity(), 'target'),
    Parser(Union('add', 'remove'), 'action'),
    Parser(Any(), 'name'),
)
# tag <targets> list
tag.add_variation(
    Parser(Entity(), 'target'),
    Parser(Literal('list'), 'action')
)
