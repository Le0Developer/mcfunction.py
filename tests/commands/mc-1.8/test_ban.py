
from mcfunction.versions.mc_1_8.ban import ban, ParsedBanCommand
from mcfunction.nodes import EntityNode


def test_ban():
    parsed = ban.parse('ban @a')
    parsed: ParsedBanCommand

    assert isinstance(parsed.target, EntityNode)
    assert parsed.reason is None

    assert str(parsed) == 'ban @a'


def test_ban_reason():
    parsed = ban.parse('ban @a not passing the test')
    parsed: ParsedBanCommand

    assert parsed.reason.value == 'not passing the test'

    assert str(parsed) == 'ban @a not passing the test'
