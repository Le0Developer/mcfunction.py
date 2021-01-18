
from mcfunction.commands.save_off import save_off, ParsedSaveOffCommand


def test_save_off():
    parsed = save_off.parse('save-off')
    parsed: ParsedSaveOffCommand

    assert str(parsed) == 'save-off'
