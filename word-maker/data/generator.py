# Raw sample
import json
import random
from collections import Counter
from engine.solver import Solver
from engine.scorer import Scorer
from game.letter_generator import LetterGenerator

class DataGenerator:
    def __init__(self, solver: Solver, scorer: Scorer):
        self.solver = solver
        self.scorer = scorer
        self.gen = LetterGenerator()
    
    def build_sample(self, letters: list[str]) -> dict | None:
        """
        Builds a single training sample from a letter set.
        Returns None if the letter set yields no valid words.
        """
        valid_words = self.solver.get_all_valid_words(letters)
        if not valid_words:
            return None
        
        # Separate words and scores
        words  = [w for w, _ in valid_words]
        scores = [s for _, s in valid_words]

        length_dist = Counter(len(w) for w in words)

        return {
            # --- Input to the model ---
            "input": "letters: " + " ".join(letters),

            # --- Target output: top 10 words ranked by score ---
            "target": ", ".join(words[:10]),

            # --- Metadata (not used in training, used in analysis) ---
            "meta": {
                "letters":        letters,
                "total_words":    len(words),
                "max_score":      sum(scores),
                "best_word":      words[0] if words else None,
                "best_score":     scores[0] if scores else 0,
                "length_dist":    dict(length_dist),
                "difficulty":     self._estimate_difficulty(len(words), length_dist),
            }
        }
    
    def _estimate_difficulty(self, total_words: int, length_dist: Counter) -> str:
        """
        Heuristic to estimate difficulty based on number of valid words and their length distribution.
        """
        long_words = sum(v for k, v in length_dist.items() if k >= 6)

        if total_words >=30 and long_words >= 3:
            return "easy"
        elif total_words >= 15 :
            return "medium"
        else:
            return "hard"
        
    def generate_batch(
        self,
        n_samples: int       = 50_000,
        difficulties: list   = ["easy", "medium", "hard"],
        log_every: int       = 1_000,
    ) -> list[dict]:
        """
        Generates a batch of training samples.
        """
        samples = []
        attempts = 0
        diff_cycle = difficulties * (n_samples // len(difficulties) + 1)  # Cycle through difficulties
        random.shuffle(diff_cycle)

        print(f"Generating {n_samples} samples ....")

        while len(samples) < n_samples:
            difficulties = diff_cycle[attempts % len(diff_cycle)]
            letters = self.gen.generate_by_difficulty(difficulties)
            sample = self.build_sample(letters)
            attempts += 1

            if sample is None:
                continue

            samples.append(sample)

            if len(samples) % log_every == 0:
                print(f"    {len(samples):>6,} / {n_samples:,}  "
                      f"(attempts: {attempts:,}, "
                      f"yield rate: {len(samples)/attempts*100:.1f}%)")

        print(f"  Done. {len(samples):,} samples in {attempts:,} attempts.\n")
        return samples