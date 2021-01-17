from time import time
from random import randint as r


class ArithmeticGame:
    def __init__(self, player, limit_time=6, lower_bound=0, upper_bound=10000):
        self.player = player
        self.time = time()
        self.limit = int(limit_time)
        self.lower_bound = int(lower_bound)
        self.upper_bound = int(upper_bound)
        self.num1 = r(self.lower_bound, self.upper_bound)
        self.num2 = r(self.lower_bound, self.upper_bound)
        self.res = self.num1 + self.num2

    def valid_time(self):
        return (time() - self.time) < self.limit

    def valid_num(self, num):
        return int(num) == self.res

    def give_question(self):
        return f"```What\'s {self.num1} + {self.num2} = ?```"