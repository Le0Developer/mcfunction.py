from __future__ import annotations

import importlib.util
from pathlib import Path
import typing as t

from ..abc import ParsedCommand
from ..exceptions import ParserException
from ..parser_types import ParserType
from ..util import tokenize


class MinecraftVersion:
    def __init__(self, version: str, module: str,
                 removed_commands: t.Set[str] = None):
        self.version = version
        self.module = module
        self.commands = []
        self.command_lookup = {}

        if removed_commands is None:
            removed_commands = set()
        self.removed_commands = removed_commands

    def populate_commands(self):  # pragma: no cover
        spec = importlib.util.find_spec(self.module)
        origin = Path(spec.origin).parent
        for file in origin.iterdir():
            if (file.name == '__init__.py' or file.name.startswith('_')
                    or file.suffix != '.py' or not file.is_file()):
                continue
            module = importlib.import_module(f'{self.module}.{file.stem}')
            try:
                command = getattr(module, file.stem)
            except AttributeError:
                # the command name may, for some reasons, not be a valid python
                #   identifier (reserved keywords, special characters, ...)
                command = getattr(module, 'command')

            self.add_command(command)

    def add_command(self, command: Command):
        if command not in self.commands:
            self.commands.append(command)
        self.command_lookup[command.name] = command
        for alias in command.aliases:
            self.command_lookup[alias] = command

    def get_command(self, name: str):
        if name in self.command_lookup:
            return self.command_lookup[name]
        elif name in self.removed_commands:
            return None

        found_myself = False
        for version in VERSIONS:
            if version.version == self.version:
                found_myself = True
            elif found_myself:
                if name in version.command_lookup:
                    return version.command_lookup[name]
                elif name in version.removed_commands:
                    return None


class Parser(t.NamedTuple):
    parser: ParserType
    destination: t.Union[None, str]


class Command:
    variations: t.List[t.Tuple[Parser, ...]]

    def __init__(self, name: str, aliases: t.List[str] = None, *,
                 parsed: t.Callable[..., ParsedCommand],
                 commandblock: bool = True):
        self.name = name
        if aliases is None:
            aliases = []
        self.aliases = aliases
        self.variations = []

        self.commandblock = commandblock
        self.parsed = parsed

    def add_variation(self, *parsers: Parser):
        self.variations.append(parsers)

    def parse(self, command: str, version: MinecraftVersion = None):
        exception = None
        exception_dept = -1
        for variation in self.variations:
            parts = tokenize(command, ' ')
            result = {'command': next(parts)}
            for no, parser in enumerate(variation):
                try:
                    node = parser.parser.parse(parts)
                except ParserException as exc:
                    if no > exception_dept:
                        exception = exc
                        exception_dept = no
                    break
                except StopIteration:
                    if no > exception_dept:
                        exception = ParserException('too few arguments')
                        exception_dept = no
                    break
                else:
                    if parser.destination:
                        result[parser.destination] = node

            else:
                try:
                    # ensure list is empty and all arguments have been parsed
                    next(parts)
                except StopIteration:
                    return self.parsed(**result)
                else:
                    if len(variation) > exception_dept:
                        exception = ParserException('invalid syntax')
                        exception_dept = len(variation)
                    continue

        if exception is None:  # pragma: no cover
            raise ParserException('should not happen')
        raise exception  # pragma: no cover


VERSIONS = [
    MinecraftVersion('1.16', 'mcfunction.versions.mc_1_16'),
    MinecraftVersion('1.15', 'mcfunction.versions.mc_1_15'),
    MinecraftVersion('1.14', 'mcfunction.versions.mc_1_14'),
    MinecraftVersion('1.13', 'mcfunction.versions.mc_1_13',
                     removed_commands={'blockdata', 'entitydata', 'stats',
                                       'toggledownfall'}),
    MinecraftVersion('1.12', 'mcfunction.versions.mc_1_12',
                     removed_commands={'achievement'}),
    MinecraftVersion('1.11', 'mcfunction.versions.mc_1_11'),
    MinecraftVersion('1.10', 'mcfunction.versions.mc_1_10'),
    MinecraftVersion('1.9', 'mcfunction.versions.mc_1_9'),
    MinecraftVersion('1.8', 'mcfunction.versions.mc_1_8'),
]


def get_version(version: str = None):
    if version is None:
        return VERSIONS[0]

    for ver in VERSIONS:
        if ver.version == version:
            return ver


def _main():
    for version in VERSIONS:
        version.populate_commands()
