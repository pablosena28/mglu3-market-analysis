"""Análise descritiva da MGLU3 em 2021."""

from pathlib import Path

import pandas as pd

from src.metrics import add_market_metrics, annualized_volatility, max_drawdown

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "raw" / "mglu3_2021.csv"


def main() -> None:
    raw = pd.read_csv(DATA_PATH)
    df = add_market_metrics(raw)

    start = df["Adj Close"].iloc[0]
    end = df["Adj Close"].iloc[-1]
    period_return = end / start - 1

    print("=== MGLU3 | 2021 ===")
    print(f"Pregões: {len(df)}")
    print(f"Preço ajustado inicial: R$ {start:.2f}")
    print(f"Preço ajustado final: R$ {end:.2f}")
    print(f"Retorno no período: {period_return:.2%}")
    print(f"Drawdown máximo: {max_drawdown(df['Adj Close']):.2%}")
    print(f"Volatilidade anualizada: {annualized_volatility(df['daily_return']):.2%}")

    print("\n=== EXTREMOS DIÁRIOS ===")
    best_idx = df["daily_return"].idxmax()
    worst_idx = df["daily_return"].idxmin()

    print(
        "Melhor pregão:",
        df.loc[best_idx, "Date"].date(),
        f"{df.loc[best_idx, 'daily_return']:.2%}",
    )
    print(
        "Pior pregão:",
        df.loc[worst_idx, "Date"].date(),
        f"{df.loc[worst_idx, 'daily_return']:.2%}",
    )

    print("\n=== RETORNOS MENSAIS ===")
    monthly_prices = df.set_index("Date")["Adj Close"].resample("ME").last()
    monthly = monthly_prices.pct_change()
    monthly.iloc[0] = monthly_prices.iloc[0] / df["Adj Close"].iloc[0] - 1

    print((monthly * 100).round(2).to_string())


if __name__ == "__main__":
    main()
