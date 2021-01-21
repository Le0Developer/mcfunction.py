
from mcfunction.versions.mc_1_8.pardon import pardon, ParsedPardonCommand
from mcfunction.nodes import EntityNode


def test_pardon():
    parsed = pardon.parse('pardon @s')
    parsed: ParsedPardonCommand

    assert isinstance(parsed.target, EntityNode)

    assert str(parsed) == 'pardon @s'
