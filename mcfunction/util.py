
import typing as t

from .abc import Node
from .exceptions import ParserException, ConstructionException


T = t.TypeVar('T')
backslash = '\\'
split_dept = {'(': ')', '[': ']', '{': '}', '\'': '\'', '"': '"'}


def tokenize(string: str, sep: str) -> t.Iterator[str]:
    assert len(sep) == 1
    start = 0
    dept = []
    last_backslash = False
    for pos, char in enumerate(string):
        if char == sep and not dept:
            yield string[start:pos]
            start = pos + 1

        if not last_backslash:
            if dept and char == dept[-1]:
                dept.pop()
            elif char in split_dept and '"' not in dept and "'" not in dept:
                dept.append(split_dept[char])

        if char == backslash and not last_backslash:
            last_backslash = True
        else:
            last_backslash = False

    if start - 1 != len(string):
        yield string[start:]

    if dept:
        raise ParserException(f'unclosed {dept[-1]!r}')


def get(generator: t.Iterator[T], amount: int = None, func=next) \
        -> t.Union[T, t.Sequence[T]]:
    if amount is None:
        return func(generator)
    r = []
    for x in range(amount):
        r.append(func(generator))
    return r


def ensure_nodes(object: t.Any, *names: str):
    for name in names:
        value = getattr(object, name, None)
        if not value or not isinstance(value, Node):
            raise ConstructionException(
                f'expected {name!r} to be Node, not {value!r}'
            )


def clean(string):
    return string.rstrip('0').rstrip('.')
