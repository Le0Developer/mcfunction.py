
from dataclasses import dataclass
import typing as t

from .versions import MinecraftVersion
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

    @classmethod
    def _parse_line(cls, command: str, version: MinecraftVersion = None):
        from .parser import parse_command  # circular import :/

        if not command:  # empty line
            return NoCommand('')
        elif command.startswith('# '):
            return NoCommand(
                command='# ',
                comment=RawNode(command[2:])
            )
        elif command.startswith('#'):
            return NoCommand(
                command='#',
                comment=RawNode(command[1:])
            )

        return parse_command(command, version)

    @classmethod
    def parse(cls: t.Type[T], lines: t.List[str],
              version: MinecraftVersion = None) -> T:
        commands = []
        for command in lines:
            commands.append(cls._parse_line(command.strip(), version))

        return cls(commands)

    @classmethod
    def load(cls, fp: t.TextIO, version: MinecraftVersion = None):
        commands = []
        while True:
            line = fp.readline()
            if not line:
                break
            commands.append(cls._parse_line(line.strip(), version))

        return cls(commands)

    @classmethod
    def loads(cls, string: str, version: MinecraftVersion = None):
        commands = []
        while True:
            next = string.find('\n')
            print(next, string)
            line = string[:next if next >= 0 else None]
            commands.append(cls._parse_line(line.strip(), version))
            if next < 0:
                break
            string = string[next + 1:]

        return cls(commands)

    def dump(self, fp: t.TextIO):
        for i, command in enumerate(self.commands):
            fp.write(str(command))
            if i != len(self.commands) - 1:
                fp.write('\n')

    def dumps(self):
        return '\n'.join(str(cmd) for cmd in self.commands)

    def __str__(self):
        return self.dumps()
