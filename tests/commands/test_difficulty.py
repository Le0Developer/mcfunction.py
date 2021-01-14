
from mcast.commands.difficulty import difficulty, ParsedDifficultyCommand


def test_difficulty():
    parsed = difficulty.parse('difficulty hard')
    parsed: ParsedDifficultyCommand

    assert parsed.difficulty.value == 'hard'

    assert str(parsed) == 'difficulty hard'
