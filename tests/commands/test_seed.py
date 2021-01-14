
from mcast.commands.seed import seed, ParsedSeedCommand


def test_seed():
    parsed = seed.parse('seed')
    parsed: ParsedSeedCommand

    assert str(parsed) == 'seed'
