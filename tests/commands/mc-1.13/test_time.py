
from mcfunction.versions.mc_1_13.time import time, ParsedTimeCommand


def test_time_add():
    parsed = time.parse('time add 69')
    parsed: ParsedTimeCommand

    assert parsed.action.value == 'add'
    assert parsed.time.value == '69'

    assert str(parsed) == 'time add 69'


def test_time_query():
    parsed = time.parse('time query day')
    parsed: ParsedTimeCommand

    assert parsed.action.value == 'query'
    assert parsed.time.value == 'day'

    assert str(parsed) == 'time query day'


def test_time_set():
    parsed = time.parse('time set noon')
    parsed: ParsedTimeCommand

    assert parsed.action.value == 'set'
    assert parsed.time.value == 'noon'

    assert str(parsed) == 'time set noon'
