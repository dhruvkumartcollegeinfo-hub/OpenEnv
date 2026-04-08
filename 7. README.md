# Trading Agent Environment

## Description
This OpenEnv project simulates a quantitative trading environment. An AI agent is tasked with managing a cash portfolio, observing dynamic market prices across discrete time steps, and executing trades to maximize its overall return on investment (ROI).

## Action Space
The agent outputs a JSON matching the `Action` model:
- `action_type`: "BUY", "SELL", or "HOLD"
- `ticker`: (Optional) String representing the asset symbol (e.g., "AAPL").
- `quantity`: (Optional) Integer amount of shares/coins to transact.

## Observation Space
- `current_step` / `max_steps`: Time progression.
- `portfolio`: Current cash balance, holding quantities, and total portfolio value.
- `current_prices`: Dictionary of ticker symbols to their current market price.
- `last_action_feedback`: String indicating success or error of the previous trade.

## Tasks & Grading
Grading is deterministic, based on achieving a target profit derived from an optimal trading strategy.
1. **Easy**: Single asset in a clear bull market. Agent must buy and hold to score 1.0.
2. **Medium**: Two assets with divergent trends. Agent must identify the winning asset and allocate capital appropriately.
3. **Hard**: Volatile crypto market. Agent must buy low, sell high at the peak, and avoid the subsequent market crash.

## Setup & Usage
1. Install dependencies: `pip install -r requirements.txt`
2. Export your API credentials:
   ```bash
   export API_BASE_URL="your_api_url"
   export MODEL_NAME="your_model"
   export HF_TOKEN="your_api_key"
