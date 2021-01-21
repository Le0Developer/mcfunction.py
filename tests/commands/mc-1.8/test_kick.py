
from mcfunction.versions.mc_1_8.kick import kick, ParsedKickCommand
from mcfunction.nodes import EntityNode


def test_kick():
    parsed = kick.parse('kick @a')
    parsed: ParsedKickCommand

    assert isinstance(parsed.target, EntityNode)
    assert parsed.reason is None

    assert str(parsed) == 'kick @a'


def test_kick_reason():
    parsed = kick.parse('kick @a not passing the test')
    parsed: ParsedKickCommand

    assert parsed.reason.value == 'not passing the test'

    assert str(parsed) == 'kick @a not passing the test'
