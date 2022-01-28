from bln.client import Client

TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODM0NDI1OTUsIm5iZiI6MTU4MzQ0MjU5NSwianRpIjoiMjcwMWQ0MjMtOWIyYi00MDdkLTg3OGUtNjA1YWYxMThkOGIxIiwiaWRlbnRpdHkiOiJiY2ExMjQ3NC1hYWQzLTRmYWMtOWEzMS01MTA0Nzc3ZTUxNDQiLCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MifQ.gohSFNcJ_fPpVSsktyNo66ul9oPpsbM3jrt_aGFWBoM"


def test_user():
    """Test user methods."""
    c = Client(TOKEN)
    c.user()
