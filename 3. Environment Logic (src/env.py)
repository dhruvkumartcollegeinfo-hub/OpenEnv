from typing import Tuple, Dict, Any
from .models import Observation, Action, EnvState, Portfolio

class TradingEnv:
    def __init__(self):
        self.state = None
        self.initial_cash = 0.0

    def reset(self, task_config: Dict[str, Any] = None) -> Observation:
        task_config = task_config or {}
        self.initial_cash = task_config.get("initial_cash", 10000.0)
        
        self.state = EnvState(
            portfolio=Portfolio(cash=self.initial_cash, holdings={}, total_value=self.initial_cash),
            step_index=0,
            price_history=task_config.get("price_history", [{"MOCK": 100.0}])
        )
        return self._get_obs("Environment initialized. Market is open.")

    def step(self, action: Action) -> Tuple[Observation, float, bool, Dict]:
        feedback = ""
        penalty = 0.0
        
        current_prices = self.state.price_history[self.state.step_index]
        
        # 1. Execute Trade at current prices
        if action.action_type != "HOLD":
            if not action.ticker or action.ticker not in current_prices:
                feedback = f"Error: Invalid or missing ticker '{action.ticker}'."
                penalty = -10.0 # Penalize bad formatting
            elif not action.quantity or action.quantity <= 0:
                feedback = "Error: Quantity must be greater than 0."
                penalty = -10.0
            else:
                price = current_prices[action.ticker]
                cost = price * action.quantity
                
                if action.action_type == "BUY":
                    if self.state.portfolio.cash >= cost:
                        self.state.portfolio.cash -= cost
                        self.state.portfolio.holdings[action.ticker] = self.state.portfolio.holdings.get(action.ticker, 0) + action.quantity
                        feedback = f"Bought {action.quantity} {action.ticker} at ${price:.2f}"
                    else:
                        feedback = f"Error: Insufficient cash to buy {action.quantity} {action.ticker}."
                        penalty = -5.0
                        
                elif action.action_type == "SELL":
                    current_qty = self.state.portfolio.holdings.get(action.ticker, 0)
                    if current_qty >= action.quantity:
                        self.state.portfolio.cash += cost
                        self.state.portfolio.holdings[action.ticker] -= action.quantity
                        if self.state.portfolio.holdings[action.ticker] == 0:
                            del self.state.portfolio.holdings[action.ticker]
                        feedback = f"Sold {action.quantity} {action.ticker} at ${price:.2f}"
                    else:
                        feedback = f"Error: Insufficient holdings to sell {action.quantity} {action.ticker}."
                        penalty = -5.0
        else:
            feedback = "Held positions."

        # 2. Record old value, advance time
        old_value = self.state.portfolio.cash + sum(qty * current_prices[t] for t, qty in self.state.portfolio.holdings.items())
        
        self.state.step_index += 1
        done = self.state.step_index >= len(self.state.price_history) - 1
        
        # 3. Calculate new portfolio value at new prices
        new_prices = self.state.price_history[self.state.step_index]
        new_value = self.state.portfolio.cash + sum(qty * new_prices[t] for t, qty in self.state.portfolio.holdings.items())
        self.state.portfolio.total_value = new_value

        # Reward is the change in portfolio value + any formatting penalties
        reward = (new_value - old_value) + penalty
        
        if done:
            feedback += " Market Closed."

        return self._get_obs(feedback), reward, done, {}

    def state_info(self) -> EnvState:
        return self.state

    def _get_obs(self, feedback: str) -> Observation:
        return Observation(
            current_step=self.state.step_index,
            max_steps=len(self.state.price_history) - 1,
            portfolio=self.state.portfolio,
            current_prices=self.state.price_history[self.state.step_index],
            last_action_feedback=feedback
        )
