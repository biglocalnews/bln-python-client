from bln.client import Client


def test_user():
    """Test everything method."""
    c = Client(tier="dev")
    e = c.everything()
    assert len(e) > 0
