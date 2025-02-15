import math
import random

def sum(*args):
    sumResult = 0
    for arg in args:
        sumResult += arg
    return sumResult

def minus(initialValue,*args):
    minusResult = initialValue
    for arg in args:
        minusResult -= arg
    return minusResult

def multiply(initialValue,*args):
    product = initialValue
    for arg in args:
        product *= arg
    return product

def divide(initialValue,*args):
    divisionResult = initialValue
    for arg in args:
        divisionResult /= arg
    return divisionResult

def powerof(initialValue,*args):
    powerResult = initialValue
    for arg in args:
        powerResult **= arg
    return powerResult

def length(var):
    return len(var)

def roundNum(var):
    return round(var)

def ceil(var):
    return math.ceil(var)

def floor(var):
    return math.floor(var)

def increment(var,by):
    return var + by

def decrement(var,by):
    return var - by

def rnd(min,max):
    return random.randint(min,max)

def modulus(value,by):
    return value % by