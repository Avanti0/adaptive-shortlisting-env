from fastapi import FastAPI
import uvicorn
from env.shortlisting_env import ShortlistingEnv
from env.tasks import TaskManager

app = FastAPI()

# Global instances (DO NOT CHANGE)
env_instance = ShortlistingEnv()
task_manager = TaskManager(env_instance)


# ---- EXISTING ROUTES (keep yours here, unchanged) ----
# (Do NOT delete your endpoints — just keep them below)
@app.post("/reset")
def reset():
    env_instance.reset()
    return {"status": "reset done"}


@app.post("/step")
def step(action: dict):
    act = action.get("action", "candidate_0")
    state, reward, done, info = env_instance.step(act)

    return {
        "state": state,
        "reward": reward,
        "done": done,
        "info": info
    }


# ---- ENTRYPOINT FIX ----
def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()

