
from mcfunction.versions.mc_1_8.debug import debug, ParsedDebugCommand


def test_debug():
    parsed = debug.parse('debug start')
    parsed: ParsedDebugCommand

    assert parsed.action.value == 'start'

    assert str(parsed) == 'debug start'
