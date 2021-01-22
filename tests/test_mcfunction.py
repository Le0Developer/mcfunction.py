
import io

from mcfunction import mcfunction, parse_mcfuntion


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


def test_mcfunction_load():
    lines = (
        '\n'  # empty line
        '# comment\n'
        '#comment with multiple words\n'
        'help'
    )

    fp = io.StringIO(lines)

    parsed = mcfunction.McFunction.load(fp)
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

    out = io.StringIO()
    parsed.dump(out)
    out.seek(0)

    assert out.read() == lines


def test_mcfunction_loads():
    lines = (
        '\n'  # empty line
        '# comment\n'
        '#comment with multiple words\n'
        'help'
    )

    assert str(mcfunction.McFunction.loads(lines)) == lines
