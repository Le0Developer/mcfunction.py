
from mcfunction.commands.banlist import banlist, ParsedBanlistCommand


def test_banlist():
    parsed = banlist.parse('banlist')
    parsed: ParsedBanlistCommand

    assert parsed.mode is None

    assert str(parsed) == 'banlist'


def test_banlist_ips():
    parsed = banlist.parse('banlist ips')
    parsed: ParsedBanlistCommand

    assert parsed.mode.value == 'ips'

    assert str(parsed) == 'banlist ips'
