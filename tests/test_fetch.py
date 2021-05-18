import pytest
import pandas as pd
from smv import fetch_nordpool, fetch_nve
from smv.fetch import year_week2date


@pytest.mark.slow
def test_nordpool_fetcher():
    data_dict = fetch_nordpool()
    data = pd.DataFrame(data_dict)
    assert not data.empty


def test_nve_fetch_invalid_url():
    data = fetch_nve("clearlyNotAValidURL")
    assert len(data) == 0


@pytest.mark.slow
def test_nve_fetch_valid_url():
    data_dict = fetch_nve("https://nvebiapi.nve.no/api/Magasinstatistikk/HentOffentligData")
    data = pd.DataFrame(data_dict)
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
