
from mcfunction.versions.mc_1_14.teammsg import teammsg, ParsedTeammsgCommand


def test_teammsg():
    parsed = teammsg.parse('teammsg test successful')
    parsed: ParsedTeammsgCommand

    assert parsed.message.value == 'test successful'

    assert str(parsed) == 'teammsg test successful'
