import random
import string


class Game:

    # Initializes the game
    def __init__(self, words):
        # Puts all words from a file into an array so you can use them to set up the board
        input = open(words, 'r')
        dictionary = []
        line = input.readline()
        while line:
            dictionary.append(line.strip("\n"))
            line = input.readline()
        input.close()

        # Determines which team will start the game and get 9 cards
        self.current_player = random.choice(['red', 'blue'])

        # Sets cards to their respective colors
        self.red_team = set()
        self.blue_team = set()
        self.neutral = set()
        if self.current_player == 'red':
            while len(self.red_team) != 9:
                self.red_team.add(random.choice(dictionary))
            while len(self.blue_team) != 8:
                word = random.choice(dictionary)
                if word not in self.red_team:
                    self.blue_team.add(word)
        else:
            while len(self.blue_team) != 9:
                self.blue_team.add(random.choice(dictionary))
            while len(self.red_team) != 8:
                word = random.choice(dictionary)
                if word not in self.blue_team:
                    self.red_team.add(word)
        while len(self.neutral) != 7:
            word = random.choice(dictionary)
            if word not in self.red_team and word not in self.blue_team:
                self.neutral.add(word)

        # Sets forbidden word
        self.assassin = ""
        while len(self.assassin) == 0:
            word = random.choice(dictionary)
            if word not in self.red_team and word not in self.blue_team and word not in self.neutral:
                self.assassin = word

        # Creates a list to put all selected words in
        self.selected = []

        # Sets winner to None until another function sets a winner if a certain criteria is met
        self.winner = None

        # Generates a code to join the game
        letters = string.ascii_letters
        self.code = ''.join(random.choice(letters) for _ in range(8))

        # Makes list out of teams so they can be send as JSON objects
        self.red_team = list(self.red_team)
        self.blue_team = list(self.blue_team)
        self.neutral = list(self.neutral)

        # Creates a list of all words, regardless of color
        self.words = list(self.red_team) + list(self.blue_team) + list(self.neutral) + [self.assassin]
        random.shuffle(self.words)

    # Gives current state of the game
    def current_state(self):
        return self.__dict__

    # Let's current team make a move
    def move(self, word):
        self.selected.append(word)
        if word == self.assassin:
            if self.current_player == "red":
                self.winner = "blue"
            else:
                self.winner = "red"
        elif set(self.red_team).issubset(self.selected):
            self.winner = 'red'
        elif set(self.blue_team).issubset(self.selected):
            self.winner = 'blue'
        else:
            if word in self.neutral:
                self.end_turn()
            elif self.current_player == "red" and word in self.blue_team:
                self.end_turn()
            elif self.current_player == "blue" and word in self.red_team:
                self.end_turn()

    # Ends turn if current team selects a wrong word or if they selected maximum allowed words
    def end_turn(self):
        if self.current_player == "red":
            self.current_player = "blue"
        else:
            self.current_player = "red"
