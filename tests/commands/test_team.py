
from mcfunction.commands.team import team, ParsedTeamCommand
from mcfunction.nodes import EntityNode


def test_team_add():
    parsed = team.parse('team add testteam')
    parsed: ParsedTeamCommand

    assert parsed.action.value == 'add'
    assert parsed.team.value == 'testteam'

    assert str(parsed) == 'team add testteam'


def test_team_add_displayname():
    parsed = team.parse('team add testteam {"text":"test successful"}')
    parsed: ParsedTeamCommand

    assert parsed.name.object['text'] == 'test successful'

    assert str(parsed) == 'team add testteam {"text":"test successful"}'


def test_team_empty():
    parsed = team.parse('team empty testteam')
    parsed: ParsedTeamCommand

    assert parsed.action.value == 'empty'
    assert parsed.team.value == 'testteam'

    assert str(parsed) == 'team empty testteam'


def test_team_join():
    parsed = team.parse('team join testteam')
    parsed: ParsedTeamCommand

    assert parsed.action.value == 'join'
    assert parsed.team.value == 'testteam'

    assert str(parsed) == 'team join testteam'


def test_team_join_target():
    parsed = team.parse('team join testteam @s')
    parsed: ParsedTeamCommand

    assert isinstance(parsed.target, EntityNode)

    assert str(parsed) == 'team join testteam @s'


def test_team_leave():
    parsed = team.parse('team leave @s')
    parsed: ParsedTeamCommand

    assert parsed.action.value == 'leave'
    assert isinstance(parsed.target, EntityNode)

    assert str(parsed) == 'team leave @s'


def test_team_list():
    parsed = team.parse('team list')
    parsed: ParsedTeamCommand

    assert parsed.action.value == 'list'

    assert str(parsed) == 'team list'


def test_team_list_team():
    parsed = team.parse('team list testteam')
    parsed: ParsedTeamCommand

    assert parsed.action.value == 'list'
    assert parsed.team.value == 'testteam'

    assert str(parsed) == 'team list testteam'


def test_team_modify():
    parsed = team.parse('team modify testteam displayName '
                        '{"text":"test successful"}')
    parsed: ParsedTeamCommand

    assert parsed.action.value == 'modify'
    assert parsed.team.value == 'testteam'
    assert parsed.option.value == 'displayName'
    assert parsed.value.value == '{"text":"test successful"}'

    assert str(parsed) == 'team modify testteam displayName ' \
                          '{"text":"test successful"}'
