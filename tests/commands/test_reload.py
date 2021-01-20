
from mcfunction.versions.mc_1_12.reload import reload, ParsedReloadCommand


def test_reload():
    parsed = reload.parse('reload')
    parsed: ParsedReloadCommand

    assert str(parsed) == 'reload'
