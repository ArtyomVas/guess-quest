# import itertools
# import random
#
#
# # Define your list of characters
# char_list = ['0', '1', '2', '3', '4', '5']
# print(char_list)
# char_list_2 = ['0', '1']
# print(char_list_2)
# filtered_list = [item for item in char_list if item not in char_list_2]
# print(filtered_list)
#
#
# # Generate permutations of length 2
# permutations_length_2 = list(itertools.permutations(filtered_list, 4))
# random.shuffle(permutations_length_2)
# print(permutations_length_2[0])
# # Print the permutations of length 2
# # for perm in permutations_length_2:
# #     print(perm)
# import itertools
#
#
# num_set = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
# permutations = list(itertools.permutations(num_set, 2))
# print(permutations)
#
# # Length of the permutations
# length = 4
#
# # Generate permutations with repetition
# permutations_with_repetition = itertools.product(num_set, repeat=length)
#
# # Convert the tuples to strings
# result = [''.join(p) for p in permutations_with_repetition]
#
# # Print the result
# for perm in result:
#     print(perm)

import random


def generate_custom_number():
    while True:
        number = [random.choice('0123456789') for _ in range(4)]

        # Count the occurrences of each digit
        digit_counts = {digit: number.count(digit) for digit in number}

        # Check if any digit occurs more than twice
        if all(count <= 2 for count in digit_counts.values()):
            return ''.join(number)


# Example usage
for _ in range(10):  # Generate 10 examples
    print(generate_custom_number())