def register(pd):
    """Register the Big Local News extensions to pandas.

    Args:
        pd (module): A pandas module you've imported elsewhere.
    """
    from pandas.api.extensions import register_dataframe_accessor

    from .read_bln import read_bln
    from .write_bln import BlnWriterAccessor

    pd.read_bln = read_bln
    register_dataframe_accessor("to_bln")(BlnWriterAccessor)
