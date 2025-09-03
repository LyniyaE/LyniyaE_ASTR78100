import argparse
parser = argparse.ArgumentParser(description="Check if a number is positive, negative, or zero")
parser.add_argument("x", type=float, help="enter a number")
args = parser.parse_args()
x = args.x
if x > 0:
    print("is positive")
elif x < 0:
    print("is negative")
else:
    print("is zero")