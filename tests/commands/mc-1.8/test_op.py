
from mcfunction.versions.mc_1_8.op import op, ParsedOpCommand
from mcfunction.nodes import EntityNode


def test_op():
    parsed = op.parse('op @s')
    parsed: ParsedOpCommand

    assert isinstance(parsed.target, EntityNode)

    assert str(parsed) == 'op @s'
