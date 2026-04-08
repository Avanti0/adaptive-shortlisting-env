import random
import sys
import json
from env.shortlisting_env import ShortlistingEnv
from env.tasks import TaskManager, grade_task


def run_agent(task_manager, task_name, seed=None):
    env = task_manager.env
    state = task_manager.run_task(task_name, seed=seed)

    steps = []
    done = False

    while not done:
        # Choose action
        if env.candidates:
            action = random.choice(env.candidates)
        else:
            action = random.choice(env.all_candidates)

        state, reward, done, info = env.step(action)

        steps.append({
            "action": action,
            "reward": round(reward, 4),
            "attempt": state["attempts"],
            "remaining": state["remaining_candidates"],
            "done": done
        })

    final_score = grade_task(env)

    return {
        "task": task_name,
        "steps": steps,
        "score": round(final_score, 2)
    }


if __name__ == "__main__":
    # Initialize
    env = ShortlistingEnv()
    tm = TaskManager(env)

    # Read difficulty from argument
    task = sys.argv[1] if len(sys.argv) > 1 else "easy"

    result = run_agent(tm, task, seed=42)

    # Output JSON (important for UI)
    print(json.dumps(result))
