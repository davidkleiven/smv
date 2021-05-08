import requests
import logging
import pandas as pd


__all__ = ('fetch_nve',)


logger = logging.getLogger(__name__)


def fetch_nve(url: str) -> pd.DataFrame:
    """
    Fetches magasin data from NVE. If an error occurs, an empty DataFrame
    is returned

    :param url: URL to fetch from
    """
    try:
        res = requests.get(url)
    except Exception as exc:
        logger.warning(exc)
        return pd.DataFrame([])

    if res.status_code != 200:
        logger.warning(f"An error occured. Error code: {res.status_code}")
        return pd.DataFrame([])

    return pd.read_json(res.content)
