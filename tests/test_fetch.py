import pytest
from smv import fetch_nordpool, fetch_nve
from smv.fetch import year_week2date


@pytest.mark.slow
def test_nordpool_fetcher():
    data = fetch_nordpool()
    print(data)
    assert False
    assert not data.empty


def test_nve_fetch_invalid_url():
    data = fetch_nve("clearlyNotAValidURL")
    assert data.empty


@pytest.mark.slow
def test_nve_fetch_valid_url():
    data = fetch_nve("https://nvebiapi.nve.no/api/Magasinstatistikk/HentOffentligData")
    assert not data.empty


@pytest.mark.parametrize("yw,expect", [
    ('01-21', "2021-01-04"),
    ('02-21', "2021-01-11"),
    ('42-21', "2021-10-18"),
    ('31-13', "2013-07-29")
    ]
)
def test_year_week2data(yw, expect):
    res = year_week2date(yw)
    assert res == expect
