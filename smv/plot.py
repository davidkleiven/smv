from typing import Dict, Sequence
import plotly.graph_objects as go
import pandas as pd


__all__ = ('raw_plot',)


def raw_plot(df: pd.DataFrame, x_field: str, y_field: str, series: Sequence[Dict[str, str]]):
    """
    Create a plot of prices as a function of time

    :param df: Data frame with date
    :param time_field: Name of the field where the time value is stored (for example Data)
    :param fields: List of fields to be included in this figure
    """
    df_sorted = df.sort_values(x_field)

    fig = go.Figure()
    for s in series:
        res = df_sorted.query(s['query'])
        fig.add_trace(
            go.Scatter(x=res[x_field], y=res[y_field], name=s.get('name', ''))
        )
    return fig
