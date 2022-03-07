# Getting started

```{contents} Sections
  :depth: 1
  :local:
```

## Setup

### Installation

The Python SDK can be installed using `pip`.

```bash
pip install bln
```

### Getting an API Key

API keys can be generated at https://biglocalnews.org/.

1. Log into Big Local News using your Google account.
2. Expand the Developer menu item in the left sidebar.
3. Click Manage Keys.
4. Generate a key and copy it to the clipboard.
5. Export the token to your environment

```bash
export BLN_API_KEY = "<Paste your API Key here>"
```

### Initializing the SDK client

The client is what will handle calls to the Big Local News API. To set up it you must authorize the client using your API key.

```python
from bln.client import Client

client = Client()
```

## Working with projects

### Creating a project

To create a project, use the client's `createProject` method. The only argument required to create a project is a name. However, it is helpful to include a description. The `createProject` method will return a dictionary of project metadata if it is successful and `None` if it fails.

```python
project_name = "Big Local News SDK Demo Project"
project_description = "This is a sample project to show users how the SDK works"

project = client.createProject(project_name, description=project_description)
```

### Get metadata for an existing project

Helper methods can assist you with selecting projects by name or id. It will return one and only one project.

```python
client.get_project_by_name("Big Local News SDK Demo Project")
client.get_project_by_id(project_id)
```

The client's `search_projects` method can be used to for more complex queries. It takes a lambda function that returns `True` or `False` based on whether or not the project metadata meets the search criteria. The `search_projects` method will return a list of project metadata for those projects matching the search query.

```python
client.search_projects(lambda project: "SDK" in project["description"])
```

### Updating project metadata

The client's `updateProject` method is used to edit project metadata. It takes the project's ID as a required argument and optional keyword arguments to update the metadata. The method will return the updated project metadata.

```python
new_name = "Big Local News SDK Demo Project - edited"
new_description = "This is a sample project to show users how the SDK works. The description and name have been edited."

client.updateProject(project_id, name=new_name, description=new_description)
```

### Deleting a project

Use the client's `deleteProject` method to delete a project. The method requires a project ID as it's sole argument.

**WARNING: This process is irreversible. Use with caution.**

```python
client.deleteProject(project_id)
```

## Working with files

The SDK client has a host of methods available for working with files. All of the methods will require a project ID as an argument.

### Uploading

The client has two different methods for file uploads - one for a single file and a second for batch uploads.

#### A single file

```python
client.upload_file(project_id, "./data/demo_a.csv")
```

#### Multiple files

The SDK client also has an `upload_files` method which takes a list of files as an argument.

```python
client.upload_files(project_id, files_to_upload)
```

### Viewing files in a project

```python
# Get the first project returned from a search
project = client.search_projects(lambda project: project["id"] == project_id)[0]

project["files"]

[
    {
        "createdAt": "2022-01-12T23:40:44.443000+00:00",
        "name": "demo_a.csv",
        "tags": [],
        "updatedAt": "2022-01-12T23:40:44.443000+00:00",
    },
    {
        "createdAt": "2022-01-12T23:40:46.372000+00:00",
        "name": "demo_b.csv",
        "tags": [],
        "updatedAt": "2022-01-12T23:40:46.372000+00:00",
    },
]
```

### Downloading a file

The client's `download_file` takes three arguments: project ID, filename and an optional output directory. If an output directory is not specified, the client will download to the current working directory.

```python
client.download_file(project_id, "demo_a.csv", output_dir="./data")
```
