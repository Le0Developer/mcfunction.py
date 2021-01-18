
from mcfunction.commands.reload import reload, ParsedReloadCommand


def test_reload():
    parsed = reload.parse('reload')
    parsed: ParsedReloadCommand

    assert str(parsed) == 'reload'
