
from mcfunction.versions.mc_1_8.summon import summon, ParsedSummonCommand
from mcfunction.nodes import PositionNode


def test_summon():
    parsed = summon.parse('summon test:entity')
    parsed: ParsedSummonCommand

    assert parsed.entity.namespace == 'test'
    assert parsed.entity.name == 'entity'

    assert str(parsed) == 'summon test:entity'


def test_summon_position():
    parsed = summon.parse('summon test:entity 0 0 0')
    parsed: ParsedSummonCommand

    assert isinstance(parsed.position, PositionNode)

    assert str(parsed) == 'summon test:entity 0 0 0'


def test_summon_nbt():
    parsed = summon.parse('summon test:entity 0 0 0 {NoGravity:1b}')
    parsed: ParsedSummonCommand

    assert parsed.nbt.value == '{NoGravity:1b}'

    assert str(parsed) == 'summon test:entity 0 0 0 {NoGravity:1b}'
