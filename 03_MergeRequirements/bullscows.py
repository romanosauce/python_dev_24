import collections
import random
import sys
import urllib.request
import cowsay


word_len = 5


def bullscows(guess: str, secret: str) -> (int, int):
    bulls = cows = 0
    letters = collections.Counter(secret)
    for i in range(len(guess)):
        if guess[i] == secret[i]:
            bulls += 1
            letters[guess[i]] -= 1
    for i in range(len(guess)):
        if guess[i] != secret[i] and guess[i] in letters \
                and letters[guess[i]] != 0:
            cows += 1
            letters[guess[i]] -= 1

    return (bulls, cows)


def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    valid_words = list(filter(lambda x: len(x) == word_len, words))
    if not valid_words:
        print("Can't find suitable words to choose")
        sys.exit(1)
    secret_word = random.choice(valid_words)
    print("Secret:", secret_word)
    guess = ""
    attempts = 0
    while guess != secret_word:
        guess = ask("Введите слово: ", words)
        inform("Быки: {}, Коровы: {}", *bullscows(guess, secret_word))
        attempts += 1

    return attempts


def ask(prompt: str, valid: list[str] = None) -> str:
    print(cowsay.cowsay(prompt, cow=random.choice(cowsay.list_cows())))
    guess = input()
    if valid:
        while guess not in valid:
            print(cowsay.cowsay("Invalid guess, try again",
                                cow=random.choice(cowsay.list_cows())))
            guess = input()
    return guess


def inform(format_string: str, bulls: int, cows: int) -> None:
    print(cowsay.cowsay(format_string.format(bulls, cows),
                        cow=random.choice(cowsay.list_cows())))


if __name__ == "__main__":
    if len(sys.argv) == 3:
        word_len = int(sys.argv[2])
    if len(sys.argv) not in [2, 3]:
        print("usage: python -m bullscows <dict_path> <word_len>")
    dict_path = sys.argv[1]
    try:
        with urllib.request.urlopen(dict_path) as f:
            word_list = f.read().decode().split()
    except Exception:
        with open(dict_path) as f:
            word_list = f.read().split()
    print("Total attempts:", gameplay(ask, inform, word_list))
