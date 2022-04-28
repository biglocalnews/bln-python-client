import os

import pandas as pd

from ..client import Client


def read_bln(project_id, file_name, api_token=None, tier="prod", **kwargs):
    """Read in the provided file from biglocalnews.org and return a pandas dataframe.

    The filenames must end with .csv, .json, .xls, or .xlsx, which are mapped to the appropriate pandas reader function.

    Args:
        project_id (str): The unique identifier of the biglocalnews.org project where the file is stored. (Required)
        file_name (str): The name of the file within the biglocalnews.org project.
        api_token (str): An API key from biglocalnews.org with permission to read from the project. (Required but can be drawn from the env variable `BLN_API_TOKEN`)
        tier (str): The biglocalnews.org environment to access. (Required but default is 'prod', which will work for most users.)
        **kwargs: Any other pandas options to be passed into the file reader.

    Returns a pandas DataFrame.
    """
    # Pull the api token
    if not api_token:
        api_token = os.getenv("BLN_API_TOKEN")
        # Raise an error if it doesn't exist
        if not api_token:
            raise ValueError(
                "No API token provided. Either provide one as an inpurt or set the BLN_API_TOKEN environment variable."
            )

    # Figure out what pandas reader method to use based on the file
    if file_name.endswith(".csv"):
        reader = pd.read_csv
    elif file_name.endswith(".json"):
        reader = pd.read_json
    elif file_name.endswith(".xls") or file_name.endswith(".xlsx"):
        reader = pd.read_excel
    else:
        raise ValueError(
            "File name does not have a pandas reader. Only .csv, .json, .xls and .xlsx files are supported."
        )

    # Create an connection to the biglocalnews.org API
    client = Client(api_token, tier=tier)

    # Get the url from biglocalnews.org
    url = client.createFileDownloadUri(project_id, file_name)

    # Read in the file and return the DataFrame.
    return reader(url["uri"], **kwargs)
