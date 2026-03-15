from collections import Counter

class Validator:
    def __init__(self, dictionary: set):
        self.dictionary = dictionary

    def is_valid(self, word: str, letters: list[str]) -> tuple[bool, str]:
        word = word.strip().upper()
        
        # Chek 1: minumun lenght
        if len(word) < 3:
            return False, "Word must be at least 3 letters long."

        # Check 2: word must be in the dictionary
        if word not in self.dictionary:
            return False, f"'{word}' is not a valid word."

        # Check 3: letter availability (multiset subset check)
        word_count = Counter(word)
        letter_count = Counter(l.upper() for l in letters)

        for char, count in word_count.items():
            if count > letter_count[char] < count:
                return False, f"Not enough '{char}' in your letters."
        
        return True, "Valid word!."
    
    def is_subset(self, word: str, letters: list[str]) -> bool:
        """Quick check without reason — used internally by solver."""
        word_count = Counter(word.upper())
        letter_count = Counter(l.upper() for l in letters)
        return all(word_count[c] <= letter_count[c] for c in word_count)