from bln.client import Client


def test_files():
    """Test get_project_by_name method."""
    c = Client(tier="dev")
    p = c.get_project_by_name("WARN Act Notices")
    args = [p["id"], "test.csv"]
    c.upload_file(*args)
    c.download_file(*args)
    c.deleteFile(*args)
    c.upload_files(args[0], [args[1]])
    c.deleteFile(*args)
