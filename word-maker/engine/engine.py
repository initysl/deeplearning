class DictionaryLoader:
    def __int__(self, path: str, min_len: int =3, max_len: int = 9):
        self.path = path
        self.min_len = min_len
        self.max_len = max_len
        self.words = self.load_dictionary()
    
    def load_dictionary(self) -> set:
        with open(self.path, "r") as file:
            return set(
                words.strip().upper()
                for words in file
                if self.min_len <= len(words.strip()) <= self.max_len
                and words.strip().isalpha() # excluse hyphenated, apostrophes, etc.
            )
    
    def __len__(self):
        return len(self.words)
    
    def __contains__(self, word: str):
        return word.upper() in self.words
