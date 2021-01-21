
from mcfunction.versions.mc_1_15.spectate import (
    spectate, ParsedSpectateCommand
)
from mcfunction.nodes import EntityNode


def test_specate():
    parsed = spectate.parse('spectate')
    parsed: ParsedSpectateCommand

    assert str(parsed) == 'spectate'


def test_spectate_target():
    parsed = spectate.parse('spectate @s')
    parsed: ParsedSpectateCommand

    assert isinstance(parsed.target, EntityNode)

    assert str(parsed) == 'spectate @s'


def test_spectate_player():
    parsed = spectate.parse('spectate @s @s')
    parsed: ParsedSpectateCommand

    assert isinstance(parsed.target, EntityNode)
    assert isinstance(parsed.player, EntityNode)

    assert str(parsed) == 'spectate @s @s'
