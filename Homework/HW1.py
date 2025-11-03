import argparse
import math
import matplotlib.pyplot as plt

# Dictionary of gravity values for different planets
gravity_dict = {
    "earth": 9.81,
    "mars": 3.71,
    "moon": 1.62,
    "jupiter": 24.79,
    "venus": 8.87,
    "saturn": 10.44,
    "mercury": 3.7,
    "uranus": 8.69,
    "neptune": 11.15,
    "sun": 274.0,
    "pluto": 0.62,
    "titan": 1.35,
    "europa": 1.31,
    "io": 1.8
}

def calculate_time(height, gravity):
    # Formula: t = sqrt(2 * height / gravity)
    time = math.sqrt(2 * height / gravity)
    return time

def create_comparison_chart(height):
    # Calculate fall times for all planets
    planets = []
    times = []
    
    for planet, gravity in gravity_dict.items():
        fall_time = calculate_time(height, gravity)
        planets.append(planet.title())
        times.append(fall_time)
    
    # Create the bar chart
    plt.bar(planets, times)
    plt.title('Fall Time Comparison - Height: ' + str(height) + ' meters')
    plt.xlabel('Planet')
    plt.ylabel('Fall Time (seconds)')
    plt.show()

def main():
    # Set up command line arguments
    parser = argparse.ArgumentParser(description="Calculate how long it takes for a ball to fall")
    
    # Add arguments
    parser.add_argument("height", type=float, help="Height in meters")
    parser.add_argument("-g", "--gravity", type=float, default=9.81, help="Gravity value")
    parser.add_argument("-p", "--planet", type=str, help="Choose a planet")
    
    # Get the arguments
    args = parser.parse_args()
    
    # Check if user picked a planet
    if args.planet:
        if args.planet in gravity_dict:
            gravity = gravity_dict[args.planet]
            planet_name = args.planet
        else:
            print("Sorry, don't know that planet. Using Earth.")
            gravity = 9.81
            planet_name = "earth"
    else:
        gravity = args.gravity
        planet_name = "custom"
    
    # Calculate the time
    fall_time = calculate_time(args.height, gravity)
    
    # Print results
    print("Height:", args.height, "meters")
    print("Gravity:", gravity, "m/s^2")
    print("Time to fall:", round(fall_time, 2), "seconds")
    print("Planet:", planet_name)
    create_comparison_chart(args.height)

if __name__ == "__main__":
    main()