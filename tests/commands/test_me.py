
from mcfunction.versions.mc_1_8.me import me, ParsedMeCommand


def test_me():
    parsed = me.parse('me test successful')
    parsed: ParsedMeCommand

    assert parsed.message.value == 'test successful'

    assert str(parsed) == 'me test successful'
