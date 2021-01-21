
from mcfunction.versions.mc_1_8.seed import seed, ParsedSeedCommand


def test_seed():
    parsed = seed.parse('seed')
    parsed: ParsedSeedCommand

    assert str(parsed) == 'seed'
