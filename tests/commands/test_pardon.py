
from mcast.commands.pardon import pardon, ParsedPardonCommand
from mcast.nodes import EntityNode


def test_pardon():
    parsed = pardon.parse('pardon @s')
    parsed: ParsedPardonCommand

    assert isinstance(parsed.target, EntityNode)

    assert str(parsed) == 'pardon @s'
