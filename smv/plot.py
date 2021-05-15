from typing import Dict, Sequence
import plotly.graph_objects as go
import pandas as pd
from smv.constants import DATE, TIME_FMT
from smv.util import datetime2float
from scipy.interpolate import interp1d
import numpy as np


__all__ = ('raw_plot', 'parametric_plot')

RAW_PLOT_REQUIRED_FIELDS = ['name', 'query']
PARAM_PLOT_REQUIRED_FIELDS = ['query', 'field']


def raw_plot(df: pd.DataFrame, x_field: str, y_field: str, series: Sequence[Dict[str, str]]):
    """
    Create a plot of prices as a function of time

    :param df: Data frame with date
    :param time_field: Name of the field where the time value is stored (for example Data)
    :param fields: List of fields to be included in this figure
    """
    if not raw_plot_series_is_valid(series):
        msg = "Series are not in a valid format. Must be a iteratable of dictionaries where"
        msg += f"the fields {RAW_PLOT_REQUIRED_FIELDS}"
        print(msg)
        return go.Figure()

    if x_field not in df.columns:
        print(f"{x_field} does not exist")
        return go.Figure()

    df_sorted = df.sort_values(x_field)

    fig = go.Figure()
    for s in series:
        try:
            res = df_sorted.query(s['query'])
            fig.add_trace(
                go.Scatter(x=res[x_field], y=res[y_field], name=s.get('name', ''))
            )
        except Exception as exc:
            print(f"Error: {exc}")
    return fig


def parametric_plot(df: pd.DataFrame, x: Dict[str, str],
                    y: Dict[str, str]):
    """
    Creates a parametric plot (x(t), y(t))

    :param df: Data frame
    :param param_field: Field where the independent parameter is stored
    :param x_field: Field to use for x-values
    """
    if DATE not in df.columns:
        print(f"{DATE} must be a field")
        return go.Figure()

    if not parametric_plot_queries_is_valid(x) or not parametric_plot_queries_is_valid(y):
        print(f"x and y myst have the keys {PARAM_PLOT_REQUIRED_FIELDS}")
        return go.Figure()

    try:
        df_sorted = df.sort_values(DATE)
        df_x = df_sorted.query(x['query'])
        df_y = df_sorted.query(y['query'])

        param_x = [datetime2float(x, TIME_FMT) for x in df_x[DATE]]
        param_y = [datetime2float(y, TIME_FMT) for y in df_y[DATE]]

        x_interp = interp1d(param_x, df_x[x['field']])
        y_interp = interp1d(param_y, df_y[y['field']])

        # Find maximum overlapping range
        t_min = max([min(param_x), min(param_y)])
        t_max = min([max(param_x), max(param_y)])
        num_points = max([len(param_x), len(param_y)])

        t = np.linspace(t_min, t_max, num_points)

        x_values = x_interp(t)
        y_values = y_interp(t)

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(x=x_values, y=y_values, mode='markers')
        )

        fig.update_layout(xaxis_title=x['field'], yaxis_title=y['field'])
    except Exception as exc:
        print(exc)
        fig = go.Figure()

    return fig


def raw_plot_series_is_valid(series: Sequence[Dict[str, str]]) -> bool:
    for s in series:
        for f in RAW_PLOT_REQUIRED_FIELDS:
            if f not in s:
                return False
    return True


def parametric_plot_queries_is_valid(item: Dict[str, str]) -> bool:
    for f in PARAM_PLOT_REQUIRED_FIELDS:
        if f not in item.keys():
            return False
    return True
