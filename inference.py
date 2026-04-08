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
        # ... (keep your prompt and client.chat.completions logic)
        
        try:
            action_dict = json.loads(response.choices[0].message.content)
            from src.models import Action
            action = Action(**action_dict)
            
            # Execute step
            obs, reward, done, info = env.step(action)
            
            # IMPROVED LOGGING: Use the feedback from the observation
            print(f"[STEP] {obs.current_step} Action: {action.action_type} {action.ticker or ''}")
            print(f"[STEP] {obs.current_step} Feedback: {obs.last_action_feedback}")
            print(f"[STEP] {obs.current_step} Reward: {reward:.2f}")
            print(f"[STEP] {obs.current_step} Portfolio Value: {obs.portfolio.total_value:.2f}")
            
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
