
from mcfunction.versions.mc_1_8.stop import stop, ParsedStopCommand


def test_stop():
    parsed = stop.parse('stop')
    parsed: ParsedStopCommand

    assert str(parsed) == 'stop'
