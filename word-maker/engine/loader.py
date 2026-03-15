class DictionaryLoader:
    def __init__(self, path: str, min_len: int = 3, max_len: int = 9):
        self.path = path
        self.min_len = min_len
        self.max_len = max_len
        self.words = self._load()

    def _load(self) -> set:
        with open(self.path, "r") as f:
            return set(
                word.strip().upper()
                for word in f
                if self.min_len <= len(word.strip()) <= self.max_len
                and word.strip().isalpha()        # exclude hyphenated, apostrophe words
            )

    def __len__(self):
        return len(self.words)

    def __contains__(self, word: str):
        return word.upper() in self.words