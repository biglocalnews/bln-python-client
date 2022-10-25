import json
from pathlib import Path
from urllib.parse import urlparse

import click

from bln.client import Client
from scripts import utils



@click.group()

def cli():
    """Big Local News command line tool."""
    pass

@cli.command()
@click.option(
    '--key',
    prompt='Paste your API key here. API keys can be created at https://biglocalnews.org/#/manage_keys'
        )

def authenticate(key: str):
    """Authenticate with the Big Local News platform. To obtain an API key, visit https://biglocalnews.org/#/manage_keys"""
    user_root = Path.home()

    bln_env_file = user_root.joinpath('.bln_env')
    bln_env_file.write_text(f'BLN_API_TOKEN={key}')
    
    # Test the key to make sure it is valid.
    try:
        client = utils.get_client()
        client.user()
    except:
        raise click.ClickException('Invalid API key. Visit https://biglocalnews.org/#/manage_keys to confirm the key or create a new one.')
    else:
        click.echo('Authentication successful.')


@cli.command()

def init():
    """Create a new Big Local News project or connect to an existing one."""
    client = utils.get_client()
    click.echo(
    """Create a new project or connect to an existing one?
        1. Create a new project.
        2. Connect to an existing project."""
    )
    create_or_get = click.prompt(
    "Choose an option",
    type=click.Choice(['1','2']),
    )

    # create a new project
    if create_or_get == '1':
        project_name = click.prompt('Enter a project name', type=str)
        project = client.createProject(project_name)

        if not project:
            raise click.ClickException('Could not create project.')
        
        project_id = project['id']
        # Do we need to prompt user for additional metadata, ie project description?
        click.echo(f'Created project {project["name"]}.')

    # connect to an existing project
    elif create_or_get == '2':
        project_url = click.prompt('Paste the url of the project here', type=str)
        project_url = urlparse(project_url)
        
        if project_url.netloc != "biglocalnews.org":
            raise click.ClickException("Invalid project url.")
        else:
            project_id = project_url.fragment.split('/')[-1]

        # Test to make sure it is a valid project
        project = client.get_project_by_id(project_id)

        if not project:
            raise click.ClickException("Invalid project ID.")

        # Test to ensure user has upload priveleges
        role = [role for role in client.effectiveProjectRoles() if role['project']['id'] == project_id][0]['role']
        
        click.echo(f"Connected to project {project['name']}")
        
        if role == 'VIEWER':
            click.echo("You can download files from this project, but don't have permission to upload files. Contact a project administrator to get write permissions.")


    # Set the data directory
    project_root = Path.cwd()
    data_dir = click.prompt('Specify a directory to store files', type=click.Path(), default=project_root.joinpath('data'))

    if not data_dir.exists():
        click.echo('Directory does not exist, creating it now.')
        data_dir.mkdir(parents=True)

    metadata = {
                'project_id': project_id,
                'data_dir': str(data_dir)
            }

    project_metadata_file = project_root.joinpath('.bln')

    project_metadata_file.write_text(json.dumps(metadata))



if __name__ == "__main__":
    cli()
