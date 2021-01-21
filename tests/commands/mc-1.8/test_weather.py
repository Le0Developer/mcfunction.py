
from mcfunction.versions.mc_1_8.weather import weather, ParsedWeatherCommand


def test_weather():
    parsed = weather.parse('weather thunder')
    parsed: ParsedWeatherCommand

    assert parsed.weather.value == 'thunder'

    assert str(parsed) == 'weather thunder'


def test_weather_duration():
    parsed = weather.parse('weather thunder 1337')
    parsed: ParsedWeatherCommand

    assert parsed.weather.value == 'thunder'
    assert parsed.duration.value == 1337

    assert str(parsed) == 'weather thunder 1337'
