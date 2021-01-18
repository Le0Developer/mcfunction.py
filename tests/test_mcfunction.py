
from mcfunction import parse_mcfuntion
from mcfunction import mcfunction


def test_mcfunction():
    lines = (
        '\n'  # empty line
        '# comment\n'
        '#comment with multiple words\n'
        'help'
    )

    parsed = parse_mcfuntion(lines.splitlines())
    parsed: mcfunction.McFunction

    empty, comment, long_comment, command = parsed.commands
    empty: mcfunction.NoCommand
    comment: mcfunction.NoCommand
    long_comment: mcfunction.NoCommand

    assert empty.command == ''
    assert empty.comment is None
    assert comment.command == '# '
    assert comment.comment.value == 'comment'
    assert long_comment.command == '#'  # without the space at the end
    assert long_comment.comment.value == 'comment with multiple words'
    assert command.command == 'help'

    assert str(parsed) == lines
