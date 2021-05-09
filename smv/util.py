import dash_core_components as dcc
import dash_html_components as html


def fig_container(figname: str, fig_id: str, fig) -> html.Div:
    return html.Div([
        html.H1(children=figname),
        dcc.Graph(
            id=fig_id,
            figure=fig
        )]
    )
