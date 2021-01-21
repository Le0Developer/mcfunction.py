
from mcfunction.versions.mc_1_13.kill import kill, ParsedKillCommand
from mcfunction.nodes import EntityNode


def test_kill_target():
    parsed = kill.parse('kill @e')
    parsed: ParsedKillCommand

    assert isinstance(parsed.target, EntityNode)

    assert str(parsed) == 'kill @e'
