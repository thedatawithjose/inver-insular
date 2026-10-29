from pathlib import Path

import pytest

from inver_insular.portfolio import PortfolioError, load_target_weights

HEADER = "ticker,asset_class,target_weight\n"


def write_csv(tmp_path: Path, content: str) -> Path:
    path = tmp_path / "weights.csv"
    path.write_text(content)
    return path


def test_valid_file_loads(tmp_path: Path) -> None:
    path = write_csv(tmp_path, HEADER + "SPY,equity,0.6\nIEF,bond,0.4\n")
    df = load_target_weights(path)
    assert df.height == 2


def test_missing_column_is_rejected(tmp_path: Path) -> None:
    path = write_csv(tmp_path, "ticker,target_weight\nSPY,1.0\n")
    with pytest.raises(PortfolioError, match="Missing columns"):
        load_target_weights(path)


def test_duplicated_ticker_is_rejected(tmp_path: Path) -> None:
    path = write_csv(tmp_path, HEADER + "SPY,equity,0.5\nSPY,equity,0.5\n")
    with pytest.raises(PortfolioError, match="Duplicated"):
        load_target_weights(path)


def test_empty_weight_is_rejected(tmp_path: Path) -> None:
    path = write_csv(tmp_path, HEADER + "SPY,equity,\nIEF,bond,1.0\n")
    with pytest.raises(PortfolioError, match="empty"):
        load_target_weights(path)


def test_negative_weight_is_rejected(tmp_path: Path) -> None:
    path = write_csv(tmp_path, HEADER + "SPY,equity,1.5\nIEF,bond,-0.5\n")
    with pytest.raises(PortfolioError, match="Negative"):
        load_target_weights(path)


def test_weights_must_sum_to_one(tmp_path: Path) -> None:
    path = write_csv(tmp_path, HEADER + "SPY,equity,0.5\nIEF,bond,0.3\n")
    with pytest.raises(PortfolioError, match="sum to"):
        load_target_weights(path)
