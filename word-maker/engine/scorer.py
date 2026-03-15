class Scorer:
    # Standard Scrabble-inspired length scoring
    SCORE_TABLE = {
        3: 1,
        4: 2,
        5: 4,
        6: 8,
        7: 15,
        8: 25,
        9: 40,
    }

    # Rare letter bonus
    RARE_LETTERS = {'Q': 5, 'Z': 5, 'X': 4, 'J': 4, 'K': 3, 'V': 2}

    def score(self, word: str) -> int:
        word = word.upper()
        base = self.SCORE_TABLE.get(len(word), 50)  # 50 for 10+ letter words
        bonus = sum(self.RARE_LETTERS.get(c, 0) for c in word)
        return base + bonus
    
    def rank(self, words: list[str]) -> list[tuple[str, int]]:
        """Returns list of (word, score) sorted highest first."""
        scored = [(word, self.score(word)) for word in words]
        return sorted(scored, key=lambda x: x[1], reverse=True)