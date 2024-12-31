from sympy import symbols, Eq, solve

# Define the variable x (change in concentration)
x = symbols('x')

# Known values
Kc = 0.62  # Equilibrium constant

# Initial concentrations (mol/L, assume V cancels out)
CO_initial = 0.01
H2O_initial = 0.50
CO2_initial = 0.30
H2_initial = 0.10

# Equilibrium concentrations in terms of x
CO_eq = CO_initial - x
H2O_eq = H2O_initial - x
CO2_eq = CO2_initial + x
H2_eq = H2_initial + x

# Equilibrium expression
equation = Eq(Kc, (CO2_eq * H2_eq) / (CO_eq * H2O_eq))

# Solve for x
x_solution = solve(equation, x)
print(x_solution)