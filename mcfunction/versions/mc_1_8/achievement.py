
from dataclasses import dataclass
import typing as t

from .. import Command, ParsedCommand, Parser
from ...nodes import EntityNode, NamespaceIDNode, RawNode
from ...parser_types import Entity, Literal, NamespaceID, Union


@dataclass()
class ParsedAchievementCommand(ParsedCommand):
    command: str

    action: RawNode
    achievement: t.Union[NamespaceIDNode, RawNode]
    target: EntityNode = None

    def __str__(self):
        base = f'{self.command} {self.action} {self.achievement}'
        if self.target is not None:
            return f'{base} {self.target}'
        return base


achievement = Command('achievement', parsed=ParsedAchievementCommand)

# achievement (give|take) (<achievement>|*) [<target>]
#  - achievement (give|take) (<achievement>|*) <target>
achievement.add_variation(
    Parser(Union('give', 'take'), 'action'),
    Parser(Literal('*'), 'achievement'),
    Parser(Entity(), 'target'),
)
achievement.add_variation(
    Parser(Union('give', 'take'), 'action'),
    Parser(NamespaceID(), 'achievement'),
    Parser(Entity(), 'target'),
)
#  - achievement (give|take) (<achievement>|*)
achievement.add_variation(
    Parser(Union('give', 'take'), 'action'),
    Parser(Literal('*'), 'achievement'),
)
achievement.add_variation(
    Parser(Union('give', 'take'), 'action'),
    Parser(NamespaceID(), 'achievement'),
)
