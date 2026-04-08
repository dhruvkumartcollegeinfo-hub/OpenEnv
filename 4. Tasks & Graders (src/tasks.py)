
from .env import TradingEnv

# --- TASK CONFIGURATIONS ---
TASKS = {
    "easy": { # Single asset, clear bull run. Just buy and hold.
        "initial_cash": 10000.0,
        "price_history": [
            {"AAPL": 100.0}, {"AAPL": 110.0}, {"AAPL": 120.0}, {"AAPL": 130.0}, {"AAPL": 150.0}
        ]
    },
    "medium": { # Two assets. One goes up, one crashes. Avoid the crash.
        "initial_cash": 10000.0,
        "price_history": [
            {"MSFT": 200.0, "TSLA": 200.0},
            {"MSFT": 210.0, "TSLA": 180.0},
            {"MSFT": 230.0, "TSLA": 150.0},
            {"MSFT": 240.0, "TSLA": 100.0},
            {"MSFT": 250.0, "TSLA": 50.0}
        ]
    },
    "hard": { # Volatile market. Buy low, sell high before the dip.
        "initial_cash": 10000.0,
        "price_history": [
            {"BTC": 40000.0, "ETH": 2000.0},
            {"BTC": 45000.0, "ETH": 2500.0}, # Peak
            {"BTC": 35000.0, "ETH": 1800.0}, # Crash
            {"BTC": 30000.0, "ETH": 1500.0},
            {"BTC": 38000.0, "ETH": 1900.0}  # Recovery
        ]
    }
}

# --- GRADERS ---
def calculate_score(env: TradingEnv, max_possible_profit: float) -> float:
    profit = env.state.portfolio.total_value - env.initial_cash
    if profit <= 0:
        return 0.0
    return min(1.0, profit / max_possible_profit)

def grade_easy(env: TradingEnv) -> float:
    # Max profit: Buy 100 AAPL at $100 -> Value at $150 = $15000. Profit = $5000
    return calculate_score(env, 5000.0)

def grade_medium(env: TradingEnv) -> float:
    # Max profit: Buy 50 MSFT at $200 -> Value at $250 = $12500. Profit = $2500
    return calculate_score(env, 2500.0)

def grade_hard(env: TradingEnv) -> float:
    # Max profit (approx): Buy ETH at 2000, sell at 2500 (Profit $2500). Wait out crash.
    # We set a reasonable "good trader" benchmark profit of $2500.
    return calculate_score(env, 2500.0)

GRADERS = {
    "easy": grade_easy,
    "medium": grade_medium,
    "hard": grade_hard
}
