import os
import random
from openai import OpenAI

from env.shortlisting_env import ShortlistingEnv
from env.tasks import TaskManager, grade_task

# =========================
# REQUIRED ENV VARIABLES
# =========================
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "baseline-agent")
HF_TOKEN = os.getenv("HF_TOKEN") or "dummy"  # fallback to avoid crash

# Initialize OpenAI client (MANDATORY as per checklist)
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

# =========================
# SAFE ACTION FUNCTION
# =========================
def get_action(env):
    """
    Safe action selector with fallback.
    Currently uses random baseline but structured for LLM extension.
    """
    try:
        if env.candidates:
            action = random.choice(env.candidates)
        else:
            action = random.choice(env.all_candidates)
    except Exception:
        # ultimate fallback (never crash)
        action = random.choice(env.all_candidates)

    # extra safety
    if not action:
        action = random.choice(env.all_candidates)

    return action


# =========================
# AGENT RUNNER
# =========================
def run_agent(task_manager, task_name, seed=None):
    env = task_manager.env
    state = task_manager.run_task(task_name, seed=seed)

    rewards = []
    steps = 0

    # START LOG (STRICT FORMAT)
    print(f"[START] task={task_name} env=shortlisting model={MODEL_NAME}", flush=True)

    done = False
    while not done:
        # SAFE ACTION SELECTION
        action = get_action(env)

        try:
            state, reward, done, info = env.step(action)
            error = "null"
        except Exception as e:
            reward = 0.0
            done = True
            error = str(e)

        steps += 1
        rewards.append(reward)

        # STEP LOG (STRICT FORMAT)
        print(
            f"[STEP] step={steps} action={action} reward={reward:.2f} done={str(done).lower()} error={error}",
            flush=True
        )

    # Compute score
    score = grade_task(env)
    score = max(0.0, min(score, 1.0))  # clamp to [0,1]

    # Success condition
    success = score >= 0.5

    # END LOG (STRICT FORMAT)
    rewards_str = ",".join([f"{r:.2f}" for r in rewards])
    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards_str}",
        flush=True
    )


# =========================
# MAIN EXECUTION
# =========================
if __name__ == "__main__":
    env = ShortlistingEnv()
    tm = TaskManager(env)

    tasks = ["easy", "medium", "hard"]
    seed = 42

    for task in tasks:
        run_agent(tm, task, seed)
        seed += 1
