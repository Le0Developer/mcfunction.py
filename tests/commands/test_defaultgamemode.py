
from mcfunction.versions.mc_1_8.defaultgamemode import (
    defaultgamemode, ParsedDefaultgamemodeCommand
)


def test_defaultgamemode():
    parsed = defaultgamemode.parse('defaultgamemode creative')
    parsed: ParsedDefaultgamemodeCommand

    assert parsed.gamemode.value == 'creative'

    assert str(parsed) == 'defaultgamemode creative'
