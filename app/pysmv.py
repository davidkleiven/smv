import click
from smv import fetch_nordpool, fetch_nve, raw_plot, parametric_plot
from smv.util import fig_container
import dash_html_components as html
import yaml
import dash
import pandas as pd


@click.group()
def cli():
    pass


@click.command()
@click.argument('outfile')
def fetch(outfile):
    """
    Fetches data from Nordpool and NVE and merges them into one datasets.
    The dataset will be written in JSON format to the passed filename
    """
    print("Fetching data from nordpool group")
    nordpool = fetch_nordpool(standardize=True)

    print("Fetching data from NVE")
    nve = fetch_nve("https://nvebiapi.nve.no/api/Magasinstatistikk/HentOffentligData",
                    standardize=True)

    print("Merging datasets")
    full_dset = pd.concat([nordpool, nve])
    full_dset.reset_index(inplace=True)
    full_dset.to_json(outfile)


@click.command()
@click.argument('outfile')
def npfetch(outfile):
    """
    Fetches all data from nordpool and stores them in a csv file
    """
    try:
        data = fetch_nordpool()
        data.to_csv(outfile)
        print(f"NordPool data written to {outfile}")
    except Exception as exc:
        print(exc)


@click.command()
@click.argument("url")
@click.argument("outfile")
def nvefetch(url: str, outfile: str):
    """
    Fetches data via NVE's API using the passed url and store them in a CSV file given by outfile.
    See http://api.nve.no/doc/magasinstatistikk/
    """
    data = fetch_nve(url)
    data.to_csv(outfile)


@click.command()
@click.argument("conf_file")
def plot(conf_file):
    # Load configuration the configuration file
    with open(conf_file, 'r') as infile:
        config = yaml.safe_load(infile)

    try:
        data = pd.read_json(config['dataset'])
    except Exception as exc:
        print(exc)
        return 1

    ok = True
    html_sections = []
    for i, plt in enumerate(config['plots']):
        try:
            if plt.get('type', '') == 'timeseries':
                fig = raw_plot(data, plt['x'], plt['y'], plt['series'])
            elif plt.get('type', '') == 'parametric':
                fig = parametric_plot(data, plt['x'], plt['y'])
            html_sections.append(fig_container(plt['name'], f'fig{i}', fig))
        except Exception as exc:
            ok = False
            print(exc)

    if ok:
        app = dash.Dash(__name__)
        app.layout = html.Div(children=html_sections)
        app.run_server(debug=True)


cli.add_command(npfetch)
cli.add_command(nvefetch)
cli.add_command(fetch)
cli.add_command(plot)


if __name__ == '__main__':
    cli()
