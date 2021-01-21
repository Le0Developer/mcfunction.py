
from mcfunction.versions.mc_1_8.spreadplayers import (
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
