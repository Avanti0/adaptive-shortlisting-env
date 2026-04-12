import os
import random

try:
    from openai import OpenAI
    client = None
    try:
        API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
        MODEL_NAME = os.getenv("MODEL_NAME", "baseline-agent")
        HF_TOKEN = os.getenv("HF_TOKEN") or "dummy"
        client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)
    except Exception:
        client = None
except ImportError:
    client = None
    API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
    MODEL_NAME = os.getenv("MODEL_NAME", "baseline-agent")

from env.shortlisting_env import ShortlistingEnv
from env.tasks import TaskManager, grade_task


def get_action(env):
    action = None
    try:
        if env.candidates:
            candidates = env.candidates
        else:
            candidates = env.all_candidates
        if candidates:
            action = random.choice(candidates)
    except Exception:
        pass
    
    if not action:
        try:
            action = random.choice(env.all_candidates)
        except Exception:
            action = "candidate_0"
    
    return action


def run_agent(task_manager, task_name, seed=None):
    env = None
    rewards = []
    steps = 0
    score = 0.0
    success = False
    started = False
    
    try:
        env = task_manager.env
        task_manager.run_task(task_name, seed=seed)
        started = True
        print(f"[START] task={task_name} env=shortlisting model={MODEL_NAME}", flush=True)
    except Exception as e:
        print(f"[START] task={task_name} env=shortlisting model={MODEL_NAME}", flush=True)
        print(f"[STEP] step=1 action=_error_ reward=0.00 done=true error={str(e).replace(chr(10), ' ').strip()}", flush=True)
        print(f"[END] success=false steps=1 score=0.00 rewards=0.00", flush=True)
        return
    
    try:
        done = False
        while not done:
            action = get_action(env)
            
            if not action:
                action = "candidate_0"
            
            try:
                state, reward, done, info = env.step(action)
                error = "null"
            except Exception as e:
                reward = 0.0
                done = True
                error = str(e).replace("\n", " ").strip() if e else "null"
            
            steps += 1
            rewards.append(reward)
            
            print(f"[STEP] step={steps} action={action} reward={reward:.2f} done={str(done).lower()} error={error}", flush=True)
        
        score = grade_task(env)
        score = max(0.0, min(score, 1.0))
        success = score >= 0.5
    except Exception as e:
        rewards_str = ",".join([f"{r:.2f}" for r in rewards]) if rewards else "0.00"
        print(f"[END] success=false steps={steps} score=0.00 rewards={rewards_str}", flush=True)
        return
    
    rewards_str = ",".join([f"{r:.2f}" for r in rewards])
    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards_str}",
        flush=True
    )


if __name__ == "__main__":
    try:
        env = ShortlistingEnv()
        tm = TaskManager(env)
    except Exception as e:
        print(f"[START] task=easy env=shortlisting model={MODEL_NAME}", flush=True)
        print(f"[STEP] step=1 action=_error_ reward=0.00 done=true error={str(e).replace(chr(10), ' ').strip()}", flush=True)
        print(f"[END] success=false steps=1 score=0.00 rewards=0.00", flush=True)
        print(f"[START] task=medium env=shortlisting model={MODEL_NAME}", flush=True)
        print(f"[STEP] step=1 action=_error_ reward=0.00 done=true error={str(e).replace(chr(10), ' ').strip()}", flush=True)
        print(f"[END] success=false steps=1 score=0.00 rewards=0.00", flush=True)
        print(f"[START] task=hard env=shortlisting model={MODEL_NAME}", flush=True)
        print(f"[STEP] step=1 action=_error_ reward=0.00 done=true error={str(e).replace(chr(10), ' ').strip()}", flush=True)
        print(f"[END] success=false steps=1 score=0.00 rewards=0.00", flush=True)
        exit(1)
    
    tasks = ["easy", "medium", "hard"]
    seed = 42
    
    for task in tasks:
        run_agent(tm, task, seed)
        seed += 1