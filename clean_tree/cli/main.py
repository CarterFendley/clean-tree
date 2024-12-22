from typing import Tuple

import click

from clean_tree.config import CleanTreeConfig
from clean_tree.logging import (
    get_logger,
    set_cli_level
)
from clean_tree.git import find_git_directories

logger = get_logger(__name__, cli=True)

@click.group()
@click.option('-v', '--verbose', count=True, help='Enable verbose logging.')
def clean_tree(verbose: int):
    """
    Commitment is hard :)
    """
    set_cli_level(verbose)

@clean_tree.command('status')
@click.option('--directory', '-d', multiple=True, default=('.',))
@click.option('--max-display', default=10)
def status(directory: Tuple[str], max_display: int):
    config = CleanTreeConfig(
        directories=directory,
        max_display=max_display
    )

    for d in config.directories:
        find_git_directories(d)
