
from mcast.commands.gamerule import gamerule, ParsedGameruleCommand


def test_gamerule():
    parsed = gamerule.parse('gamerule doTestFail')
    parsed: ParsedGameruleCommand

    assert parsed.rule.value == 'doTestFail'

    assert str(parsed) == 'gamerule doTestFail'


def test_gamerule_set():
    parsed = gamerule.parse('gamerule doTestFail false')
    parsed: ParsedGameruleCommand

    assert parsed.rule.value == 'doTestFail'
    assert parsed.value.value == 'false'  # hopefully

    assert str(parsed) == 'gamerule doTestFail false'
