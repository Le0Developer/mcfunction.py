
from mcfunction.versions.mc_1_8.scoreboard import (
    scoreboard, ParsedScoreboardCommand
)
from mcfunction.nodes import EntityNode


def test_scoreboard_objectives_add():
    parsed = scoreboard.parse('scoreboard objectives add testobjective dummy')
    parsed: ParsedScoreboardCommand

    assert parsed.category.value == 'objectives'
    assert parsed.action.value == 'add'
    assert parsed.objective.value == 'testobjective'
    assert parsed.criterion.value == 'dummy'

    assert str(parsed) == 'scoreboard objectives add testobjective dummy'


def test_scoreboard_objectives_add_displayname():
    parsed = scoreboard.parse('scoreboard objectives add testobjective dummy '
                              '{"text":"test successful"}')
    parsed: ParsedScoreboardCommand

    assert parsed.name.object['text'] == 'test successful'

    assert str(parsed) == 'scoreboard objectives add testobjective dummy ' \
                          '{"text":"test successful"}'


def test_scoreboard_objectives_list():
    parsed = scoreboard.parse('scoreboard objectives list')
    parsed: ParsedScoreboardCommand

    assert parsed.category.value == 'objectives'
    assert parsed.action.value == 'list'

    assert str(parsed) == 'scoreboard objectives list'


def test_scoreboard_objectives_modify_displayname():
    parsed = scoreboard.parse('scoreboard objectives modify testobjective '
                              'displayname {"text":"test successful"}')
    parsed: ParsedScoreboardCommand

    assert parsed.category.value == 'objectives'
    assert parsed.action.value == 'modify'
    assert parsed.objective.value == 'testobjective'
    assert parsed.mode.value == 'displayname'
    assert parsed.name.object['text'] == 'test successful'

    assert str(parsed) == 'scoreboard objectives modify testobjective ' \
                          'displayname {"text":"test successful"}'


def test_scoreboard_objectives_modify_rendertype():
    parsed = scoreboard.parse('scoreboard objectives modify testobjective '
                              'rendertype hearts')
    parsed: ParsedScoreboardCommand

    assert parsed.category.value == 'objectives'
    assert parsed.action.value == 'modify'
    assert parsed.objective.value == 'testobjective'
    assert parsed.mode.value == 'rendertype'
    assert parsed.value.value == 'hearts'

    assert str(parsed) == 'scoreboard objectives modify testobjective ' \
                          'rendertype hearts'


def test_scoreboard_objectives_remove():
    parsed = scoreboard.parse('scoreboard objectives remove testobjective')
    parsed: ParsedScoreboardCommand

    assert parsed.category.value == 'objectives'
    assert parsed.action.value == 'remove'
    assert parsed.objective.value == 'testobjective'

    assert str(parsed) == 'scoreboard objectives remove testobjective'


def test_scoreboard_objectives_setdisplay():
    parsed = scoreboard.parse('scoreboard objectives setdisplay sidebar')
    parsed: ParsedScoreboardCommand

    assert parsed.category.value == 'objectives'
    assert parsed.action.value == 'setdisplay'
    assert parsed.slot.value == 'sidebar'

    assert str(parsed) == 'scoreboard objectives setdisplay sidebar'


def test_scoreboard_objectives_setdisplay_value():
    parsed = scoreboard.parse('scoreboard objectives setdisplay sidebar '
                              'testobjective')
    parsed: ParsedScoreboardCommand

    assert parsed.objective.value == 'testobjective'

    assert str(parsed) == 'scoreboard objectives setdisplay sidebar ' \
                          'testobjective'


def test_scoreboard_players_add():
    parsed = scoreboard.parse('scoreboard players add @s testobjective 1')
    parsed: ParsedScoreboardCommand

    assert parsed.category.value == 'players'
    assert parsed.action.value == 'add'
    assert isinstance(parsed.target, EntityNode)
    assert parsed.objective.value == 'testobjective'
    assert parsed.value.value == 1

    assert str(parsed) == 'scoreboard players add @s testobjective 1'


def test_scoreboard_players_enable():
    parsed = scoreboard.parse('scoreboard players enable @s testobjective')
    parsed: ParsedScoreboardCommand

    assert parsed.category.value == 'players'
    assert parsed.action.value == 'enable'
    assert isinstance(parsed.target, EntityNode)
    assert parsed.objective.value == 'testobjective'

    assert str(parsed) == 'scoreboard players enable @s testobjective'


