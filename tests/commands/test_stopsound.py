
from mcfunction.commands.stopsound import stopsound, ParsedStopsoundCommand
from mcfunction.nodes import EntityNode


def test_stopsound():
    parsed = stopsound.parse('stopsound @s')
    parsed: ParsedStopsoundCommand

    assert isinstance(parsed.target, EntityNode)

    assert str(parsed) == 'stopsound @s'


def test_stopsound_source():
    parsed = stopsound.parse('stopsound @s master')
    parsed: ParsedStopsoundCommand

    assert parsed.source.value == 'master'

    assert str(parsed) == 'stopsound @s master'


def test_stopsound_sound():
    parsed = stopsound.parse('stopsound @s master test:sound')
    parsed: ParsedStopsoundCommand

    assert parsed.sound.namespace == 'test'
    assert parsed.sound.name == 'sound'

    assert str(parsed) == 'stopsound @s master test:sound'
