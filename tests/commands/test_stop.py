
from mcast.commands.stop import stop, ParsedStopCommand


def test_stop():
    parsed = stop.parse('stop')
    parsed: ParsedStopCommand

    assert str(parsed) == 'stop'
