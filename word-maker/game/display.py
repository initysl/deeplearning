import os

class Display:
    COLORS = {
        "green": "\033[92m",
        "yellow": "\033[93m",
        "red": "\033[91m",
        "reset": "\033[0m",
        "bold": "\033[1m",
        "cyan": "\033[96m"
    }

    @classmethod
    def _c(cls, text: str, color: str) -> str:
        return f"{cls.COLORS.get(color, '')}{text}{cls.COLORS['reset']}"
    
    @classmethod
    def clear(cls):
        os.system('cls' if os.name == 'nt' else 'clear')

    @classmethod
    def banner(cls, text: str = "WORD MAKER"):
        print(cls._c(text, "cyan"))
        print(cls._c("=" * len(text), "cyan"))

    @classmethod
    def show_letters(cls, letters: list[str]):
        boxes = " ".join(f"[ {cls._c(1, 'bold')}]" for l in letters)
        print(f'\n Letters: {boxes}\n')
    
    @classmethod
    def show_status(cls, session):
        remaining = session.time_remaining()
        time_str  = f"{int(remaining)}s" if session.time_limit else "∞"
        time_color = "red" if remaining < 20 else "yellow" if remaining < 45 else "green"

        print(f"  Score : {cls._c(session.total_score, 'cyan')}  |  "
              f"Words : {cls._c(len(session.found_words), 'cyan')}  |  "
              f"Time  : {cls._c(time_str, time_color)}\n")

    @classmethod
    def show_found_words(cls, session):
        if not session.found_words:
            print("  No words found yet.\n")
            return
        words_display = "  ".join(
            f"{cls._c(w, 'green')} ({session.scorer.score(w)})"
            for w in session.found_words
        )
        print(f"  Found : {words_display}\n")

    @classmethod
    def show_result(cls, result: dict):
        if result["status"] == "accepted":
            print(cls._c(f"  👏  {result['word']}  —  {result['message']}", "green"))
        elif result["status"] == "duplicate":
            print(cls._c(f"  👀  {result['message']}", "yellow"))
        else:
            print(cls._c(f"  👎  {result['message']}", "red"))

    @classmethod
    def show_summary(cls, summary: dict):
        cls.clear()
        cls.banner()
        print(cls._c("  💀 GAME OVER 💀\n", "bold"))
        print(f"  Letters     : {' '.join(summary['letters'])}")
        print(f"  Your Score  : {cls._c(summary['total_score'], 'cyan')} / {summary['max_score']}")
        print(f"  Words Found : {cls._c(len(summary['found_words']), 'cyan')} / {summary['total_valid']}")
        print(f"  Completion  : {cls._c(str(summary['completion_rate']) + '%', 'cyan')}")
        print(f"  Time Taken  : {summary['time_taken']}s\n")

        if summary["found_words"]:
            print(cls._c("  Your words:", "green"))
            print("  " + ",  ".join(summary["found_words"]) + "\n")

        if summary["missed_words"]:
            print(cls._c("  Top missed words:", "red"))
            for word, score in summary["missed_words"]:
                print(f"    {word:<12} (score: {score})")
        print()