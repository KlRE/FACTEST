#need to implement add, multiply, exponential, divide, subtract
import numpy as np
import math
# from scipy.optimize import minimize
import scipy.optimize as opt

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

# #USER INPUTS CONSTANTS/VARIABLES
# class Constants: #to set constants values
#     c = 0.5
#     k0 = 100

# class Variables: #to set constaints (for now only er)
#     er_min = 0
#     er_max = 2*math.pi




class constant:
    def __init__(self, name : str, value : float):
        self.value = value
        self.name = name

class variable:
    def __init__(self, name : str, bounds = [None, None]): #MAY NEED TO CHANGE BOUNDS = NONE (for inf stuff)
        self.name = name
        self.bounds = bounds

# k = constant(100, 'k')
# theta_err = variable([0, 2*pi], 'e_theta')

class lyapunov:
    def __init__(self, alpha, beta):
        self.alpha = alpha
        self.beta = beta

 
class beta:
    def __init__(self, variables, constants, equation): #variables/constants are list of respective class, equation is string
        
        self.const_names = [const.name for const in constants]
        self.const_val = [const.value for const in constants] #gets the values in order of const name


        self.var_names = [var.name for var in variables]
        self.var_bounds = [var.bounds for var in variables] #bounds in order of const name
        self.init_guess = [(var.bounds[0]+var.bounds[1]-(var.bounds[0]+var.bounds[1])/100)/2 for var in variables] #min of the bounds for init guess
        self.beta = eval(f"lambda {', '.join(self.const_names + self.var_names)}: {equation}") #joins const + variables EX: ['x','y'] -> "x, y"

        models = ["L-BFGS-B", "SLSQP", "Powell", "TNC", "Nelder-Mead", "COBYLA"]
        self.computed_var_min = opt.minimize(lambda vars: self.beta(*self.const_val, *vars), self.init_guess, bounds=self.var_bounds, method = 'Powell') #can test with diff methods
        self.computed_var_max = opt.minimize(lambda vars: -self.beta(*self.const_val, *vars), self.init_guess, bounds=self.var_bounds, method = 'Powell')
        

        self.minimum = self.beta(*self.const_val, *self.computed_var_min.x)
        self.maximum = self.beta(*self.const_val, *self.computed_var_max.x)


# class alpha:
#     def __init__(self, constants, variables, equation)\
print("Hovercraft:")
equation0 = "(1-math.cos(etheta))/(k0)"

# c = constant("c", 0.5)
k0 = constant("k0",1)
etheta = variable( "etheta", [0,2*math.pi])
print(f"With beta as {equation0}")
print(f"etheta bounds: {etheta.bounds}")
# print(f"c: {c.value}")
print(f"k0: {k0.value}")
# func = beta([etheta],[c, k0], "1/2*(1-math.cos(etheta))/(c*k0)")
func = beta([etheta],[k0], equation0)
#hovercraft

print("Min: ", func.minimum, " Max: ", func.maximum)

# print(func.computed_var_min)
# print()
print("==============================================")
print("Robot:")
equation = "(1/(2*(1+ec/a)))*(ec**2+es**2)"

ec = variable("ec", [-1,1])
es = variable("es", [-1,1])
a = constant("a", 3)

print(f"With beta as {equation}")
print(f"ec bounds: {ec.bounds}")
print(f"es bounds: {es.bounds}")
print(f"a: {a.value}")
robot = beta([ec, es],[a], equation)

print("Min: ", robot.minimum, " Max: ", robot.maximum)

print("==============================================")
print("AUV:")
equation2 = "np.dot(np.array([k1, k2, k3]), np.array([1-math.cos(phi), 1-math.cos(theta), 1-math.cos(psi)]))"

phi = variable("phi", [0,2*math.pi])
theta = variable("theta", [0,2*math.pi])
psi = variable("psi", [0,2*math.pi])

k1 = constant( "k1", 1)
k2 = constant( "k2", 0.01)
k3 = constant("k3", 0.0001)

print(f"With beta as {equation2}")
for var in [phi, theta, psi]:
    print(f"{var.name} bounds: {var.bounds}")
for const in [k1, k2, k3]:
    print(f"{const.name}: {const.value}")

auv = beta([phi, theta, psi],[k1, k2, k3], equation2)

# print(f"With beta as {equation}")
# print(f"ec bounds: {ec.bounds}")
# print(f"es bounds: {es.bounds}")
# print(f"a: {a.value}")
print("Min: ", auv.minimum, " Max: ", auv.maximum)
