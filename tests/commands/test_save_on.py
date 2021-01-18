
from mcfunction.commands.save_on import save_on, ParsedSaveOnCommand


def test_save_on():
    parsed = save_on.parse('save-on')
    parsed: ParsedSaveOnCommand

    assert str(parsed) == 'save-on'
