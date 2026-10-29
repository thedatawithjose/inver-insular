from pathlib import Path

import polars as pl
import yfinance as yf  # type: ignore[import-untyped]


def download_prices(tickers: list[str], start: str, end: str) -> pl.DataFrame:
    # Descarga precios históricos desde Yahoo Finance para la lista de tickers indicada.
    # auto_adjust=True ajusta automáticamente por splits y dividendos.
    # progress=False desactiva la barra de progreso en consola.
    raw = yf.download(tickers, start=start, end=end, auto_adjust=True, progress=False)

    # Extrae los precios de cierre ('Close') e incluye la fecha como columna con reset_index.
    # Convierte el resultado de pandas a un DataFrame de Polars en formato ancho (fechas en filas, tickers en columnas).
    wide = pl.from_pandas(raw["Close"].reset_index())

    # Transforma y estandariza los datos para su posterior análisis:
    return (
        # Convierte de formato ancho a formato largo (unpivot):
        # Cada fila pasa a ser un par (fecha, ticker) con su precio ajustado.
        wide.unpivot(index="Date", variable_name="ticker", value_name="adj_close")
        # Estandariza el nombre de la columna 'Date' a minúsculas ('date').
        .rename({"Date": "date"})
        # Convierte la columna 'date' al tipo Date nativo de Polars (sin componente de hora).
        .with_columns(pl.col("date").cast(pl.Date))
    )


def save_prices(df: pl.DataFrame, path: Path) -> None:
    # Asegura que la carpeta contenedora exista antes de guardar (crea carpetas intermedias si faltan).
    path.parent.mkdir(parents=True, exist_ok=True)

    # Guarda el DataFrame en disco en formato Parquet (eficiente, columnar y ligero).
    df.write_parquet(path)
