
from mcfunction.versions.mc_1_8.save_off import save_off, ParsedSaveOffCommand


def test_save_off():
    parsed = save_off.parse('save-off')
    parsed: ParsedSaveOffCommand

    assert str(parsed) == 'save-off'
