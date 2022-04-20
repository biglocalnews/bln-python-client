import os

from bln import Client


def test_files():
    """Test file methods."""
    c = Client(tier=os.getenv("BLN_TEST_ENV", "dev"))
    p = c.get_project_by_name("WARN Act Notices")
    c.upload_file(p["id"], "tests/test.csv")
    c.download_file(p["id"], "test.csv")
    c.deleteFile(p["id"], "test.csv")
    c.upload_files(p["id"], ["tests/test.csv"])
    c.deleteFile(p["id"], "test.csv")
