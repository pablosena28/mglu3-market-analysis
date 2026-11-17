"""Métricas de risco e retorno para séries de preços."""

from __future__ import annotations

import numpy as np
import pandas as pd


def add_market_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Adiciona retorno, retorno acumulado, médias móveis, drawdown e volatilidade."""
    data = df.copy()
    data["Date"] = pd.to_datetime(data["Date"])
    data = data.sort_values("Date").reset_index(drop=True)

    data["daily_return"] = data["Adj Close"].pct_change()
    data["cumulative_return"] = data["Adj Close"] / data["Adj Close"].iloc[0] - 1
    data["sma_20"] = data["Adj Close"].rolling(20).mean()
    data["sma_50"] = data["Adj Close"].rolling(50).mean()

    running_peak = data["Adj Close"].cummax()
    data["drawdown"] = data["Adj Close"] / running_peak - 1
    data["rolling_vol_21"] = data["daily_return"].rolling(21).std() * np.sqrt(252)

    return data


def max_drawdown(price: pd.Series) -> float:
    """Retorna o maior drawdown da série."""
    running_peak = price.cummax()
    drawdown = price / running_peak - 1
    return float(drawdown.min())


def annualized_volatility(returns: pd.Series, periods: int = 252) -> float:
    """Calcula volatilidade anualizada a partir de retornos periódicos."""
    return float(returns.dropna().std() * np.sqrt(periods))