def test_scoreboard_players_list():
    parsed = scoreboard.parse('scoreboard players list')
    parsed: ParsedScoreboardCommand

    assert parsed.category.value == 'players'
    assert parsed.action.value == 'list'

    assert str(parsed) == 'scoreboard players list'


def test_scoreboard_players_list_target():
    parsed = scoreboard.parse('scoreboard players list @s')
    parsed: ParsedScoreboardCommand

    assert parsed.category.value == 'players'
    assert parsed.action.value == 'list'
    assert isinstance(parsed.target, EntityNode)

    assert str(parsed) == 'scoreboard players list @s'


def test_scoreboard_players_operation():
    parsed = scoreboard.parse('scoreboard players operation @s testobjective1 '
                              '>< @s testobjective2')
    parsed: ParsedScoreboardCommand

    assert parsed.category.value == 'players'
    assert parsed.action.value == 'operation'
    assert isinstance(parsed.target, EntityNode)
    assert parsed.objective.value == 'testobjective1'
    assert parsed.operation.value == '><'
    assert isinstance(parsed.source_target, EntityNode)
    assert parsed.source_objective.value == 'testobjective2'

    assert str(parsed) == 'scoreboard players operation @s testobjective1 ' \
                          '>< @s testobjective2'


def test_scoreboard_players_reset():
    parsed = scoreboard.parse('scoreboard players reset @s')
    parsed: ParsedScoreboardCommand

    assert parsed.category.value == 'players'
    assert parsed.action.value == 'reset'
    assert isinstance(parsed.target, EntityNode)

    assert str(parsed) == 'scoreboard players reset @s'


def test_scoreboard_players_reset_objective():
    parsed = scoreboard.parse('scoreboard players reset @s testobjective')
    parsed: ParsedScoreboardCommand

    assert parsed.objective.value == 'testobjective'

    assert str(parsed) == 'scoreboard players reset @s testobjective'


def test_team_add():
    parsed = scoreboard.parse('scoreboard teams add testteam')
    parsed: ParsedScoreboardCommand

    assert parsed.action.value == 'add'
    assert parsed.team.value == 'testteam'

    assert str(parsed) == 'scoreboard teams add testteam'


def test_team_add_displayname():
    parsed = scoreboard.parse('scoreboard teams add testteam '
                              '{"text":"test successful"}')
    parsed: ParsedScoreboardCommand

    assert parsed.name.object['text'] == 'test successful'

    assert str(parsed) == 'scoreboard teams add testteam ' \
                          '{"text":"test successful"}'


def test_team_empty():
    parsed = scoreboard.parse('scoreboard teams empty testteam')
    parsed: ParsedScoreboardCommand

    assert parsed.action.value == 'empty'
    assert parsed.team.value == 'testteam'

    assert str(parsed) == 'scoreboard teams empty testteam'


def test_team_join():
    parsed = scoreboard.parse('scoreboard teams join testteam')
    parsed: ParsedScoreboardCommand

    assert parsed.action.value == 'join'
    assert parsed.team.value == 'testteam'

    assert str(parsed) == 'scoreboard teams join testteam'


def test_team_join_target():
    parsed = scoreboard.parse('scoreboard teams join testteam @s')
    parsed: ParsedScoreboardCommand

    assert isinstance(parsed.target, EntityNode)

    assert str(parsed) == 'scoreboard teams join testteam @s'


def test_team_leave():
    parsed = scoreboard.parse('scoreboard teams leave @s')
    parsed: ParsedScoreboardCommand

    assert parsed.action.value == 'leave'
    assert isinstance(parsed.target, EntityNode)

    assert str(parsed) == 'scoreboard teams leave @s'


def test_team_list():
    parsed = scoreboard.parse('scoreboard teams list')
    parsed: ParsedScoreboardCommand

    assert parsed.action.value == 'list'

    assert str(parsed) == 'scoreboard teams list'


def test_team_list_team():
    parsed = scoreboard.parse('scoreboard teams list testteam')
    parsed: ParsedScoreboardCommand

    assert parsed.action.value == 'list'
    assert parsed.team.value == 'testteam'

    assert str(parsed) == 'scoreboard teams list testteam'


def test_team_option():
    parsed = scoreboard.parse('scoreboard teams option testteam displayName '
                              '{"text":"test successful"}')
    parsed: ParsedScoreboardCommand

    assert parsed.action.value == 'option'
    assert parsed.team.value == 'testteam'
    assert parsed.option.value == 'displayName'
    assert parsed.value.value == '{"text":"test successful"}'

    assert str(parsed) == 'scoreboard teams option testteam displayName ' \
                          '{"text":"test successful"}'
