from fastapi import FastAPI, Body
from typing import Optional
import subprocess
from env.shortlisting_env import ShortlistingEnv
from env.tasks import TaskManager
from models import ShortlistingAction, ShortlistingObservation

app = FastAPI()

# Global environment instance for OpenEnv compliance
env_instance = ShortlistingEnv()
task_manager = TaskManager(env_instance)

@app.get("/")
def home():
    return {"message": "Adaptive Shortlisting Env is running"}

@app.get("/run")
def run_inference():
    try:
        result = subprocess.run(
            ["python3", "inference.py"],
            capture_output=True,
            text=True,
            timeout=60
        )

        return {
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    except Exception as e:
        return {"error": str(e)}

# OpenEnv Compliance Endpoints
@app.post("/reset")
def reset(seed: Optional[int] = None, task: Optional[str] = "easy"):
    """Resets the environment for a given task and seed."""
    state = task_manager.run_task(task, seed=seed)
    return state

@app.post("/step")
def step(action_payload: ShortlistingAction):
    """Performs a step in the environment."""
    state, reward, done, info = env_instance.step(action_payload.action)
    return {
        "observation": state,
        "reward": reward,
        "done": done,
        "info": info
    }

@app.get("/state")
def state():
    """Returns the current state of the environment."""
    return env_instance.get_state()
