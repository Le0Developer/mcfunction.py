
from mcfunction.versions.mc_1_8.ban_ip import ban_ip, ParsedIPBanCommand
from mcfunction.nodes import EntityNode


def test_banip():
    parsed = ban_ip.parse('ban-ip 127.0.0.1')
    parsed: ParsedIPBanCommand

    assert parsed.target.value == '127.0.0.1'
    assert parsed.reason is None

    assert str(parsed) == 'ban-ip 127.0.0.1'


def test_banip_reason():
    parsed = ban_ip.parse('ban-ip @a not passing the test')
    parsed: ParsedIPBanCommand

    assert isinstance(parsed.target, EntityNode)
    assert parsed.reason.value == 'not passing the test'

    assert str(parsed) == 'ban-ip @a not passing the test'
