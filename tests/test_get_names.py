from bln.client import Client


def test_get_name():
    """Test methods that get user and group names."""
    c = Client(tier="dev")
    c.userNames()
    c.groupNames()
