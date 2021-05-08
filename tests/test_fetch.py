import pytest
from smv import fetch_nordpool, fetch_nve


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
