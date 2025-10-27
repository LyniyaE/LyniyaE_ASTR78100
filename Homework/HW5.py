import numpy as np
import matplotlib.pyplot as plt
import random
import math
import matplotlib.animation as animation

# Photon in a slab
mean_free_path = 150  # meters

def simulate_photon():
    x = 0  # position
    direction = 1
    xpos = [0]
    ypos = [0]
    scatters = 0
    total_dis = 0
    
    while True:
        # get random step size 
        r = random.random()
        step = -mean_free_path * math.log(r)
        total_dis = total_dis + step
        
        # move the photon
        newx = x + step * direction
        
        # check where photon ended up
        if newx >= 1000:
            # photon gone
            xpos.append(1000)
            ypos.append(ypos[-1])
            return xpos, ypos, "escaped", scatters, total_dis
        elif newx <= 0:
            # photon got reflected back
            xpos.append(0)
            ypos.append(ypos[-1])
            return xpos, ypos, "reflected", scatters, total_dis
        else:
            # photon is still inside, so it scatters
            x = newx
            scatters = scatters + 1
            
            # pick random scattering angle from 0 to 180 degrees
            angle = random.random() * math.pi  # in radians
            direction = math.cos(angle)  # new direction
            
            # save the position
            xpos.append(x)
            ypos.append((random.random() - 0.5) * 30)  # add random y for animation
            
            # stop if too many scatterings
            if scatters > 1000:
                return xpos, ypos, "too_many", scatters, total_dis

# run one simulation
x_path, y_path, outcome, num_scatterings, distance = simulate_photon()

print("Outcome:", outcome)
print("Number of scatterings:", num_scatterings)
print("Total distance traveled:", distance, "m")
print("Distance ratio (total/slab width):", distance/1000)

# plot the photon path
plt.figure(figsize=(10, 4))
plt.plot(x_path, y_path, 'b-', linewidth=1)
plt.plot(x_path, y_path, 'ro', markersize=3)
# draw slab boundaries
plt.axvline(0, color='black', linewidth=2, label='slab boundaries')
plt.axvline(1000, color='black', linewidth=2)
plt.xlabel('Position (m)')
plt.ylabel('Y offset (for visualization)')
plt.title('Photon path through slab')
plt.legend()
plt.grid(True)
plt.show()

# animation of photon path
x_anim, y_anim, result_anim, scatt_anim, dist_anim = simulate_photon()
print("Animation photon:", result_anim, "with", scatt_anim, "scatterings")

fig = plt.figure(figsize=(10,4))
ax = plt.axes(xlim=(-50, 1050), ylim=(-40, 40))
ax.axvline(0, color='black', linewidth=3)
ax.axvline(1000, color='black', linewidth=3)
line, = ax.plot([], [], 'b-', linewidth=1)
point, = ax.plot([], [], 'ro', markersize=5)

def init():
    line.set_data([], [])
    point.set_data([], [])
    return line, point

def animate(i):
    if i < len(x_anim):
        # draw path up to current point
        line.set_data(x_anim[:i+1], y_anim[:i+1])
        # show current position
        point.set_data([x_anim[i]], [y_anim[i]])
    return line, point

anim = animation.FuncAnimation(fig, animate, init_func=init, frames=len(x_anim), interval=400, blit=True)

plt.show()


import numpy as np
import matplotlib.pyplot as plt
import math

sigma_T = 6.65e-25        
R_sun = 6.96e10           
c = 3e10                  
Na = 6.02e23              
escape_radius = 0.7 * R_sun

def photon_simulation():
    # Start in 3D space
    x, y, z = 0.05 * R_sun, 0.0, 0.0
    r = 0.05 * R_sun  
    total_distance = 0.0
    scatterings = 0
    
    radii_plot = []
    scattering_numbers = []
    
    for i in range(20000):
        step_size = (1e6 + r/1000) * np.random.exponential(1)
        
        phi = np.random.uniform(0, 2*np.pi)
        cos_theta = np.random.uniform(-1, 1)
        sin_theta = np.sqrt(1 - cos_theta**2)
        
        #3D
        x += step_size * sin_theta * np.cos(phi)
        y += step_size * sin_theta * np.sin(phi)
        z += step_size * cos_theta
        
        # Calculate new radius
        r = np.sqrt(x**2 + y**2 + z**2)
        
        if r > escape_radius:
            break
            
        total_distance += step_size
        scatterings += 1
        
        # Save every 500 steps
        if i % 500 == 0:
            radii_plot.append(r)
            scattering_numbers.append(scatterings)
    
    escape_time = total_distance / c
    return scatterings, escape_time, radii_plot, scattering_numbers

num_scatterings, time_seconds, r_data, scatter_data = photon_simulation()
time_years = time_seconds / (365 * 24 * 3600)

print(f"Number of scatterings: {num_scatterings}")
print(f"Escape time: {time_years:.2e} years")

plt.figure(figsize=(10, 6))
plt.plot(scatter_data, np.array(r_data)/R_sun, 'orange', linewidth=2)
plt.xlabel('Scattering Number')
plt.ylabel('Radius (Solar Radii)')
plt.title('Photon Escaping')
plt.grid(True)
plt.show()

'''
My escape time is way too fast!! 
As if there's a black hole in the Sun.
'''