from typing import Sequence, List
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

import datetime


def fig_container(figname: str, fig_id: str, fig) -> html.Div:
    return html.Div([
        html.H1(children=figname),
        dcc.Graph(
            id=fig_id,
            figure=fig,
            style={'width': '70vw', 'height': '90vh'}
        )]
    )


def datetime2float(d: str, fmt: str):
    epoch = datetime.datetime.utcfromtimestamp(0)
    total_seconds = (datetime.datetime.strptime(d, fmt) - epoch).total_seconds()
    return total_seconds


def deseasonalize(dates: Sequence[str], values: Sequence[float], time_fmt: str,
                  period_sec: int) -> List[float]:
    """
    Average the quantity in col over years

    :param dates: Sequence with dates
    :param values: Sequence with corresonding values
    :param time_fmt: Format of the timestamps (e.g. %Y-%m-%d)
    :param period_sec: Period in seconds
    """
    # Convert the time array into UTC to allow for interpolation
    t_float = [datetime2float(x, time_fmt) for x in dates]
    interp = interp1d(t_float, values, bounds_error=False)
    return [v - interp(t - period_sec) for t, v in zip(t_float, values)]


def add_deseasonalized_value(df: pd.DataFrame, date_col: str, col: str, time_fmt: str,
                             period_sec: int):
    """
    Adds the deseasonalized data to the passe data frame

    :param df: Data frame with data
    :param data_col: Column with dates
    :param col: Column with data
    :param time_fmt: Format of the date column
    :param period_sec: Period of the data
    """
    deseason_col_name = col + "_deseasonalized"
    df[deseason_col_name] = deseasonalize(df[date_col], df[col], time_fmt, period_sec)
    return df


def add_missing_columns(df: pd.DataFrame, cols: Sequence[str]):
    missing = set(cols) - set(df.columns)
    for col in missing:
        df[col] = np.nan
