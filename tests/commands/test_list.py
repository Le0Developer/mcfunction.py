
from mcast.commands.list import list, ParsedListCommand


def test_list():
    parsed = list.parse('list')
    parsed: ParsedListCommand

    assert parsed.uuids is None

    assert str(parsed) == 'list'


def test_list_uuids():
    parsed = list.parse('list uuids')
    parsed: ParsedListCommand

    assert parsed.uuids.value == 'uuids'

    assert str(parsed) == 'list uuids'
