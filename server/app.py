from fastapi import FastAPI, Body
from typing import Optional
import subprocess
from env.shortlisting_env import ShortlistingEnv
from env.tasks import TaskManager
from server.models import ShortlistingAction, ShortlistingObservation

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
@app.api_route("/reset", methods=["GET", "POST"])
def reset(seed: Optional[int] = None, task: Optional[str] = "easy"):
    """Resets the environment for a given task and seed."""
    state = task_manager.run_task(task, seed=seed)
    return {
        "observation": state,
        "reward": 0.0,
        "done": False,
        "info": {"task": task, "success": False}
    }

@app.api_route("/step", methods=["GET", "POST"])
def step(action_payload: Optional[ShortlistingAction] = None, action: Optional[str] = None):
    """Performs a step in the environment."""
    final_action = action
    if action_payload and action_payload.action:
        final_action = action_payload.action
    
    if not final_action:
        return {"error": "No action provided"}

    state, reward, done, info = env_instance.step(final_action)
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
