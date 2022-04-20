import os

from bln import Client


def test_get_name():
    """Test methods that get user and group names."""
    c = Client(tier=os.getenv("BLN_TEST_ENV", "dev"))
    c.userNames()
    c.groupNames()
