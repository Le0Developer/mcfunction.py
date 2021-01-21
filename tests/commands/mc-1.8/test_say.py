
from mcfunction.versions.mc_1_8.say import say, ParsedSayCommand


def test_say():
    parsed = say.parse('say test successful')
    parsed: ParsedSayCommand

    assert parsed.message.value == 'test successful'

    assert str(parsed) == 'say test successful'
