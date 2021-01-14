
from dataclasses import dataclass

from . import Command, ParsedCommand, Parser
from ..exceptions import ConstructionException
from ..nodes import EntityNode, IntegerNode, NamespaceIDNode, RawNode
from ..parser_types import Entity, Integer, Literal, NamespaceID, Union
from ..util import ensure_nodes


@dataclass()
class ParsedEffectCommand(ParsedCommand):
    command: str

    action: RawNode

    target: EntityNode = None
    effect: NamespaceIDNode = None

    seconds: IntegerNode = None
    amplifier: IntegerNode = None
    hide_particles: RawNode = None

    def __str__(self):
        base = f'{self.command} {self.action}'
        if self.action.value == 'clear':
            if self.target is not None:
                if self.effect is not None:
                    return f'{base} {self.target} {self.effect}'
                return f'{base} {self.target}'
            return base

        elif self.action.value == 'give':
            ensure_nodes(self, 'target', 'effect')
            command = f'{base} {self.target} {self.effect}'
            if self.seconds is None:
                return command
            elif self.amplifier is None:
                return f'{command} {self.seconds}'
            elif self.hide_particles is None:
                return f'{command} {self.seconds} {self.amplifier}'
            return f'{command} {self.seconds} {self.amplifier} ' \
                   f'{self.hide_particles}'

        else:
            raise ConstructionException(
                f'expected action to be \'clear\' or \'give\', '
                f'not {self.action.value!r}'
            )


effect = Command('effect', parsed=ParsedEffectCommand)

# effect clear [<targets>] [<effect>]
#  - effect clear <targets> <effect>
effect.add_variation(
    Parser(Literal('clear'), 'action'),
    Parser(Entity(), 'target'),
    Parser(NamespaceID(), 'effect'),
)
#  - effect clear <targets>
effect.add_variation(
    Parser(Literal('clear'), 'action'),
    Parser(Entity(), 'target'),
)
#  - effect clear
effect.add_variation(
    Parser(Literal('clear'), 'action'),
)

# effect give <targets> <effect> [<seconds>] [<amplifier>] [<hideParticles>]
#  - effect give <targets> <effect> <seconds> <amplifier> <hideParticles>
effect.add_variation(
    Parser(Literal('give'), 'action'),
    Parser(Entity(), 'target'),
    Parser(NamespaceID(), 'effect'),
    Parser(Integer(), 'seconds'),
    Parser(Integer(), 'amplifier'),
    Parser(Union('true', 'false'), 'hide_particles'),
)
#  - effect give <targets> <effect> <seconds> <amplifier>
effect.add_variation(
    Parser(Literal('give'), 'action'),
    Parser(Entity(), 'target'),
    Parser(NamespaceID(), 'effect'),
    Parser(Integer(), 'seconds'),
    Parser(Integer(), 'amplifier'),
)
#  - effect give <targets> <effect> <seconds>
effect.add_variation(
    Parser(Literal('give'), 'action'),
    Parser(Entity(), 'target'),
    Parser(NamespaceID(), 'effect'),
    Parser(Integer(), 'seconds'),
)
#  - effect give <targets> <effect>
effect.add_variation(
    Parser(Literal('give'), 'action'),
    Parser(Entity(), 'target'),
    Parser(NamespaceID(), 'effect'),
)
