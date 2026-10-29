from pathlib import Path

import pytest

from inver_insular.portfolio import PortfolioError, load_target_weights

# Encabezado estándar requerido para generar archivos CSV válidos en los tests.
HEADER = "ticker,asset_class,target_weight\n"


def write_csv(tmp_path: Path, content: str) -> Path:
    # Función auxiliar para escribir rápidamente archivos CSV de prueba en una carpeta temporal.
    path = tmp_path / "weights.csv"
    path.write_text(content)
    return path


def test_valid_file_loads(tmp_path: Path) -> None:
    # Comprueba que un archivo con estructura y pesos válidos (0.6 + 0.4 = 1.0) se cargue con 2 filas.
    path = write_csv(tmp_path, HEADER + "SPY,equity,0.6\nIEF,bond,0.4\n")
    df = load_target_weights(path)
    assert df.height == 2


def test_missing_column_is_rejected(tmp_path: Path) -> None:
    # Comprueba que se lance PortfolioError cuando falta una columna obligatoria ('asset_class').
    path = write_csv(tmp_path, "ticker,target_weight\nSPY,1.0\n")
    with pytest.raises(PortfolioError, match="Missing columns"):
        load_target_weights(path)


def test_duplicated_ticker_is_rejected(tmp_path: Path) -> None:
    # Comprueba que se rechace un portafolio con tickers duplicados (SPY repetido).
    path = write_csv(tmp_path, HEADER + "SPY,equity,0.5\nSPY,equity,0.5\n")
    with pytest.raises(PortfolioError, match="Duplicated"):
        load_target_weights(path)


def test_empty_weight_is_rejected(tmp_path: Path) -> None:
    # Comprueba que se rechace el archivo si alguna ponderación está vacía o nula.
    path = write_csv(tmp_path, HEADER + "SPY,equity,\nIEF,bond,1.0\n")
    with pytest.raises(PortfolioError, match="empty"):
        load_target_weights(path)


def test_negative_weight_is_rejected(tmp_path: Path) -> None:
    # Comprueba que se rechacen ponderaciones negativas.
    path = write_csv(tmp_path, HEADER + "SPY,equity,1.5\nIEF,bond,-0.5\n")
    with pytest.raises(PortfolioError, match="Negative"):
        load_target_weights(path)


def test_weights_must_sum_to_one(tmp_path: Path) -> None:
    # Comprueba que se lance error si la suma de las ponderaciones difiere de 1.0 (ej. 0.5 + 0.3 = 0.8).
    path = write_csv(tmp_path, HEADER + "SPY,equity,0.5\nIEF,bond,0.3\n")
    with pytest.raises(PortfolioError, match="sum to"):
        load_target_weights(path)
