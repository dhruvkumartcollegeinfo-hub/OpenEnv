import os
import json
from openai import OpenAI
from src.env import TradingEnv
from src.tasks import TASKS, GRADERS

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4-turbo")
HF_TOKEN = os.getenv("HF_TOKEN")

client = OpenAI(api_key=HF_TOKEN, base_url=API_BASE_URL)

def run_inference(task_name: str):
    env = TradingEnv()
    obs = env.reset(TASKS[task_name])
    
    print(f"[START] Task: {task_name}")
    print(f"[START] Initial Observation: {obs.model_dump_json()}")
    
    done = False
    
    while not done:
        prompt = f"""
        You are a Quantitative Trading AI. Maximize your portfolio value.
        Current Observation: {obs.model_dump_json()}
        Determine your next trade. You can BUY, SELL, or HOLD. You must specify the ticker and quantity if buying or selling.
        Respond ONLY with a JSON object matching this schema:
        {{"action_type": "BUY" | "SELL" | "HOLD", "ticker": "str (optional)", "quantity": int (optional)}}
        """
        
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        try:
            action_dict = json.loads(response.choices[0].message.content)
            from src.models import Action
            action = Action(**action_dict)
            
            print(f"[STEP] {obs.current_step} Action: {action.model_dump_json()}")
            obs, reward, done, info = env.step(action)
            
            print(f"[STEP] {obs.current_step} Observation: {obs.model_dump_json()}")
            print(f"[STEP] {obs.current_step} Reward: {reward:.2f}")
            
        except Exception as e:
            print(f"[STEP] {obs.current_step} Error: {e}")
            break
            
    final_score = GRADERS[task_name](env)
    print(f"[END] Task: {task_name} completed.")
    print(f"[END] Final Score: {final_score:.2f}")
    print("-" * 40)

if __name__ == "__main__":
    if not HF_TOKEN:
        print("Error: HF_TOKEN environment variable not set.")
        exit(1)
        
    for task in ["easy", "medium", "hard"]:
        run_inference(task)
