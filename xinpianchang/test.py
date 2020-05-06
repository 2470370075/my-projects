import timeit
import random


def generate(num):
    while num:
        yield random.randrange(10)
        num -= 1


def create_list(num):
    numbers = []
    while num:
        numbers.append(random.randrange(10))
        num -= 1
    return numbers

import datetime
a = datetime.datetime.now()
x = generate(9999990)
print(sum(x))
b = datetime.datetime.now()
print(b-a)

a = datetime.datetime.now()
y = create_list(9999990)
print(sum(y))
b = datetime.datetime.now()
print(b-a)