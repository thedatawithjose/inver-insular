import polars as pl

from inver_insular.quality import invalid_prices_report, missing_prices_report


def test_missing_days_are_counted() -> None:
    df = pl.DataFrame(
        {
            "date": ["2024-01-02", "2024-01-02", "2024-01-03", "2024-01-03"],
            "ticker": ["SPY", "JNJ", "SPY", "JNJ"],
            "adj_close": [470.0, 160.0, 468.0, None],
        }
    )

    report = missing_prices_report(df)

    assert report["ticker"].to_list() == ["JNJ", "SPY"]
    assert report["missing_days"].to_list() == [1, 0]
    assert report["trading_days"].to_list() == [2, 2]


def test_invalid_prices_are_counted() -> None:
    df = pl.DataFrame(
        {
            "date": ["2024-01-02", "2024-01-02", "2024-01-03", "2024-01-03"],
            "ticker": ["SPY", "JNJ", "SPY", "JNJ"],
            "adj_close": [470.0, 0.0, 468.0, -5.0],
        }
    )

    report = invalid_prices_report(df)

    assert report["ticker"].to_list() == ["JNJ", "SPY"]
    assert report["invalid_prices"].to_list() == [2, 0]
