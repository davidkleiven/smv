from typing import List
import yaml
import pkgutil
import pandas as pd


__all__ = ('NordPoolFetcher',)


class NordPoolFetcher:
    """
    Class for fetching datafiles from noordpol
    """
    def __init__(self):
        self._links = self.get_files()

    @staticmethod
    def get_files() -> List[str]:
        """
        Loads files specified listed in assets/nordpool_files.yml
        """
        data = yaml.safe_load(pkgutil.get_data(__name__, "assets/nordpool_files.yml"))
        return data.get('files', [])

    def fetch(self):
        """
        Fetches data from nordpool and stores them in a file
        """
        return pd.concat([pd.read_html(url)[0] for url in self._links])
