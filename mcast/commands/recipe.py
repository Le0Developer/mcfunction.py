
from dataclasses import dataclass
import typing as t

from . import Command, ParsedCommand, Parser
from ..nodes import EntityNode, NamespaceIDNode, RawNode
from ..parser_types import Entity, Literal, NamespaceID, Union


@dataclass()
class ParsedRecipeCommand(ParsedCommand):
    command: str

    action: RawNode
    target: EntityNode
    recipe: t.Union[NamespaceIDNode, RawNode]

    def __str__(self):
        return f'{self.command} {self.action} {self.target} {self.recipe}'


recipe = Command('recipe', parsed=ParsedRecipeCommand)

# recipe (give|take) <targets> *
recipe.add_variation(
    Parser(Union('give', 'take'), 'action'),
    Parser(Entity(), 'target'),
    Parser(Literal('*'), 'recipe'),
)

# recipe (give|take) <targets> <recipe>
recipe.add_variation(
    Parser(Union('give', 'take'), 'action'),
    Parser(Entity(), 'target'),
    Parser(NamespaceID(), 'recipe'),
)
