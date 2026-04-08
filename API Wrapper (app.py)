from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, Optional
from src.env import TradingEnv
from src.models import Action, Observation, EnvState

app = FastAPI(title="Trading Agent Environment API")
env = TradingEnv()

class ResetRequest(BaseModel):
    task_config: Optional[Dict[str, Any]] = None

@app.get("/")
def health_check():
    return {"status": "running", "environment": "trading-agent-env"}

@app.post("/reset", response_model=Observation)
def reset_env(request: ResetRequest = ResetRequest()):
    try:
        return env.reset(request.task_config)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/step")
def step_env(action: Action):
    try:
        obs, reward, done, info = env.step(action)
        return {"observation": obs.model_dump(), "reward": reward, "done": done, "info": info}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/state", response_model=EnvState)
def get_state():
    return env.state_info()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
