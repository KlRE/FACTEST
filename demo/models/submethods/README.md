## Libraries Used
- [Numpy]
- [Scipy]

## Usage

To use the Lyapunov class to calculate the lower and upper bounds of beta, the user needs to define variables, constants, as well as the equation used. 

## Define Variables and Constants

Each variable used in the function is defined with the variable class. The variable class has the following attributes:

| Attribute          | Type              | Default | Description |
| ------------------ | ----------------- | ------- | ----------- |
| `name`             | String            |         | Name of variable
| `bounds`           | list of float     | `[None, None]` | Lower and upper bound of variable

Each constant used in the function is defined with the constant class. The constant class has the following attributes:
| Attribute          | Type              |  Description |
| ------------------ | ----------------- |  ----------- |
| `name`             | String  |  Name of constant                   |
| `value`            | float |  Value of constant             |

```
beta_function = beta(variables, constants, equation)
```

| Arg                | Type              |  Description |
| ------------------ | ----------------- |  ----------- |
| `variables`        | list of variable  |  List of variables that will be used in the equation                   |
| `constants`        | list of constant  |  List of constants that will be used in the equation              |
| `equation`         | String |          |  Equation in string form          |

The beta class has the following attributes

| Attribute          | Type              | Description |
| ------------------ | ----------------- |  ----------- |
| `const_names`      | list of Strings   |  List of constant names used in equation                  |
| `const_val`        | list of floats    |  List of values corresponding to constant values in const_names     |
| `var_names`        | list of Strings   |  List of variable names used in equation           |
| `var_bounds`       | 2d list of floats |  List of bounds corresponding to each variable                       |
| `init_guess`       | list of floats    |  Initial guesses for each variable |
| `beta`             | lambda function   |  Lambda function         |
| `computed_var_min` |                   |  Output of minimize function                       |
| `computed_var_max` |                   |  Output of maximize function                        |
| `minimum`          | float             |  Lower bound                        |
| `maximum`          | float             |  Upper bound                       |

The minimum and maximum values are calculated using the scipy.optimize.minimize function. This function allows for many different computation models, which may need to be adjusted depending on the beta equation used. 
**Currently implemented loop through a bunch of models in beta class to see which works best**

## Variable and Constant Definition Example

Two variables and one constant (based on the Robot Model)

```
ec = variable("ec", [-2,0])
es = variable("es", [-1,1])
a = constant("a", 100)
```

Three variables and three constants (based on the AUV Model)
```
phi = variable("phi", [0,2*math.pi])
theta = variable("theta", [0,2*math.pi])
psi = variable("psi", [0,2*math.pi])

k1 = constant( "k1", 10)
k2 = constant( "k2", 100)
k3 = constant("k3", 1000)
```

## Complete Example

### Hovercraft Model
```
hover_eq = "(1-math.cos(etheta))/(k0)"

k0 = constant("k0",1)
etheta = variable( "etheta", [0,2*math.pi])

func = beta([etheta],[k0], hover_eq)
```
This returns a range of $[0,2]$, which matches the theoretical range of $[0, \frac{2}{k0}]$
### Autonomous Underwater Vehicle (AUV) Model
```
auv_eq = "np.dot(np.array([k1, k2, k3]), np.array([1-math.cos(phi), 1-math.cos(theta), 1-math.cos(psi)]))"

phi = variable("phi", [0,2*math.pi])
theta = variable("theta", [0,2*math.pi])
psi = variable("psi", [0,2*math.pi])

k1 = constant( "k1", 10)
k2 = constant( "k2", 100)
k3 = constant("k3", 1000)

auv = beta([phi, theta, psi],[k1, k2, k3], auv_eq)
```
This returns a range of $[0,2220]$, which matches the theoretical range of $[0, 2(k1 + k2 + k3)]$