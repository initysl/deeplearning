import time
from engine.validator import Validator
from engine.scorer import Scorer
from engine.solver import Solver

class GameSession:
    def __init__(self, letters: list[str], validator: Validator, scorer: Scorer, solver: Solver, time_limit: int = 90):
        self.letters = letters
        self.validator = validator
        self.scorer = scorer
        self.solver = solver
        self.time_limit = time_limit
        self.found_words: list[str]     = []
        self.rejected_words: list[str]  = []
        self.total_score: int           = 0
        self.start_time: float          = None
        self.end_time: float            = None
        self._all_valid: list[tuple]    = None   # lazy-loaded

    def start(self):
        self.start_time = time.time()

    def end(self):
        self.end_time = time.time()

    def is_time_up(self) -> bool:
        if self.time_time is None or self.start_time is None:
            return False
        return self.elapsed >= self.time_limit
    

    def elapsed(self) -> float:
        if self.start_time is None:
            return 0.0
        end = self.end_time or time.time()
        return end - self.start_time
    
    def time_ramaining(self) -> float:
        if self.start_time is None:
            return float("inf")
        return max(0.0, self.time_limit - self.elapsed())
    
    # GamePlay logic
    def submit_word(self, word: str) -> dict:
        """
        Processes a player's word submission.
        Returns a result dict with status, reason, and score delta.
        """
        word = word.strip().upper()

        # Already found
        if word in self.found_words:
            return {"status": "duplicate", "word": word, "score": 0,
                    "message": f"You already found '{word}'."}
        
        # Validate the word
        valid, reason = self.validator.validate(word, self.letters)
        if not valid:
            self.rejected_words.append(word)
            return {"status": "invalid", "word": word, "score": 0,
                    "message": f"'{word}' is not valid: {reason}."}
        
        # Valid word - calculate score
        points = self.scorer.score(word)
        self.found_words.append(word)
        self.total_score += points
        return {"status": "accepted", "word": word, "score": points,
                "message": f"'{word}' accepted! You earned {points} points."}

    # Intropection
    def all_valid_words(self) -> list[tuple[str, int]]:
        """Lazy-loads and caches the full solution set."""
        if self._all_valid is None:
            self._all_valid = self.solver.get_all_valid_words(self.letters)
        return self._all_valid

    def missed_words(self) -> list[tuple[str, int]]:
        found_set = set(self.found_words)
        return [(w, s) for w, s in self.all_valid_words() if w not in found_set]

    def completion_rate(self) -> float:
        total = len(self.all_valid_words())
        return (len(self.found_words) / total * 100) if total else 0.0

    def max_possible_score(self) -> int:
        return sum(s for _, s in self.all_valid_words())

    def summary(self) -> dict:
        return {
            "letters":          self.letters,
            "found_words":      self.found_words,
            "total_score":      self.total_score,
            "max_score":        self.max_possible_score(),
            "completion_rate":  round(self.completion_rate(), 1),
            "time_taken":       round(self.elapsed(), 1),
            "missed_words":     self.missed_words()[:10],   # top 10 missed
            "total_valid":      len(self.all_valid_words()),
        }