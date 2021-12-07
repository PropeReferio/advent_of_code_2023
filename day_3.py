from collections import Counter

epsilon, gamma = '', ''

with open("./inputs/day_3.txt") as rf:
    binary = rf.read().split('\n')

# for i in range(len(binary[-1])):
#     zeroes = 0
#     ones = 0
#     for num in binary:
#         if num[i] == '0':
#             zeroes += 1
#         elif num[i] == '1':
#             ones += 1
#     if ones > zeroes:
#         gamma += '1'
#         epsilon += '0'
#     else:
#         gamma += '0'
#         epsilon += '1'
#
# gamma_base_10 = int(gamma, 2)
# epsilon_base_10 = int(epsilon, 2)
# print(f"base 2: {gamma}, base 10: {gamma_base_10}")
# print(f"base 2: {epsilon}, base 10: {epsilon_base_10}")
#
# print(epsilon_base_10 * gamma_base_10)

# Part 2
oxygen_binary = binary.copy()
for i in range(len(oxygen_binary[-1])):
    # Per digit loop
    zeroes = 0
    ones = 0
    ones_index_list = []
    zeroes_index_list = []
    for j, num in enumerate(oxygen_binary):
        # Per whole number loop
        if num[i] == '0':
            zeroes += 1
            zeroes_index_list.append(j)
        elif num[i] == '1':
            ones += 1
            ones_index_list.append(j)
    if ones >= zeroes:
        # if ones are equally common, keep ones.
        oxygen_binary = [oxygen_binary[index] for index in ones_index_list]
    else:
        oxygen_binary = [oxygen_binary[index] for index in zeroes_index_list]
    if len(oxygen_binary) == 1:
        break

oxygen_generator_rating = int(oxygen_binary[0], 2)

co2_binary = binary.copy()
for i in range(len(co2_binary[-1])):
    # Per digit loop
    zeroes = 0
    ones = 0
    ones_index_list = []
    zeroes_index_list = []
    for j, num in enumerate(co2_binary):
        # Per whole number loop
        if num[i] == '0':
            zeroes += 1
            zeroes_index_list.append(j)
        elif num[i] == '1':
            ones += 1
            ones_index_list.append(j)
    if ones >= zeroes:
        co2_binary = [co2_binary[index] for index in zeroes_index_list]
    else:
        co2_binary = [co2_binary[index] for index in ones_index_list]
    if len(co2_binary) == 1:
        break


co2_scrubber_rating = int(co2_binary[0], 2)

print(co2_scrubber_rating * oxygen_generator_rating)