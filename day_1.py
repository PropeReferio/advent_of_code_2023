from pathlib import Path

# To do this, count the number of times a depth measurement increases from
# the previous measurement. (There is no measurement before the first

with open(Path("C:/Users/boste/OneDrive/Desktop/day_1_input.txt"), "r") as rf:
    depths = [int(depth) for depth in rf.read().split()]

increases = 0

for i in range(1, len(depths)):
    if depths[i] > depths[i-1]:
        increases += 1

# print(increases)

# Pt. 2 - comparing sum of three depths
increases = 0

for i in range(3, len(depths)):
    group_a = sum([depths[i-1], depths[i-2], depths[i-3]])
    group_b = sum([depths[i], depths[i-1], depths[i-2]])
    if group_b > group_a:
        increases += 1

print(increases)