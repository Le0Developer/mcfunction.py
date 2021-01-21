
from mcfunction.versions.mc_1_8.toggledownfall import (
    toggledownfall, ParsedToggledownfallCommand
)


def test_toggledownfall():
    parsed = toggledownfall.parse('toggledownfall')
    parsed: ParsedToggledownfallCommand

    assert str(parsed) == 'toggledownfall'
