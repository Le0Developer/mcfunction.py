
from dataclasses import dataclass
import typing as t

from .abc import ParsedCommand
from .nodes import RawNode


T = t.TypeVar('T')


@dataclass()
class NoCommand(ParsedCommand):
    command: str  # by ParsedCommand

    comment: RawNode = None

    def __str__(self):
        if self.comment is not None:
            return f'{self.command}{self.comment}'
        return self.command


@dataclass()
class McFunction:
    commands: t.List[ParsedCommand]

    def __str__(self):
        return '\n'.join(str(cmd) for cmd in self.commands)

    @classmethod
    def parse(cls: t.Type[T], lines: t.List[str]) -> T:
        from .parser import parse_command  # circular import :/

        commands = []
        for command in (x.strip() for x in lines):
            if not command:  # empty line
                commands.append(NoCommand(''))
            elif command.startswith('# '):
                commands.append(NoCommand(
                    command='# ',
                    comment=RawNode(command[2:])
                ))
            elif command.startswith('#'):
                commands.append(NoCommand(
                    command='#',
                    comment=RawNode(command[1:])
                ))
            else:
                commands.append(parse_command(command))

        return cls(commands)
