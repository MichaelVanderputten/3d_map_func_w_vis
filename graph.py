import math

def deg2(a,b,c, x):
    return a*x**2 + b*x + c

def deg3(a,b,c,d,x):
    return a*x**3 + b*x**2 + c*x + d

def lin(m,x,b):
    return m*x + b

def sinf(a,b,x,c,d):
    return a*math.sin(b*(x-c)) + d

def cosf(a,b,x,c,d):
    return a*math.cos(b*(x-c)) + d