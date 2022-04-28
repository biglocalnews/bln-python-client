import os

import bln
import pandas as pd

bln.pandas.register(pd)


def test_pandas_read():
    """Test the `read_bln` method."""
    project_id = "UHJvamVjdDpiZGM5NmU1MS1kMzBhLTRlYTctODY4Yi04ZGI4N2RjMzQ1ODI="
    file_name = "ia.csv"
    tier = os.getenv("BLN_TEST_ENV", "dev")
    df = pd.read_bln(project_id, file_name, tier=tier)
    assert len(df) > 0


def test_pandas_write():
    """Test the `writer_bln` method."""
    df = pd.read_csv("tests/test.csv")
    project_id = "UHJvamVjdDpiZGM5NmU1MS1kMzBhLTRlYTctODY4Yi04ZGI4N2RjMzQ1ODI="
    file_name = "test.csv"
    tier = os.getenv("BLN_TEST_ENV", "dev")
    df.to_bln(project_id, file_name, tier=tier, index=False)
