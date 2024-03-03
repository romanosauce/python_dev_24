import collections
import random
import sys


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
    guess = ""
    attemps = 0
    while guess != secret_word:
        guess = ask("Введите слово: ", words)
        inform("Быки: {}, Коровы: {}", *bullscows(guess, secret_word))
        attemps += 1

    return attemps
