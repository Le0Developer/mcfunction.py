
from mcfunction.versions.mc_1_8.help import help, ParsedHelpCommand


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
