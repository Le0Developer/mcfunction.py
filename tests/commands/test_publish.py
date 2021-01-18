
from mcfunction.commands.publish import publish, ParsedPublishCommand


def test_publish():
    parsed = publish.parse('publish')
    parsed: ParsedPublishCommand

    assert str(parsed) == 'publish'
