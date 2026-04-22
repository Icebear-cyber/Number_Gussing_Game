# Number Guessing Game
# A fun Python game - guess the randomly generated number!

import random
import time

# ─── Color Codes ──────────────────────────────────────────────────────────────
class Colors:
    RED     = '\033[91m'
    GREEN   = '\033[92m'
    YELLOW  = '\033[93m'
    BLUE    = '\033[94m'
    CYAN    = '\033[96m'
    WHITE   = '\033[97m'
    BOLD    = '\033[1m'
    RESET   = '\033[0m'

def colored(text, color):
    return f"{color}{text}{Colors.RESET}"

# ─── Difficulty Settings ──────────────────────────────────────────────────────
DIFFICULTY = {
    '1': {'name': 'Easy',   'range': (1, 50),   'attempts': 10, 'hint': True},
    '2': {'name': 'Medium', 'range': (1, 100),  'attempts': 7,  'hint': True},
    '3': {'name': 'Hard',   'range': (1, 500),  'attempts': 8,  'hint': False},
    '4': {'name': 'Expert', 'range': (1, 1000), 'attempts': 10, 'hint': False},
}

# ─── Helper Functions ─────────────────────────────────────────────────────────
def print_banner():
    print(colored('=' * 50, Colors.CYAN))
    print(colored('      NUMBER GUESSING GAME      ', Colors.BOLD + Colors.YELLOW))
    print(colored('=' * 50, Colors.CYAN))
    print()

def get_difficulty():
    print(colored('Select Difficulty:', Colors.BOLD + Colors.WHITE))
    for key, val in DIFFICULTY.items():
        r = val['range']
        print(f"  {colored(key, Colors.YELLOW)}. {val['name']:8s}  (1-{r[1]}, {val['attempts']} attempts)")
    print()
    while True:
        choice = input(colored('Your choice (1-4): ', Colors.CYAN)).strip()
        if choice in DIFFICULTY:
            return DIFFICULTY[choice]
        print(colored('Invalid choice. Please enter 1, 2, 3, or 4.', Colors.RED))

def get_guess(low, high):
    while True:
        try:
            guess = int(input(colored(f'  Enter your guess ({low}-{high}): ', Colors.CYAN)))
            if low <= guess <= high:
                return guess
            print(colored(f'  Please enter a number between {low} and {high}.', Colors.RED))
        except ValueError:
            print(colored('  Invalid input. Please enter a whole number.', Colors.RED))

def get_hint(guess, secret, low, high):
    diff = abs(guess - secret)
    total_range = high - low
    if diff == 0:
        return ''
    elif diff <= total_range * 0.05:
        return colored(' (Extremely close!)', Colors.GREEN + Colors.BOLD)
    elif diff <= total_range * 0.15:
        return colored(' (Very warm!)', Colors.GREEN)
    elif diff <= total_range * 0.30:
        return colored(' (Getting warm...)', Colors.YELLOW)
    elif diff <= total_range * 0.50:
        return colored(' (Cold)', Colors.BLUE)
    else:
        return colored(' (Ice cold!)', Colors.CYAN)

def calculate_score(attempts_used, max_attempts, num_range, time_taken):
    base = 1000
    attempt_penalty = (attempts_used - 1) * (base // max_attempts)
    time_penalty = min(int(time_taken * 2), 300)
    range_bonus = num_range // 50
    score = max(0, base - attempt_penalty - time_penalty + range_bonus)
    return score

# ─── Main Game Logic ──────────────────────────────────────────────────────────
def play_game(difficulty):
    low, high = difficulty['range']
    max_attempts = difficulty['attempts']
    hint_enabled = difficulty['hint']
    diff_name = difficulty['name']

    secret = random.randint(low, high)
    print()
    print(colored(f'  Difficulty: {diff_name}  |  Range: {low}-{high}  |  Attempts: {max_attempts}', Colors.WHITE))
    print(colored(f'  I have picked a number between {low} and {high}. Can you guess it?', Colors.BLUE))
    print()

    start_time = time.time()
    guesses = []

    for attempt in range(1, max_attempts + 1):
        remaining = max_attempts - attempt + 1
        print(colored(f'  Attempt {attempt}/{max_attempts}  |  Remaining: {remaining}', Colors.WHITE))

        guess = get_guess(low, high)
        guesses.append(guess)
        time_taken = time.time() - start_time

        if guess == secret:
            print()
            print(colored('  CORRECT! You guessed it!', Colors.GREEN + Colors.BOLD))
            score = calculate_score(attempt, max_attempts, high - low, time_taken)
            print(colored(f'  The number was: {secret}', Colors.YELLOW))
            print(colored(f'  Attempts used: {attempt}/{max_attempts}', Colors.WHITE))
            print(colored(f'  Time taken: {time_taken:.1f}s', Colors.WHITE))
            print(colored(f'  Score: {score} pts', Colors.CYAN + Colors.BOLD))
            return True, attempt, score

        elif guess < secret:
            direction = colored('TOO LOW  ^', Colors.RED + Colors.BOLD)
        else:
            direction = colored('TOO HIGH v', Colors.RED + Colors.BOLD)

        hint = get_hint(guess, secret, low, high) if hint_enabled else ''
        print(colored(f'  {direction}{hint}', Colors.WHITE))
        print()

    # Failed
    print()
    print(colored(f'  GAME OVER! You used all {max_attempts} attempts.', Colors.RED + Colors.BOLD))
    print(colored(f'  The number was: {secret}', Colors.YELLOW))
    print(colored(f'  Your guesses: {guesses}', Colors.WHITE))
    return False, max_attempts, 0

# ─── High Score Tracker ───────────────────────────────────────────────────────
class HighScoreTracker:
    def __init__(self):
        self.scores = []

    def add(self, name, score, difficulty, attempts):
        self.scores.append({'name': name, 'score': score, 'difficulty': difficulty, 'attempts': attempts})
        self.scores.sort(key=lambda x: x['score'], reverse=True)

    def display(self):
        if not self.scores:
            print(colored('  No scores yet!', Colors.WHITE))
            return
        print(colored('\n  LEADERBOARD:', Colors.BOLD + Colors.YELLOW))
        print(colored('  ' + '-' * 40, Colors.CYAN))
        for i, entry in enumerate(self.scores[:5], 1):
            print(f"  {colored(str(i), Colors.YELLOW)}.  {entry['name']:12s}  {colored(str(entry['score']) + ' pts', Colors.GREEN):15s}  {entry['difficulty']}  ({entry['attempts']} attempts)")
        print()

# ─── Entry Point ─────────────────────────────────────────────────────────────
def main():
    print_banner()
    tracker = HighScoreTracker()
    wins = 0
    losses = 0

    while True:
        difficulty = get_difficulty()
        won, attempts, score = play_game(difficulty)

        if won:
            wins += 1
            name = input(colored('\n  Enter your name for the leaderboard: ', Colors.CYAN)).strip() or 'Player'
            tracker.add(name, score, difficulty['name'], attempts)
            tracker.display()
        else:
            losses += 1

        print(colored(f'\n  Session Stats: {wins} wins / {losses} losses', Colors.WHITE))
        print()
        again = input(colored('  Play again? (y/n): ', Colors.CYAN)).strip().lower()
        if again != 'y':
            print()
            print(colored('  Thanks for playing! Final Stats:', Colors.BOLD + Colors.YELLOW))
            print(colored(f'  Wins: {wins}  |  Losses: {losses}', Colors.WHITE))
            tracker.display()
            print(colored('  Goodbye!', Colors.CYAN))
            break
        print()
        print_banner()

if __name__ == '__main__':
    main()
