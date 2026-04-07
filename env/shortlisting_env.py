import random
import os

GREEN, AMBER, BLACK = "G", "Y", "R"
WIN = "GGGGG"

def get_feedback(secret: str, guess: str) -> str:
    """Returns Wordle-style feedback for a guess given a secret word."""
    feedback = [BLACK] * 5
    secret_list = list(secret)
    guess_list = list(guess)

    # First pass: Find Greens
    for i in range(5):
        if guess_list[i] == secret_list[i]:
            feedback[i] = GREEN
            secret_list[i] = None  # Mark as used
            guess_list[i] = None

    # Second pass: Find Ambers
    for i in range(5):
        if guess_list[i] is not None and guess_list[i] in secret_list:
            feedback[i] = AMBER
            secret_list[secret_list.index(guess_list[i])] = None

    return "".join(feedback)

class ShortlistingEnv:
    def __init__(self, words_file: str = "wordlebot_inspiration/five_letter_words.txt", max_attempts: int = 6):
        if not os.path.exists(words_file):
            raise FileNotFoundError(f"Candidate file not found: {words_file}")
            
        with open(words_file) as f:
            self.original_candidates = [line.strip().upper() for line in f]
        
        self.max_attempts = max_attempts
        self.all_candidates = list(self.original_candidates)
        self.reset()

    def reset(self, seed: int = None, candidate_pool: list = None):
        """Randomly select a target candidate and initialize the environment state."""
        if seed is not None:
            random.seed(seed)
        
        if candidate_pool is not None:
            self.all_candidates = [c.upper() for c in candidate_pool]
        else:
            self.all_candidates = list(self.original_candidates)
            
        self.target = random.choice(self.all_candidates)
        self.candidates = list(self.all_candidates)
        self.initial_count = len(self.candidates)
        self.prev_candidate_count = self.initial_count
        
        self.history = []  # List of (guess, feedback) tuples
        self.attempts = 0
        self.last_feedback = ""
        self.done = False
        self.solved = False
        self.solved_in = None
        
        return self.get_state()

    def step(self, action: str):
        """
        Treat action as a selected candidate (string).
        Compare it with the target, generate feedback, filter pool, and return (state, reward, done, info).
        """
        if self.done:
            return self.get_state(), 0.0, True, {"message": "Episode already finished"}

        guess = action.upper()
        self.attempts += 1
        self.last_feedback = get_feedback(self.target, guess)
        self.history.append((guess, self.last_feedback))
        
        # Filter the candidate pool based on feedback (dropImpossibles)
        self._drop_impossibles(guess, self.last_feedback)
        curr_count = len(self.candidates)
        
        # Reward logic
        prev_count = self.prev_candidate_count
        reduction = (prev_count - curr_count) / prev_count if prev_count > 0 else 0
        
        done = False
        reward = 0.0
        
        if guess == self.target:
            reward = 1.0
            done = True
            self.solved = True
            self.solved_in = self.attempts
        elif self.attempts >= self.max_attempts:
            reward = 0.0
            done = True
        else:
            reward = reduction
            
        self.done = done
        self.prev_candidate_count = curr_count
        
        # Fallback if candidates pool becomes empty unexpectedly
        if not self.candidates and not self.done:
            self.done = True
            reward = 0.0 
            
        info = {
            "success": self.solved,
            "target": self.target if self.done else None
        }
        
        return self.get_state(), reward, self.done, info

    def get_state(self):
        """Returns current observation: remaining count, last feedback, attempt number, and candidate ratio."""
        return {
            "remaining_candidates": len(self.candidates),
            "last_feedback": self.last_feedback,
            "attempts": self.attempts,
            "candidate_ratio": len(self.candidates) / self.initial_count if self.initial_count > 0 else 0
        }

    def _drop_impossibles(self, guess: str, feedback: str):
        """Filters the candidate list based on the last guess and feedback."""
        self.candidates = [
            word for word in self.candidates 
            if get_feedback(word, guess) == feedback
        ]

if __name__ == '__main__':
    # Simple test run to verify improvements
    env = ShortlistingEnv()
    state = env.reset()
    print(f"Initial State: {state}")
    
    # Simulate a step with a random guess
    test_guess = random.choice(env.all_candidates)
    state, reward, done, info = env.step(test_guess)
    print(f"Guess: {test_guess} (Target: {env.target})")
    print(f"New State: {state}")
    print(f"Reward: {reward:.4f}, Done: {done}, Info: {info}")
