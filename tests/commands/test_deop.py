
from mcfunction.commands.deop import deop, ParsedDeopCommand
from mcfunction.nodes import EntityNode


def test_deop():
    parsed = deop.parse('deop @s')
    parsed: ParsedDeopCommand

    assert isinstance(parsed.target, EntityNode)

    assert str(parsed) == 'deop @s'
