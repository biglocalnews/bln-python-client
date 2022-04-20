import os

from bln import Client


def test_user():
    """Test everything method."""
    c = Client(tier=os.getenv("BLN_TEST_ENV", "dev"))
    e = c.everything()
    assert len(e) > 0
