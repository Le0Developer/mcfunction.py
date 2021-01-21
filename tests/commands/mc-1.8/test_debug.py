
from mcfunction.versions.mc_1_8.debug import debug, ParsedDebugCommand
from mcfunction.nodes import PositionNode


def test_debug():
    parsed = debug.parse('debug start')
    parsed: ParsedDebugCommand

    assert parsed.action.value == 'start'

    assert str(parsed) == 'debug start'


def test_debug_chunk():
    parsed = debug.parse('debug chunk 0 0 0')
    parsed: ParsedDebugCommand

    assert parsed.action.value == 'chunk'
    assert isinstance(parsed.position, PositionNode)

    assert str(parsed) == 'debug chunk 0 0 0'
