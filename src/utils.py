import logging
import duckdb
import polars as pl
import pandas as pd
from typing import Dict

DB_PATH = "db.db"


def setup_logging(level: int = logging.INFO) -> None:
    """Configure root logger."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )


def get_connection(path: str = DB_PATH):
    """Return a new DuckDB connection."""
    return duckdb.connect(path)


def load_curated(con) -> pl.DataFrame:
    """Load curated_risk_data into a Polars DataFrame."""
    return pl.from_arrow(
        con.execute("SELECT * FROM curated_risk_data").arrow()
    )


def group_by_asset_class(
    df: pl.DataFrame,
    agg_dict: Dict[str, str],
    rename_map: Dict[str, str]
) -> pd.DataFrame:
    """
    Group by asset_class using pandas fallback and rename columns.

    df: Polars DataFrame
    agg_dict: mapping of column -> pandas agg function
    rename_map: mapping of original column -> new name
    """
    pdf = df.to_pandas()
    report = pdf.groupby('asset_class').agg(agg_dict)
    # rename only existing columns
    report = report.rename(
        columns={k: v for k, v in rename_map.items() if k in report.columns}
    )
    return report
