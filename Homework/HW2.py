import math
import matplotlib.pyplot as plt

def f(x):
    return math.exp(-x**2)

a = 0.0
b = 3.0
step = 0.1
N = 1000

# i have to store all the values to plot them
x_values = []
trap_values = []

x = a
while x <= b + 1e-10:  # stops at 3, tiny bit extra just in case
    # Trapezoidal
    h = (x - a) / N
    s = 0.5*f(a) + 0.5*f(x)
    for k in range(1, N):
        s += f(a + k*h)
    trap_values.append(h * s)  # .append() adds this value to end of list
    
    x_values.append(x)  # saves current x value to the list
    x += step

plt.plot(x_values, trap_values, color='hotpink')
plt.xlabel("x")
plt.ylabel("E(x)")
plt.title("Numerical Integration of e^(-t²) from 0 to x")
plt.grid(True)
plt.show()