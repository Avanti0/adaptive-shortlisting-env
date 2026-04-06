import random

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

class WordleBot:
    instructions = """The computer will guess the word using local game engine."""

    def __init__(self, name: str = "ImprovedBot", seed: int = None):
        try:
            with open("five_letter_words.txt") as f:
                self.all_words = [line.strip().upper() for line in f]
        except FileNotFoundError:
            print("Error: five_letter_words.txt not found.")
            raise SystemExit()
        
        self.name = name
        if seed is not None:
            random.seed(seed)
        self.reset()

    def reset(self, seed: int = None):
        """Resets the game state for a new round."""
        if seed is not None:
            random.seed(seed)
        
        self.secret_word = random.choice(self.all_words)
        self.words = list(self.all_words)
        self.tries = 0
        self.allowed = 6
        self.status = "PLAY"
        # Start with a random word from the list
        self.guess = random.choice(self.words)
        self.response = ""
        return self.get_observation()

    def get_observation(self):
        """Returns the current state of the game."""
        return {
            "tries": self.tries,
            "possible_words_count": len(self.words),
            "status": self.status,
            "last_feedback": self.response
        }

    def step(self, guess: str):
        """Perform a single guess step, returning (obs, reward, done, info)."""
        if self.status != "PLAY":
            return self.get_observation(), 0, True, {"message": "Game already over"}

        self.tries += 1
        self.guess = guess.upper()
        self.response = get_feedback(self.secret_word, self.guess)
        
        done = False
        reward = 0

        if self.response == WIN:
            self.status = "WON"
            reward = 10
            done = True
        elif self.tries >= self.allowed:
            self.status = "EXCEEDED"
            reward = -10
            done = True
        
        self.drop_impossibles()
        
        if not self.words and self.status == "PLAY":
            self.status = "FAILED"
            done = True

        return self.get_observation(), reward, done, {"secret": self.secret_word if done else None}

    def drop_impossibles(self):
        """Filters the word list based on the last guess and feedback."""
        new_words = []
        for word in self.words:
            if get_feedback(word, self.guess) == self.response:
                new_words.append(word)
        self.words = new_words

    def get_next_guess(self):
        """Suggests the next guess based on letter frequency in remaining words."""
        if not self.words:
            return None
        if len(self.words) == 1:
            return self.words[0]
        
        # Simple frequency heuristic
        letter_freqs = {}
        for word in self.words:
            for char in set(word): # Distinct letters only for information gain
                letter_freqs[char] = letter_freqs.get(char, 0) + 1
        
        return max(self.words, key=lambda w: sum(letter_freqs.get(c, 0) for c in set(w)))

    def play(self):
        """Plays a single guess and prints output (for CLI use)."""
        current_guess = self.guess
        print(f"-- Attempt {self.tries + 1} --")
        print(f"Guess    : {current_guess}")
        
        obs, reward, done, info = self.step(current_guess)
        print(f"Feedback : {self.response}")
        
        if self.status == "WON":
            print("\nYay! The bot solved the Wordle!")
        elif self.status == "EXCEEDED":
            print(f"OOPS. Answer was {info['secret']}")
        elif self.status == "FAILED":
            print("I have no more words to guess. Something went wrong.")
        else:
            print(f"{len(self.words)} possible words remaining.\n")
            self.guess = self.get_next_guess()

    def game(self):
        """Runs the full game loop."""
        print(f"Bot '{self.name}' starting game...")
        while self.status == "PLAY":
            self.play()

if __name__ == '__main__':
    bot = WordleBot(name="LocalImprovedBot")
    bot.game()
