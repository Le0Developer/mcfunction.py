
from mcfunction.versions.mc_1_9.particle import (
    particle, ParsedParticleCommand
)
from mcfunction.nodes import EntityNode, PositionNode


def test_particle_delta():
    parsed = particle.parse('particle test:particle 0 0 0 1 1 1 2 3')
    parsed: ParsedParticleCommand

    assert isinstance(parsed.delta, PositionNode)
    assert parsed.speed.value == 2
    assert parsed.count.value == 3

    assert str(parsed) == 'particle test:particle 0 0 0 1 1 1 2 3'


def test_particle_mode():
    parsed = particle.parse('particle test:particle 0 0 0 1 1 1 2 3 force')
    parsed: ParsedParticleCommand

    assert parsed.mode.value == 'force'

    assert str(parsed) == 'particle test:particle 0 0 0 1 1 1 2 3 force'


def test_particle_viewers():
    parsed = particle.parse('particle test:particle 0 0 0 1 1 1 2 3 force @s')
    parsed: ParsedParticleCommand

    assert isinstance(parsed.viewers, EntityNode)

    assert str(parsed) == 'particle test:particle 0 0 0 1 1 1 2 3 force @s'
