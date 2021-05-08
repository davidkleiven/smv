import click
from smv import NordPoolFetcher, fetch_nve


@click.group()
def cli():
    pass


@click.command()
@click.argument('outfile')
def npfetch(outfile):
    """
    Fetches all data from nordpool and stores them in a csv file
    """
    try:
        fetcher = NordPoolFetcher()
        data = fetcher.fetch()
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

cli.add_command(npfetch)
cli.add_command(nvefetch)


if __name__ == '__main__':
    cli()
