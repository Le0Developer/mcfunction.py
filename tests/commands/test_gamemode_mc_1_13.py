
from mcfunction.versions.mc_1_13.gamemode import (
    gamemode, ParsedGamemodeCommand
)
from mcfunction.nodes import EntityNode


def test_gamemode():
    parsed = gamemode.parse('gamemode creative')
    parsed: ParsedGamemodeCommand

    assert parsed.gamemode.value == 'creative'

    assert str(parsed) == 'gamemode creative'


def test_gamemode_target():
    parsed = gamemode.parse('gamemode creative @a')
    parsed: ParsedGamemodeCommand

    assert isinstance(parsed.target, EntityNode)

    assert str(parsed) == 'gamemode creative @a'
