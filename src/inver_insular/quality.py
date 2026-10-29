import polars as pl


def missing_prices_report(df: pl.DataFrame) -> pl.DataFrame:
    has_price = pl.col("adj_close").is_not_null()
    trading_days = df.filter(has_price)["date"].n_unique()

    return (
        df.group_by("ticker")
        .agg(has_price.sum().alias("days_with_price"))
        .with_columns(pl.lit(trading_days).alias("trading_days"))
        .with_columns(
            (pl.col("trading_days") - pl.col("days_with_price")).alias("missing_days")
        )
        .sort("ticker")
    )
