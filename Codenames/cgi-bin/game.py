import random
import string


class Game:

    # Initializes the game
    def __init__(self, woorden):
        # Puts all words in a file so you can use them to set up the board
        invoer = open(woorden, 'r')
        woordenboek = []
        regel = invoer.readline()
        while regel:
            woordenboek.append(regel.strip("\n"))
            regel = invoer.readline()
        invoer.close()

        # Determines which team will start the game and get 9 cards
        self.current_player = random.choice(['red', 'blue'])

        # Sets cards to their respective colors
        self.red_team = set()
        self.blue_team = set()
        self.neutral = set()
        if self.current_player == 'red':
            while len(self.red_team) != 9:
                self.red_team.add(random.choice(woordenboek))
            while len(self.blue_team) != 8:
                woord = random.choice(woordenboek)
                if woord not in self.red_team:
                    self.blue_team.add(woord)
        else:
            while len(self.blue_team) != 9:
                self.blue_team.add(random.choice(woordenboek))
            while len(self.red_team) != 8:
                woord = random.choice(woordenboek)
                if woord not in self.blue_team:
                    self.red_team.add(woord)
        while len(self.neutral) != 7:
            woord = random.choice(woordenboek)
            if woord not in self.red_team and woord not in self.blue_team:
                self.neutral.add(woord)

        # Sets forbidden word
        self.assassin = ""
        while len(self.assassin) == 0:
            woord = random.choice(woordenboek)
            if woord not in self.red_team and woord not in self.blue_team and woord not in self.neutral:
                self.assassin = woord

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
