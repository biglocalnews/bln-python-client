import os
from pathlib import Path
import sys

import click

from bln.client import Client

def get_client():

    env_file = Path.home().joinpath('.bln-env')

    if env_file.exists():
        with open(env_file, 'r') as infile:
            for line in infile.readlines():
                try:
                    key, value = line.split('=')
                    os.environ.setdefault(key, value)
                except ValueError:
                    pass

    try:
        client = Client()
    except ValueError:
        raise click.ClickException('A valid API key could not be found. Visit https://biglocalnews.org/#/manage_keys to create a key.')

    return client


def get_project(project_id):
    pass

