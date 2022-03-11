import os

from bln.client import Client


def test_user():
    """Test everything method."""
    c = Client(tier=os.getenv("BLN_TEST_ENV", "dev"))
    e = c.everything()
    assert len(e) > 0
