
from mcfunction.commands.say import say, ParsedSayCommand


def test_say():
    parsed = say.parse('say test successful')
    parsed: ParsedSayCommand

    assert parsed.message.value == 'test successful'

    assert str(parsed) == 'say test successful'
