from importlib.metadata import PackageNotFoundError, version

distribution_name = "bln"

try:
    __version__ = version("bln")
except PackageNotFoundError:
    # Package is not installed (e.g., during local development)
    __version__ = "0.0.0"
