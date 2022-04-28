try:
    import pandas as pd
except ImportError:
    raise ImportError("pandas must be installed to take advantage of this module")

from pandas.api.extensions import register_dataframe_accessor

# Import our tools
from .read_bln import read_bln
from .write_bln import BlnWriterAccessor

# Monkeypatch pandas
pd.read_bln = read_bln
register_dataframe_accessor('to_bln')(BlnWriterAccessor)
