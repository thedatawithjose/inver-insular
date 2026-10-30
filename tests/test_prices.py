from pathlib import Path

import pandas as pd
import polars as pl
import pytest

from inver_insular import prices


def fake_download(*args: object, **kwargs: object) -> pd.DataFrame:
    dates = pd.DatetimeIndex(["2024-01-02", "2024-01-03"], name="Date")
    columns = pd.MultiIndex.from_product([["Close"], ["IEF", "SPY"]])
    values = [[95.0, 470.0], [95.5, 468.0]]
    return pd.DataFrame(values, index=dates, columns=columns)


def test_download_returns_long_table(monkeypatch: pytest.MonkeyPatch) -> None:
    # Reemplaza temporalmente yfinance.download por fake_download para aislar la prueba de internet.
    monkeypatch.setattr(prices.yf, "download", fake_download)

    # Llama a la función con una lista de tickers y rango de fechas.
    df = prices.download_prices(["SPY", "IEF"], "2024-01-01", "2024-01-04")

    # Verifica que las columnas estén en minúsculas y en formato largo: date, ticker, adj_close.
    assert df.columns == ["date", "ticker", "adj_close"]
    # Verifica la cantidad esperada de registros (2 fechas x 2 tickers = 4 filas).
    assert df.height == 4
    # Verifica que la columna de fecha se haya convertido correctamente a tipo pl.Date de Polars.
    assert df.schema["date"] == pl.Date


def test_save_prices_roundtrip(tmp_path: Path) -> None:
    # Prepara un DataFrame de prueba mínimo.
    df = pl.DataFrame({"ticker": ["SPY"], "adj_close": [470.0]})

    # Define la ruta destino dentro de una subcarpeta que aún no existe para verificar que se cree automáticamente.
    path = tmp_path / "raw" / "prices.parquet"

    # Guarda los datos en formato Parquet.
    prices.save_prices(df, path)

    # Lee el archivo Parquet guardado y valida que su contenido coincida exactamente con el original.
    assert pl.read_parquet(path).equals(df)
