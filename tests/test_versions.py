
from mcfunction import get_version


version = get_version('1.13')


def test_self_command():
    assert version.get_command('data') is not None  # added in 1.13


def test_self_deleted_command():
    assert version.get_command('entitydata') is None  # removed in 1.13


def test_older_command():
    assert version.get_command('help') is not None  # added in 1.8
    # (actually, added earlier, but that's not tracked)


def test_older_deleted_command():
    assert version.get_command('achievement') is None  # removed in 1.12
