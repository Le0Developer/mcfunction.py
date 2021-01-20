
from dataclasses import dataclass

from .. import Command, ParsedCommand, Parser
from ...nodes import RawNode
from ...parser_types import Literal


@dataclass()
class ParsedSaveAllCommand(ParsedCommand):
    command: str

    flush: RawNode = None

    def __str__(self):
        if self.flush is not None:
            return f'{self.command} {self.flush}'
        return self.command


save_all = Command('save-all', commandblock=False, parsed=ParsedSaveAllCommand)

# save-all
save_all.add_variation()

# save-all flush
save_all.add_variation(
    Parser(Literal('flush'), 'flush'),
)
