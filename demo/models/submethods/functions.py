#need to implement add, multiply, exponential, divide, subtract
import numpy
import math
from scipy.optimize import minimize_scalar

# from fractions import Fraction

def add(first, second):
    #first/second: float
    return first + second

def multiply(first, second):
    #first/second: float
    return first * second

def divide(first, second):
    return first / second

def subtract(first, second):
    return first - second

def exponential(base, exponent):
    #base: String
    #exponent: float
    # return float(sum(Fraction(s) for s in base.split()))**exponent
    return base**exponent
        # need lower and upper bounds for er (etheta)
        #er has user provided bound
        # beta(er) has our bounds
        # see if can return 


class Constants: #to set constants values
    c = 0.5
        # self.c = value 

class Variables: #to set constaints (for now only er)
    # def __init__(self, er_min, er_max):
    er_min = 0
    er_max = 2*math.pi

class lyaponuv:
    def __init__(self, alpha, beta) -> None:
        #where alpha and beta are strings of the formula
        value = 0.5 #float
        self.constants = Constants()
        self.variables = Variables()


        # self.alpha = add(multiply(self.c,exponential(self.ex,2)), multiply(self.c,exponential(self.ey,2)))
        self.alpha = eval(f"lambda x,y: {alpha}")
        self.beta = eval(f"lambda theta: {beta}")
        # self.beta = lambda theta: 1/2*theta**2
        # self.beta = lambda theta: (1-math.cos(theta))/2

    def beta_bounds(self):
        er_bounds = (self.variables.er_min, self.variables.er_max)
        minimum = minimize_scalar(lambda theta: self.beta(theta), bounds=er_bounds, method='bounded')
        maximum = minimize_scalar(lambda theta: -self.beta(theta), bounds=er_bounds, method='bounded')
        return (self.beta(minimum.x)/self.constants.c, self.beta(maximum.x)/self.constants.c)

testing = lyaponuv("1", "1/2*theta**2")
min_1, max_1 = testing.beta_bounds()
print("Given bounds: (", testing.variables.er_min,", ", testing.variables.er_max, ")")
print("With beta as 1/2*theta**2")
print("Computed min: " ,min_1, " Computed max: ", max_1)

print(4*math.pi**2)
print(max_1/math.pi)
