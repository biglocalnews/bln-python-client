import os

from bln import Client


def test_files():
    """Test file methods."""
    c = Client(tier=os.getenv("BLN_TEST_ENV", "dev"))
    p = c.get_project_by_name("WARN Act Notices")
    args = [p["id"], "tests/test.csv"]
    c.upload_file(*args)
    c.download_file(*args)
    c.deleteFile(*args)
    c.upload_files(args[0], [args[1]])
    c.deleteFile(*args)
