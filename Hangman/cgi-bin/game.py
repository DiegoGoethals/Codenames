import string
import random
import re


class Game:

    def __init__(self, word):
        # Sets word chosen by players as word to guess
        self.word = word

        # Shows how many letters have to be guessed by players and are already guessed
        self.progress = "."*len(self.word)

        # Generates a random code so other players can actually join the game to try and guess the word
        self.code = ''.join(random.choice(string.ascii_letters) for _ in range(8))

        # Initializes how many mistakes can be made and will diminish every time someone guesses wrong
        self.mistakes_left = 10

        # Initializes the collection of already guessed letters, right and wrong
        self.selected = []

        # Obviously creates an empty winner slot
        self.winner = None

    # Enables the players to guess a letter
    def guess(self, letter):
        if letter in self.selected:
            return False
        self.selected.append(letter)
        if letter not in self.word:
            self.mistakes_left -= 1
        else:
            matches = []
            for match in re.finditer(letter, self.word):
                matches.append(match.start())
            for match in matches:
                self.progress = self.progress[:match] + letter + self.progress[match + 1:]
        self.check_win()

    # Checks if the game is done and if so who won, the hanger or the guessers
    def check_win(self):
        if self.mistakes_left == 0:
            self.winner = "Hanger"
        if self.progress == self.word:
            self.winner = "Guesser"
