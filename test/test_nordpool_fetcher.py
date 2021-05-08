import pytest
from smv import NordPoolFetcher


@pytest.mark.slow
def test_fetcher():  
    data =  NordPoolFetcher().fetch()
    assert not data.empty