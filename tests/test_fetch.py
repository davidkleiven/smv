import pytest
from smv import NordPoolFetcher, fetch_nve


@pytest.mark.slow
def test_nordpool_fetcher():
    data = NordPoolFetcher().fetch()
    assert not data.empty


def test_nve_fetch_invalid_url():
    data = fetch_nve("clearlyNotAValidURL")
    assert data.empty


@pytest.mark.slow
def test_nve_fetch_valid_url():
    data = fetch_nve("https://nvebiapi.nve.no/api/Magasinstatistikk/HentOffentligData")
    assert not data.empty
