import threading
from engine import DictionaryLoader, Validator, Solver, Scorer
from game import LetterGenerator, GameSession, Display

def run_game(difficulty: str = "medium", time_limit: int = 90):
    # --- Boot ---
    Display.clear()
    Display.banner()
    print("  Loading dictionary...")
    loader    = DictionaryLoader("dictionary/words.txt")
    validator = Validator(loader.words)
    solver    = Solver(loader.words)
    scorer    = Scorer()
    gen       = LetterGenerator()
    print(f"  Ready. ({len(loader)} words loaded)\n")

    # --- Difficulty select ---
    print("  Difficulty: (1) Easy  (2) Medium  (3) Hard")
    choice = input("  Choose [default=2]: ").strip()
    diff_map = {"1": "easy", "2": "medium", "3": "hard"}
    difficulty = diff_map.get(choice, "medium")

    # --- Generate letters and session ---
    letters = gen.generate_by_difficulty(difficulty)
    session = GameSession(letters, validator, solver, scorer, time_limit=time_limit)

    # --- Timer thread ---
    stop_event = threading.Event()

    def timer_thread():
        while not stop_event.is_set():
            if session.is_time_up():
                print(cls._c("\n\n  ⏰  Time's up!\n", "red"))  
                stop_event.set()
                break
            import time; time.sleep(1)

    # --- Main game loop ---
    Display.clear()
    Display.banner()
    session.start()
    t = threading.Thread(target=timer_thread, daemon=True)
    t.start()

    print(f"  Difficulty : {difficulty.upper()}")
    print(f"  Time Limit : {time_limit}s")
    print("  Type a word and press ENTER. Type 'quit' to end early.\n")

    while not session.is_time_up():
        Display.show_letters(session.letters)
        Display.show_status(session)
        Display.show_found_words(session)

        try:
            word = input("  Your word: ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if word.lower() == "quit":
            break
        if word.lower() == "hint":
            missed = session.missed_words()
            if missed:
                # Reveal first letter of the best missed word as a hint
                best_missed = missed[0][0]
                print(f"\n  Hint: Try a {len(best_missed)}-letter word starting with '{best_missed[0]}'...\n")
            continue

        result = session.submit_word(word)
        Display.show_result(result)
        import time; time.sleep(0.8)
        Display.clear()
        Display.banner()

    # --- End ---
    stop_event.set()
    session.end()
    Display.show_summary(session.summary())

if __name__ == "__main__":
    run_game()