
from mcfunction.versions.mc_1_8.clone import clone, ParsedCloneCommand


def test_clone():
    parsed = clone.parse('clone -1 -1 -1 ~1 ~1 ~1 ^ ^ ^')
    parsed: ParsedCloneCommand

    assert (parsed.begin.x.value == -1 and parsed.begin.y.value == -1
            and parsed.begin.z.value == -1)
    assert (parsed.end.x.relative and parsed.end.y.relative
            and parsed.end.z.relative)
    assert (parsed.destination.x.local and parsed.destination.y.local
            and parsed.destination.z.local)

    assert str(parsed) == 'clone -1 -1 -1 ~1 ~1 ~1 ^ ^ ^'


def test_clone_replace():
    parsed = clone.parse('clone 0 0 0 1 1 1 2 2 2 replace force')
    parsed: ParsedCloneCommand

    assert parsed.mask_mode.value == 'replace'
    assert parsed.clone_mode.value == 'force'

    assert str(parsed) == 'clone 0 0 0 1 1 1 2 2 2 replace force'


def test_clone_filtered():
    parsed = clone.parse('clone 0 0 0 1 1 1 2 2 2 filtered test:filter')
    parsed: ParsedCloneCommand

    assert parsed.mask_mode.value == 'filtered'
    assert parsed.filter.namespace == 'test'
    assert parsed.filter.name == 'filter'
    assert parsed.clone_mode is None

    assert str(parsed) == 'clone 0 0 0 1 1 1 2 2 2 filtered test:filter'
