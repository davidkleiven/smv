import dash_core_components as dcc
import dash_html_components as html

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


def datetime2float(d: str):
    epoch = datetime.datetime.utcfromtimestamp(0)
    total_seconds = (datetime.datetime.strptime(d, "%Y-%m-%d") - epoch).total_seconds()
    return total_seconds
