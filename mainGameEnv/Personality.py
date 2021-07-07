import random
from sys import stdin


class Personality:

    def __init__(self):
        pass

    def make_choice(self, options):
        pass


class StupidAI(Personality):
    def __init__(self):
        pass

    def make_choice(self, options):
        #return random.choice(range(len(options)))
        return len(options)-1

class Human(Personality):
    def __init__(self):
        pass

    def make_choice(self, options):
        return int(stdin.readline())

