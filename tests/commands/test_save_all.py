
from mcfunction.commands.save_all import save_all, ParsedSaveAllCommand


def test_save_all():
    parsed = save_all.parse('save-all')
    parsed: ParsedSaveAllCommand

    assert parsed.flush is None

    assert str(parsed) == 'save-all'


def test_save_all_flush():
    parsed = save_all.parse('save-all flush')
    parsed: ParsedSaveAllCommand

    assert parsed.flush.value == 'flush'

    assert str(parsed) == 'save-all flush'
