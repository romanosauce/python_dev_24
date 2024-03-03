import collections


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
