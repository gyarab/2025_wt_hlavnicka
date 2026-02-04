from turtle import (bgcolor,forward,right,exitonclick,left)
from random import randint
from math import sqrt

bgcolor("lightblue")

def domecek(a):
    s = sqrt(2) * a / 2
    forward(a)
    right(90)
    forward(a)
    right(45)
    forward(s)
    right(90)
    forward(s)
    right(45)
    forward(a)
    right(45+90)
    forward(2*s)
    right(45+90)
    forward(a)
    right(45+90)
    forward(2*s)
def zemekoule(a):
    for i in range(8):
        domecek(a)

zemekoule(randint(10,200))
exitonclick()