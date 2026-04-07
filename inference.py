import random
from env.shortlisting_env import ShortlistingEnv
from env.tasks import TaskManager, grade_task

def run_agent(task_manager, task_name, seed=None):
    """
    Runs a baseline agent for a specific task and prints logs in the required format.
    """
    env = task_manager.env
    state = task_manager.run_task(task_name, seed=seed)
    
    print(f"[START]")
    print(f"task: {task_name}")
    
    done = False
    while not done:
        # Simple Baseline Agent: Pick a random candidate from the current filtered pool
        # This is a strong baseline because the environment already does the filtering
        # in its step() function, so picking any word from the current pool is valid.
        if env.candidates:
            action = random.choice(env.candidates)
        else:
            # Fallback if somehow the pool is empty
            action = random.choice(env.all_candidates)
            
        state, reward, done, info = env.step(action)
        
        print(f"[STEP]")
        print(f"action: {action}")
        print(f"reward: {reward:.4f}")
        print(f"done: {str(done).lower()}")
        
    final_score = grade_task(env)
    print(f"[END]")
    print(f"score: {final_score:.2f}")
    print("-" * 20)

if __name__ == "__main__":
    # Initialize Environment and Task Manager
    env = ShortlistingEnv()
    tm = TaskManager(env)
    
    # Run all tasks with a fixed seed for reproducibility
    tasks_to_run = ["easy", "medium", "hard"]
    global_seed = 42
    
    for task in tasks_to_run:
        # Increment seed for each task to ensure different targets but deterministic runs
        run_agent(tm, task, seed=global_seed)
        global_seed += 1
