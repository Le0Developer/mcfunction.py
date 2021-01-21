
from mcfunction.versions.mc_1_8.setidletimeout import (
    setidletimeout, ParsedSetidletimeoutCommand
)


def test_setidletimeout():
    parsed = setidletimeout.parse('setidletimeout 5')
    parsed: ParsedSetidletimeoutCommand

    assert parsed.minutes.value == 5

    assert str(parsed) == 'setidletimeout 5'
