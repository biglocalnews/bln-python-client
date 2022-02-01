from bln.client import Client


def test_get_project_by_name():
    """Test get_project_by_name method."""
    c = Client()
    p = c.get_project_by_name("WARN Act Notices")
    assert p["name"] == "WARN Act Notices"
