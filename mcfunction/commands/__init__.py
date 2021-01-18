from __future__ import annotations

import importlib
from pathlib import Path
import typing as t

from ..abc import ParsedCommand
from ..exceptions import ParserException
from ..parser_types import ParserType
from ..util import tokenize


commands = []
command_lookup = {}


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

    def parse(self, command: str):
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


class Parser(t.NamedTuple):
    parser: ParserType
    destination: t.Union[None, str]


def _main():  # pragma: no cover
    # populate command list with all commands
    for path in Path(__file__).parent.iterdir():
        if (path.name == '__init__.py' or path.name.startswith('_')
                or path.suffix != '.py'):
            continue
        module = importlib.import_module(f'{__name__}.{path.stem}')
        try:
            command = getattr(module, path.stem)
        except AttributeError:
            # the command name may, for some reasons, not be a valid python
            #   identifier (reserved keywords, special characters, ...)
            command = getattr(module, 'command')

        commands.append(command)
        command_lookup[command.name] = command
        for alias in command.aliases:
            command_lookup[alias] = command


_main()
