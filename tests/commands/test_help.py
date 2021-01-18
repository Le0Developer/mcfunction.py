
from mcfunction.commands.help import help, ParsedHelpCommand


def test_help():
    parsed = help.parse('help')
    parsed: ParsedHelpCommand

    assert parsed.cmd is None

    assert str(parsed) == 'help'


def test_help_command():
    parsed = help.parse('help help')
    parsed: ParsedHelpCommand

    assert parsed.cmd.value == 'help'

    assert str(parsed) == 'help help'
