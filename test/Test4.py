import random
from sympy.strategies.core import switch

def fibonacciNumber():
    # returns 6 numbers between 1 and 40
    a = 0
    b = 1
    c = 1
    yield a
    yield b
    for i in range(100):
        a = b
        b = c
        c = a + b
        yield c
        

for fib in fibonacciNumber():
       print("And the next number is... %d!" %(fib))