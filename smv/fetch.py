import requests
import logging
import pandas as pd
from typing import List
import yaml
import pkgutil


__all__ = ('fetch_nve', 'fetch_nordpool')


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


def fetch_nordpool():
    """
    Fetches data from nordpool and stores them in a file
    """
    links = _load_nordpool_links()
    return pd.concat([pd.read_html(url)[0] for url in links])


def _load_nordpool_links() -> List[str]:
    """
    Load the links from assets(nordpool_files.yml)
    """
    data = yaml.safe_load(pkgutil.get_data(__name__, "assets/nordpool_files.yml"))
    return data.get('files', [])
