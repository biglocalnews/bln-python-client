try:
    import pandas as pd
except ImportError:
    raise ImportError("pandas must be installed to take advantage of this module")

from .read_bln import read_bln

pd.read_bln = read_bln
