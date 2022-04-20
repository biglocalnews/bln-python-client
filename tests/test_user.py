import os

from bln import Client


def test_user():
    """Test user methods."""
    c = Client(tier=os.getenv("BLN_TEST_ENV", "dev"))
    c.user()
