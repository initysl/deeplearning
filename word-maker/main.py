from engine import DictionaryLoader, Validator, Solver, Scorer

def main():
    print("Loading dictionary...")
    loader = DictionaryLoader("dictionary/words.txt")
    print(f"Loaded {len(loader)} words.")

    validator = Validator(loader.words)
    solver = Solver(loader.words)
    scorer = Scorer()

    # --- Test 1: Validate individual words ---
    test_letters = list("STARTLE")
    print(f"Letters: {test_letters}\n")

    for word in ["STAR", "STARE", "RATTLE", "LATEST", "STARTLE", "XYZ", "AT"]:
        valid, reason = validator.is_valid(word, test_letters)
        status = "✓" if valid else "✗"
        print(f"  {status} {word:<10} — {reason}")

    # --- Test 2: Find all valid words ---
    print("\nAll valid words (top 10):")
    all_words = solver.get_all_valid_words(test_letters)
    for word, score in all_words[:10]:
        print(f"  {word:<12} score: {score}")

    # --- Test 3: Best word ---
    best = solver.best_word(test_letters)
    print(f"\nBest word: {best[0]} (score: {best[1]})")

    # --- Test 4: Words grouped by length ---
    print("\nWords by length:")
    by_length = solver.words_by_length(test_letters)
    for length, words in by_length.items():
        print(f"  {length} letters: {', '.join(words[:5])}{'...' if len(words) > 5 else ''}")

if __name__ == "__main__":
    main()