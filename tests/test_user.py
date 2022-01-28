from bln.client import Client


def test_user():
    """Test user methods."""
    c = Client()
    c.user()
