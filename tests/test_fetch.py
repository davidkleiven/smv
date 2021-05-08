import pytest
from smv import NordPoolFetcher, fetch_nve



@pytest.mark.slow
def test_nordpool_fetcher():
    data = NordPoolFetcher().fetch()
    assert not data.empty

def test_nve_fetch():
    # Case 1: Make sure an empty dataframe is returned when the URL is wrong
    data = fetch_nve("clearlyNotAValidURL")
    assert data.empty

    # Case 2: Valid URL, but no data
    data = fetch_nve("https://nvebiapi.nve.no/api/Magasinstatistikk/HentOffentligData")
    assert not data.empty
