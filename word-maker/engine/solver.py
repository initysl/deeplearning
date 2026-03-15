from collections import Counter
from engine.scorer import Scorer

class Solver:
    def __init__(self, dictionary: set):
        self.dictionary = dictionary
        self.scorer = Scorer()

    def get_all_valid_words(self, letters: list[str]) -> list[tuple[str, int]]:
        """
        Scans full dictionary and returns all valid words
        as (word, score) pairs, sorted highest score first.
        """
        letter_count = Counter(l.upper() for l in letters)

        valid = []
        for word in self.dictionary:
            word_count = Counter(word)
            if all(word_count[c] <= letter_count[c] for c in word_count):
                valid.append(word)

        return self.scorer.rank(valid)

    def best_word(self, letters: list[str]) -> tuple[str, int] | None:
        """Returns the single highest scoring valid word."""
        results = self.get_all_valid_words(letters)
        return results[0] if results else None

    def words_by_length(self, letters: list[str]) -> dict[int, list[str]]:
        """Groups valid words by their length — useful for hint bucketing."""
        all_words = self.get_all_valid_words(letters)
        grouped = {}
        for word, score in all_words:
            grouped.setdefault(len(word), []).append(word)
        return dict(sorted(grouped.items(), reverse=True))