import os
import random

from bln.client import Client


def test_create_project():
    """Test creating and deleting a project."""
    c = Client(tier=os.getenv("BLN_TEST_ENV", "dev"))
    name = f"Test project {random.randint(0, 100)}"
    c.createProject(name)
    p = c.get_project_by_name(name)
    assert p["name"] == name
    c.deleteProject(p["id"])
