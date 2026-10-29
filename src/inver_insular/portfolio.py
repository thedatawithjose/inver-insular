from pathlib import Path

import polars as pl

# Columnas obligatorias que debe contener el archivo CSV del portafolio.
REQUIRED_COLUMNS = {"ticker", "asset_class", "target_weight"}
# Margen de tolerancia para comparaciones numéricas de punto flotante al validar la suma de pesos.
TOLERANCE = 1e-6


class PortfolioError(ValueError):
    """Raised when the client's portfolio file is invalid."""


def load_target_weights(path: Path) -> pl.DataFrame:
    # Carga el archivo CSV con las ponderaciones objetivo usando Polars.
    df = pl.read_csv(path)

    # 1. Validación de columnas obligatorias:
    # Comprueba que no falte ninguna de las columnas requeridas ('ticker', 'asset_class', 'target_weight').
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise PortfolioError(f"Missing columns: {sorted(missing)}")

    # 2. Validación de tickers únicos:
    # Evita que existan activos duplicados en la asignación del portafolio.
    if df["ticker"].is_duplicated().any():
        raise PortfolioError("Duplicated tickers found")

    # 3. Validación de valores nulos o vacíos:
    # Verifica que cada fila tenga un peso asignado.
    if df["target_weight"].null_count() > 0:
        raise PortfolioError("Some target weights are empty")

    # 4. Validación de no negatividad:
    # Asegura que no existan ponderaciones negativas (no se permiten posiciones cortas).
    if (df["target_weight"] < 0).any():
        raise PortfolioError("Negative weights are not allowed")

    # 5. Validación de la suma total:
    # Comprueba que la suma de todos los pesos sea igual a 1.0 (100%), permitiendo un margen por tolerancia numérica.
    total = float(df["target_weight"].sum())
    if abs(total - 1.0) > TOLERANCE:
        raise PortfolioError(f"Weights sum to {total}, expected 1.0")

    return df
