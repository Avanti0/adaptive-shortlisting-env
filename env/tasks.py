import random
from env.shortlisting_env import ShortlistingEnv

def get_easy_pool(env):
    """Returns a subset of 100 words for the Easy task."""
    random.seed(42) # Deterministic pool for task consistency
    return random.sample(env.original_candidates, 100)

def get_medium_pool(env):
    """Returns a subset of 1000 words for the Medium task."""
    random.seed(42)
    return random.sample(env.original_candidates, 1000)

def get_hard_pool(env):
    """Returns the full list of candidates for the Hard task."""
    return env.original_candidates

def grade_task(env):
    """
    Standard grader:
    - 1.0 if solved in <= 3 attempts.
    - 0.5 if solved but took > 3 attempts.
    - 0.0 if not solved.
    """
    if env.solved:
        if env.solved_in <= 3:
            return 1.0
        else:
            return 0.5
    return 0.0

class TaskManager:
    def __init__(self, env):
        self.env = env
        self.tasks = {
            "easy": get_easy_pool(self.env),
            "medium": get_medium_pool(self.env),
            "hard": get_hard_pool(self.env)
        }

    def run_task(self, task_name, seed=None):
        if task_name not in self.tasks:
            raise ValueError(f"Unknown task: {task_name}")
        
        pool = self.tasks[task_name]
        return self.env.reset(seed=seed, candidate_pool=pool)

if __name__ == "__main__":
    # Quick verification
    env = ShortlistingEnv()
    tm = TaskManager(env)
    
    print("Testing Easy Task...")
    tm.run_task("easy", seed=123)
    print(f"Pool size: {len(env.all_candidates)}")
    print(f"Initial state: {env.get_state()}")
    
    # Simulate a win in 2 steps for grading test
    env.target = "APPLE" # Force target for testing
    env.candidates = ["APPLE", "BERRY"]
    env.step("APPLE")
    print(f"Grade (Solved in 1): {grade_task(env)}")
