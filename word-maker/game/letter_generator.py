# game/letter_generator.py

import random
from collections import Counter

class LetterGenerator:
    # Frequency-weighted English letter distribution
    LETTER_WEIGHTS = {
        'A': 8, 'B': 2, 'C': 3, 'D': 4, 'E': 12, 'F': 2, 'G': 3,
        'H': 3, 'I': 7, 'J': 1, 'K': 2, 'L': 5, 'M': 3, 'N': 7,
        'O': 8, 'P': 2, 'Q': 1, 'R': 6, 'S': 6, 'T': 7, 'U': 4,
        'V': 1, 'W': 2, 'X': 1, 'Y': 2, 'Z': 1
    }
    VOWELS     = set("AEIOU")
    CONSONANTS = set("BCDFGHJKLMNPQRSTVWXYZ")

    def generate(self, n: int = 7, min_vowels: int = 2, max_vowels: int = 4) -> list[str]:
        """
        Generates a balanced letter set with guaranteed vowel count.
        Retries until the vowel constraint is satisfied.
        """
        letters_pool  = list(self.LETTER_WEIGHTS.keys())
        weights_pool  = list(self.LETTER_WEIGHTS.values())

        while True:
            letters = random.choices(letters_pool, weights=weights_pool, k=n)
            vowel_count = sum(1 for l in letters if l in self.VOWELS)
            if min_vowels <= vowel_count <= max_vowels:
                return letters

    def generate_by_difficulty(self, difficulty: str = "medium") -> list[str]:
        """
        Wraps generate() with difficulty presets.
        Easy   → more vowels, common letters
        Medium → balanced
        Hard   → fewer vowels, rare letters possible
        """
        presets = {
            "easy":   {"n": 7, "min_vowels": 3, "max_vowels": 4},
            "medium": {"n": 7, "min_vowels": 2, "max_vowels": 3},
            "hard":   {"n": 7, "min_vowels": 2, "max_vowels": 2},
        }
        params = presets.get(difficulty, presets["medium"])
        return self.generate(**params)