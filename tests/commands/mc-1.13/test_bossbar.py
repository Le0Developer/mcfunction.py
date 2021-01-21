
from mcfunction.versions.mc_1_13.bossbar import bossbar, ParsedBossbarCommand


def test_bossbar_add():
    parsed = bossbar.parse('bossbar add test:bossbar {"text":"test ok!"}')
    parsed: ParsedBossbarCommand

    assert parsed.action.value == 'add'
    assert parsed.id.namespace == 'test'
    assert parsed.id.name == 'bossbar'
    assert parsed.name.object == {'text': 'test ok!'}

    assert str(parsed) == 'bossbar add test:bossbar {"text":"test ok!"}'


def test_bossbar_get():
    parsed = bossbar.parse('bossbar get test:bossbar value')
    parsed: ParsedBossbarCommand

    assert parsed.action.value == 'get'
    assert parsed.setting.value == 'value'

    assert str(parsed) == 'bossbar get test:bossbar value'


def test_bossbar_list():
    parsed = bossbar.parse('bossbar list')
    parsed: ParsedBossbarCommand

    assert parsed.action.value == 'list'

    assert str(parsed) == 'bossbar list'


def test_bossbar_remove():
    parsed = bossbar.parse('bossbar remove test:bossbar')
    parsed: ParsedBossbarCommand

    assert parsed.action.value == 'remove'

    assert str(parsed) == 'bossbar remove test:bossbar'


def test_bossbar_set_value():
    parsed = bossbar.parse('bossbar set test:bossbar value 1337')
    parsed: ParsedBossbarCommand

    assert parsed.action.value == 'set'
    assert parsed.setting.value == 'value'
    assert parsed.value.value == 1337

    assert str(parsed) == 'bossbar set test:bossbar value 1337'


def test_bossbar_set_players():
    parsed = bossbar.parse('bossbar set test:bossbar players')
    parsed: ParsedBossbarCommand

    assert parsed.action.value == 'set'
    assert parsed.setting.value == 'players'
    assert parsed.value is None

    assert str(parsed) == 'bossbar set test:bossbar players'
