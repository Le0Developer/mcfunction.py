
from mcast.commands.time import time, ParsedTimeCommand


def test_time_add():
    parsed = time.parse('time add 69')
    parsed: ParsedTimeCommand

    assert parsed.action.value == 'add'
    assert parsed.time.value == '69'

    assert str(parsed) == 'time add 69'


def test_time_query():
    parsed = time.parse('time query gametime')
    parsed: ParsedTimeCommand

    assert parsed.action.value == 'query'
    assert parsed.time.value == 'gametime'

    assert str(parsed) == 'time query gametime'


def test_time_set():
    parsed = time.parse('time set 69')
    parsed: ParsedTimeCommand

    assert parsed.action.value == 'set'
    assert parsed.time.value == '69'
