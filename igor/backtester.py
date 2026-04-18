"""
Backtester for the HRT Datathon 2026.

Usage
-----
    from backtester import backtest

    # predictions: DataFrame or dict with keys 'session' and 'volume'
    # (volume = target_position in the submission format)
    results = backtest(predictions)
    print(results)

The metric mirrors the competition definition:
    pnl_i = volume_i * (close_end_i / close_halfway_i - 1)
    sharpe  = mean(pnl) / std(pnl) * 16
"""

import numpy as np
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

HALFWAY_BAR = 49   # last seen bar index
END_BAR     = 99   # last unseen bar index


def _load_prices() -> pd.DataFrame:
    """Return a DataFrame indexed by session with halfway and end close prices."""
    seen   = pd.read_parquet(DATA_DIR / "bars_seen_train.parquet",   engine="fastparquet")
    unseen = pd.read_parquet(DATA_DIR / "bars_unseen_train.parquet", engine="fastparquet")

    halfway = (
        seen[seen["bar_ix"] == HALFWAY_BAR]
        .set_index("session")["close"]
        .rename("close_halfway")
    )
    end = (
        unseen[unseen["bar_ix"] == END_BAR]
        .set_index("session")["close"]
        .rename("close_end")
    )
    return pd.concat([halfway, end], axis=1).dropna()


def backtest(
    predictions,
    verbose: bool = True,
) -> pd.DataFrame:
    """
    Evaluate a set of trading predictions against the training ground truth.

    Parameters
    ----------
    predictions : DataFrame with columns ['session', 'volume']
                  OR dict mapping session -> volume
                  'volume' is the target_position (number of shares to buy/sell).
    verbose     : print a summary table to stdout.

    Returns
    -------
    pd.DataFrame with per-session columns:
        session, volume, close_halfway, close_end, pnl
    and a printed summary (sharpe, mean_pnl, std_pnl, win_rate).
    """
    # Normalise input to DataFrame
    if isinstance(predictions, dict):
        df = pd.DataFrame(
            list(predictions.items()), columns=["session", "volume"]
        )
    else:
        df = pd.DataFrame(predictions).rename(
            columns={"target_position": "volume"}
        )[["session", "volume"]]

    prices = _load_prices()

    result = df.merge(prices, on="session", how="inner")
    missing = len(df) - len(result)
    if missing:
        print(f"[backtester] Warning: {missing} session(s) not found in train data.")

    result["ret"] = result["close_end"] / result["close_halfway"] - 1
    result["pnl"] = result["volume"] * result["ret"]

    pnl = result["pnl"]
    sharpe   = pnl.mean() / pnl.std() * 16 if pnl.std() > 0 else np.nan
    mean_pnl = pnl.mean()
    std_pnl  = pnl.std()
    win_rate = (pnl > 0).mean()

    if verbose:
        print("=" * 40)
        print(f"  Sessions evaluated : {len(result)}")
        print(f"  Sharpe ratio       : {sharpe:+.4f}")
        print(f"  Mean PnL           : {mean_pnl:+.6f}")
        print(f"  Std  PnL           : {std_pnl:.6f}")
        print(f"  Win rate           : {win_rate:.2%}")
        print("=" * 40)

    result.attrs["sharpe"]   = sharpe
    result.attrs["mean_pnl"] = mean_pnl
    result.attrs["std_pnl"]  = std_pnl
    result.attrs["win_rate"] = win_rate

    return result
