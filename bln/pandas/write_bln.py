import os
import pathlib
import tempfile

from ..client import Client


class BlnWriterAccessor:
    """Write in attached dataframe to biglocalnews.org.

    The filenames must end with .csv, .json, .xls, or .xlsx, which are mapped to the appropriate pandas writer function.

    Args:
        project_id (str): The unique identifier of the biglocalnews.org project where the file is stored. (Required)
        file_name (str): The name of the file within the biglocalnews.org project.
        api_token (str): An API key from biglocalnews.org with permission to read from the project. (Required but can be drawn from the env variable `BLN_API_TOKEN`)
        tier (str): The biglocalnews.org environment to access. (Required but default is 'prod', which will work for most users.)
        **kwargs: Any other pandas options to be passed into the file writer,
    """

    def __init__(self, pandas_obj):
        """Initialize accessor."""
        self._obj = pandas_obj

    def __call__(self, project_id, file_name, api_token=None, tier="prod", **kwargs):
        """Write in attached dataframe to biglocalnews.org.."""
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
            writer = self._obj.to_csv
        elif file_name.endswith(".json"):
            writer = self._obj.to_json
        elif file_name.endswith(".xls") or file_name.endswith(".xlsx"):
            writer = self._obj.to_excel
        else:
            raise ValueError(
                "File name does not have a pandas writer. Only .csv, .json, .xls and .xlsx files are supported."
            )

        # Get a temporary file
        temp_path = pathlib.Path(tempfile.mkdtemp()) / file_name

        # Write the file to the temporary location
        writer(temp_path, **kwargs)

        # Create an connection to the biglocalnews.org API
        client = Client(api_token, tier=tier)

        # Now upload that file to biglocalnews.org
        client.upload_file(project_id, temp_path)
