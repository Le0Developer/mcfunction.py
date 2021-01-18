
from mcfunction.commands.spreadplayers import (
    spreadplayers, ParsedSpreadplayersCommand
)
from mcfunction.nodes import EntityNode, Position2dNode


def test_spreadplayers():
    parsed = spreadplayers.parse('spreadplayers 0 0 1 2 false @s')
    parsed: ParsedSpreadplayersCommand

    assert isinstance(parsed.center, Position2dNode)
    assert parsed.distance.value == 1
    assert parsed.range.value == 2
    assert parsed.teams.value == 'false'
    assert isinstance(parsed.target, EntityNode)

    assert str(parsed) == 'spreadplayers 0 0 1 2 false @s'


def test_spreadplayers_height():
    parsed = spreadplayers.parse('spreadplayers 0 0 1 2 under 69 false @s')
    parsed: ParsedSpreadplayersCommand

    assert parsed.under.value == 'under'
    assert parsed.height.value == 69

    assert str(parsed) == 'spreadplayers 0 0 1 2 under 69 false @s'
