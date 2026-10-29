from pathlib import Path

import polars as pl

REQUIRED_COLUMNS = {"ticker", "asset_class", "target_weight"}
TOLERANCE = 1e-6


class PortfolioError(ValueError):
    """Raised when the client's portfolio file is invalid."""


def load_target_weights(path: Path) -> pl.DataFrame:
    df = pl.read_csv(path)

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise PortfolioError(f"Missing columns: {sorted(missing)}")

    if df["ticker"].is_duplicated().any():
        raise PortfolioError("Duplicated tickers found")

    if df["target_weight"].null_count() > 0:
        raise PortfolioError("Some target weights are empty")

    if (df["target_weight"] < 0).any():
        raise PortfolioError("Negative weights are not allowed")

    total = float(df["target_weight"].sum())
    if abs(total - 1.0) > TOLERANCE:
        raise PortfolioError(f"Weights sum to {total}, expected 1.0")

    return df
