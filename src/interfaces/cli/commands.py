import pathlib

import click


@click.group()
@click.pass_context
def cli(ctx: click.Context):
    pass


@cli.command(help="Ingest document in knowledge base")
@click.argument(
    "path",
    nargs=-1,
    type=click.Path(
        exists=True,
        path_type=pathlib.Path,
    ),
)
@click.option("-r", "--recursive", is_flag=True)
@click.pass_context
def ingest(ctx: click.Context, recursive: bool, path: pathlib.Path):
    click.echo("Running ingestion pipeline")
