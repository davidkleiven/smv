import requests
import logging
import pandas as pd
from typing import List
import yaml
import pkgutil
import datetime
from smv.constants import NP2PO, DATE, AREA_NUM, DATA_SRC


__all__ = ('fetch_nve', 'fetch_nordpool')


logger = logging.getLogger(__name__)


def fetch_nve(url: str, standardize: bool = False) -> dict:
    """
    Fetches magasin data from NVE. If an error occurs, an empty DataFrame
    is returned

    :param url: URL to fetch from
    :param standardize: If True, the data will be standardized
    """
    try:
        res = requests.get(url)
    except Exception as exc:
        logger.warning(exc)
        return {}

    if res.status_code != 200:
        logger.warning(f"An error occured. Error code: {res.status_code}")
        return {}

    dset = pd.read_json(res.content)

    if standardize:
        dset = standardize_nve(dset)
    return dset


def fetch_nordpool(standardize: bool = False):
    """
    Fetches data from nordpool and stores them in a file

    :param standardize: If True, the data will be standardized
    """
    links = _load_nordpool_links()
    datasets = []
    for url in links:
        data = pd.read_html(url, decimal=',', thousands=None)[0]

        # Pandas interpretes the HTML as a nested table. The two outermost levels
        # has only one column, thus the column names can be replaced by the two
        # last columns
        cols = list(data.columns.get_level_values(2))

        cols[0] = 'Week-Year'

        # Hack: Ensure that Tromso is spelled without special characters
        for i, c in enumerate(cols):
            if c.startswith('Troms'):
                cols[i] = 'Tromso'
                break
        data.columns = cols

        # Add proper data column
        data['Date'] = [year_week2date(x) for x in data['Week-Year']]
        datasets.append(data)
    dset = pd.concat(datasets)

    if standardize:
        dset = standardize_nordpool(dset)
    return dset


def standardize_nordpool(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts nordpool data into NVE format. Only cities with an
    assigned "area number" will be extracted. See constants.NP2PO.

    :param df: Dataframe from nordpool HTML files
    """
    std_rep = []
    for _, row in df.iterrows():
        for city, area_num in NP2PO.items():
            data_item = {
                DATE: row['Date'],
                AREA_NUM: area_num,
                "Price": row[city],
                "Unit": "NOK/MWh",
                DATA_SRC: "nordpool"
            }
            std_rep.append(data_item)
    dset = pd.DataFrame(std_rep)
    return dset


def standardize_nve(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardizes data retrieved from NVE
    """
    df[DATA_SRC] = "NVE"
    return df


def year_week2date(year_week: str) -> datetime.date:
    """
    Converts year and week to a data by picking the Monday in that week
    """
    splitted = year_week.split('-')
    week, year = splitted[0].strip(), splitted[1].strip()

    if len(year) == 2:
        # Missing century
        year = "20" + year
    return datetime.date.fromisocalendar(int(year), int(week), 1).strftime("%Y-%m-%d")


def _load_nordpool_links() -> List[str]:
    """
    Load the links from assets(nordpool_files.yml)
    """
    data = yaml.safe_load(pkgutil.get_data(__name__, "assets/nordpool_files.yml"))
    return data.get('files', [])
