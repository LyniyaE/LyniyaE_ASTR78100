import numpy as np
import plotly.graph_objects as go

# convert to first order system
# x1 = x, x2 = y, x3 = vx, x4 = vy
# dx1/dt = x3
# dx2/dt = x4  
# dx3/dt = -alpha*x1/(x1^2 + x2^2)^(3/2)
# dx4/dt = -alpha*x2/(x1^2 + x2^2)^(3/2)

def derivatives(t, state):
    x, y, vx, vy = state
    alpha = 10/2  # GM/L with G=1, M=10, L=2
    
    r2 = x**2 + y**2
    r32 = r2**(1.5)
    
    dxdt = vx
    dydt = vy
    dvxdt = -alpha * x / r32
    dvydt = -alpha * y / r32
    
    return np.array([dxdt, dydt, dvxdt, dvydt])

# runge kutta 4th order
def rk4(f, t, y, h):
    k1 = h * f(t, y)
    k2 = h * f(t + h/2, y + k1/2)
    k3 = h * f(t + h/2, y + k2/2)
    k4 = h * f(t + h, y + k3)
    return y + (k1 + 2*k2 + 2*k3 + k4)/6

# initial conditions and parameters
x0 = 1.0
y0 = 0.0
vx0 = 0.0
vy0 = 1.0

t_start = 0
t_end = 10
dt = 0.01
steps = int((t_end - t_start) / dt)

# arrays for results
t = np.zeros(steps + 1)
x = np.zeros(steps + 1)
y = np.zeros(steps + 1)

# initial values
t[0] = t_start
state = np.array([x0, y0, vx0, vy0])
x[0] = state[0]
y[0] = state[1]

# solve ode
for i in range(steps):
    t[i+1] = t[i] + dt
    state = rk4(derivatives, t[i], state, dt)
    x[i+1] = state[0]
    y[i+1] = state[1]

# plot
fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='orbit'))
fig.add_trace(go.Scatter(x=[x[0]], y=[y[0]], mode='markers', name='start'))
fig.add_trace(go.Scatter(x=[0], y=[0], mode='markers', name='rod center'))
fig.update_layout(title='orbit plot', xaxis_title='x', yaxis_title='y')
fig.update_xaxes(scaleanchor="y", scaleratio=1)
fig.show()
