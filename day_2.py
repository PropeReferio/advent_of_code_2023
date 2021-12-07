from pathlib import Path

start_x, start_y = 0, 0

with open(Path("./inputs/day_2.txt"), "r") as rf:
    paths = [line for line in rf.read().split("\n")]

for path in paths:
    direction, value = path.split(" ")
    value = int(value)
    if direction == "forward":
        start_x += value
    elif direction == "up":
        start_y -= value
    elif direction == "down":
        start_y += value

print(start_x * start_y)

# Part 2

start_x, start_y, aim = 0, 0, 0

for path in paths:
    direction, value = path.split(" ")
    value = int(value)
    if direction == "forward":
        start_x += value
        start_y += aim * value
    elif direction == "up":
        aim -= value
    elif direction == "down":
        aim += value

print(start_x * start_y)