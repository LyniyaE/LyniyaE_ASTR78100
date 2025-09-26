# HW3 Exercise 6.16: The Lagrange Point
# Using Newton's method to find where satellite stays between Earth and Moon

G = 6.674e-11
M = 5.972e24
m = 7.348e22
R = 3.844e8
w = 2.662e-6

# equation to solve: GM/r^2 - Gm/(R-r)^2 - w^2*r = 0
def f(r):
    return G*M/(r**2) - G*m/((R-r)**2) - w**2 * r

# derivative using central difference
def df(r):
    h = r * 1e-6 
    return (f(r + h) - f(r - h)) / (2 * h)

# make a plot first to find the root
import matplotlib.pyplot as plt

r_vals = []
f_vals = []
for i in range(50):
    r_test = 2.5e8 + (3.5e8 - 2.5e8) * i/49
    r_vals.append(r_test)
    f_vals.append(f(r_test))

plt.plot([r/1e6 for r in r_vals], f_vals)
plt.axhline(y=0, color='red', linestyle='--')
plt.xlabel('r (millions of m)')
plt.ylabel('f(r)')
plt.grid(True)
plt.show()

# starting value
r = 3.25e8
tol = 1e-10 

# newton's method
for i in range(10):
    f_r = f(r)
    df_r = df(r)
    r_new = r - f_r/df_r
    err = abs(r_new - r)
    
    print("iter", i+1, ": r =", r/1000, "km, error =", err)
    
    if err < tol:
        print("converged!")
        break
    
    r = r_new

print("Answer: r =", r/1000, "km")