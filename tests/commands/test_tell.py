
from mcast.commands.tell import tell, ParsedTellCommand
from mcast.nodes import EntityNode


def test_tell():
    parsed = tell.parse('tell @s test successful')
    parsed: ParsedTellCommand

    assert isinstance(parsed.target, EntityNode)
    assert parsed.message.value == 'test successful'

    assert str(parsed) == 'tell @s test successful'
