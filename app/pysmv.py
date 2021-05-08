import click
from smv import NordPoolFetcher


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

cli.add_command(npfetch)


if __name__ == '__main__':
    cli()