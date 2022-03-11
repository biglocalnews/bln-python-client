import os

from bln.client import Client


def test_get_project_by_name():
    """Test get_project_by_name method."""
    c = Client(tier=os.getenv("BLN_TEST_ENV", "dev"))
    name = "WARN Act Notices"
    p = c.get_project_by_name(name)
    assert p["name"] == name


def test_get_project_by_id():
    """Test get_project_by_id method."""
    c = Client(tier=os.getenv("BLN_TEST_ENV", "dev"))
    id = "UHJvamVjdDpiZGM5NmU1MS1kMzBhLTRlYTctODY4Yi04ZGI4N2RjMzQ1ODI="
    p = c.get_project_by_id(id)
    assert p["id"] == id
