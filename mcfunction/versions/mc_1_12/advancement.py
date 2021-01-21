
from dataclasses import dataclass

from .. import Command, ParsedCommand, Parser
from ...nodes import EntityNode, NamespaceIDNode, RawNode
from ...parser_types import Any, Entity, Literal, NamespaceID, Union


@dataclass()
class ParsedAdvancementCommand(ParsedCommand):
    command: str

    action: RawNode
    target: EntityNode
    mode: RawNode = None
    advancement: NamespaceIDNode = None
    criterion: RawNode = None

    def __str__(self):
        if self.action.value == 'test':
            base = f'{self.command} {self.action} {self.target}'
            if self.criterion is not None:
                return f'{base} {self.advancement} {self.criterion}'
            return f'{base} {self.advancement}'

        base = f'{self.command} {self.action} {self.target} {self.mode}'
        if self.advancement is not None:
            if self.criterion is not None:
                return f'{base} {self.advancement} {self.criterion}'
            return f'{base} {self.advancement}'
        return base


advancement = Command('advancement', parsed=ParsedAdvancementCommand)

# advancement (grant|revoke) <targets> everything
advancement.add_variation(
    Parser(Union('grant', 'revoke'), 'action'),
    Parser(Entity(), 'target'),
    Parser(Literal('everything'), 'mode'),
)

# advancement (grant|revoke) <targets> only <advancement> <criterion>
advancement.add_variation(
    Parser(Union('grant', 'revoke'), 'action'),
    Parser(Entity(), 'target'),
    Parser(Literal('only'), 'mode'),
    Parser(NamespaceID(), 'advancement'),
    Parser(Any(), 'criterion'),
)
# advancement (grant|revoke) <targets> (only|from|through|until)
#   <advancement>
advancement.add_variation(
    Parser(Union('grant', 'revoke'), 'action'),
    Parser(Entity(), 'target'),
    Parser(Union('only', 'from', 'through', 'until'), 'mode'),
    Parser(NamespaceID(), 'advancement'),
)

# advancement test <targets> <advancement> [<criterion>]
#  - advancement test <targets> <advancement> <criterion>
advancement.add_variation(
    Parser(Literal('test'), 'action'),
    Parser(Entity(), 'target'),
    Parser(NamespaceID(), 'advancement'),
    Parser(Any(), 'criterion'),
)

#  - advancement test <targets> <advancement>
advancement.add_variation(
    Parser(Literal('test'), 'action'),
    Parser(Entity(), 'target'),
    Parser(NamespaceID(), 'advancement'),
)
