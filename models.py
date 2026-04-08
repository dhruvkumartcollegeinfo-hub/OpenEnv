from pydantic import BaseModel
from typing import Dict, List, Optional, Literal

class Portfolio(BaseModel):
    cash: float
    holdings: Dict[str, int] # Ticker -> Quantity
    total_value: float

class Observation(BaseModel):
    current_step: int
    max_steps: int
    portfolio: Portfolio
    current_prices: Dict[str, float]
    last_action_feedback: str

class Action(BaseModel):
    action_type: Literal["BUY", "SELL", "HOLD"]
    ticker: Optional[str] = None
    quantity: Optional[int] = None

class EnvState(BaseModel):
    portfolio: Portfolio
    step_index: int
    price_history: List[Dict[str, float]]
