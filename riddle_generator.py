import random
import itertools
from db_manager import *


###########################################################################################
# Creates the first "One correct number in the correct place" number:


def generate_random_number():
    while True:
        number = [random.choice('0123456789') for _ in range(4)]

        # Count the occurrences of each digit
        digit_counts = {digit: number.count(digit) for digit in number}

        # Check if any digit occurs more than twice
        if all(count <= 2 for count in digit_counts.values()):
            return ''.join(number)


###########################################################################################
# Creates the first "One correct number in the correct place" number:


def choose_digit_and_index(number):
    index = random.randint(0, 3)
    digit = number[index]
    return digit, index


def generate_new_number_with_same_digit(digit, index):
    while True:
        new_number = list(generate_random_number())
        new_number[index] = digit
        if new_number[index] == digit:
            return ''.join(new_number)


###########################################################################################
# Creates the second "two correct numbers in wrong places" number:


def choose_two_digits_and_indices(number):
    indices = random.sample(range(4), 2)
    digits = [number[i] for i in indices]
    return digits, indices


def generate_new_number_with_two_digits(digits, indices, original_digits):
    while True:
        new_number = list(generate_random_number())
        if any(digit in original_digits for digit in new_number):  # Verifies it's not the same number
            continue

        all_digits = [0, 1, 2, 3]
        filtered_list = [item for item in all_digits if item not in indices]
        permutations = list(itertools.permutations(filtered_list, 2))
        random.shuffle(permutations)
        new_indices = permutations[0]

        for i, digit in zip(new_indices, digits):
            new_number[i] = digit
        return ''.join(new_number)


###########################################################################################
# Creates the third "two correct numbers in correct places" number:


def generate_new_number_with_two_digits_at_same_indices(digits, indices, original_digits):
    while True:
        new_number = list(generate_random_number())
        if any(new_number[i] in original_digits for i in range(4) if i not in indices):
            continue
        for i, digit in zip(indices, digits):
            new_number[i] = digit
        return ''.join(new_number)


###########################################################################################
# Creates the fourth "wrong" number:


def generate_unique_number(original_number):
    all_digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    original_digits = list(original_number)
    filtered_list = [item for item in all_digits if item not in original_digits]
    length = 4
    permutations = list(itertools.product(filtered_list, repeat=length))
    random.shuffle(permutations)
    return ''.join(permutations[0])


def create_riddle():
    original_number = generate_random_number()
    print("Original 4-digit random number:", original_number)
    one_digit = choose_digit_and_index(original_number)
    two_digits_diff = choose_two_digits_and_indices(original_number)
    two_digits_same = choose_two_digits_and_indices(original_number)
    unique_number = generate_unique_number(original_number)
    same_digit_number = generate_new_number_with_same_digit(one_digit[0], one_digit[1])
    print(f"One digit at same place: {one_digit} -> {same_digit_number}")
    different_places_number = generate_new_number_with_two_digits(two_digits_diff[0], two_digits_diff[1],
                                                                  set(original_number))
    print(f"Two digits at different places: {two_digits_diff} -> {different_places_number}")
    same_places_number = generate_new_number_with_two_digits_at_same_indices(two_digits_same[0], two_digits_same[1],
                                                                             set(original_number))
    print(f"Two digits at same places: {two_digits_same} -> {same_places_number}")
    print(f"Completely different number: {unique_number}")

    return [same_digit_number, different_places_number, same_places_number, unique_number]


###########################################################################################
# Counts how many numbers can meet the constraints:


def is_valid_number(number, hint1, hint2, hint3, hint4):
    # Constraint 1: One digit is correct and in the correct index: same_digit_number
    constraint1 = hint1
    correct_count = sum(1 for i in range(4) if number[i] == constraint1[i])
    if correct_count < 1:
        return False

    # Constraint 2: Two digits are correct but in different indexes: different_places_number
    constraint2 = hint2
    correct_digits = [i for i in range(4) if number[i] in constraint2 and number[i] != constraint2[i]]
    if len(correct_digits) != 2:
        return False

    # Constraint 3: Two digits are correct and in their correct indexes: same_places_number
    constraint3 = hint3
    correct_count = sum(1 for i in range(4) if number[i] == constraint3[i])
    if correct_count != 2:
        return False

    # Constraint 4: None of the digits are correct: unique_number
    constraint4 = hint4
    if any(digit in constraint4 for digit in number):
        return False

    return True


def get_number_of_riddle_solutions(hint1, hint2, hint3, hint4):
    valid_numbers = []
    for number in range(0, 10000):
        str_number = str(number).zfill(4)
        if is_valid_number(str_number, hint1, hint2, hint3, hint4):
            valid_numbers.append(str_number)
    # print("Number of possible answers:", len(valid_numbers))
    print("Valid numbers that meet all constraints:", valid_numbers)
    return len(valid_numbers)


def user_has_solved_riddle(user_id, riddle_id):
    user_data_dict = get_user_dict(user_id)

    for riddle in user_data_dict["riddles"]:
        if riddle["riddleId"] == riddle_id and riddle["status"] == "solved":
            return True

    return False


def user_has_gaveup_riddle(user_id, riddle_id):
    user_data_dict = get_user_dict(user_id)

    for riddle in user_data_dict["riddles"]:
        if riddle["riddleId"] == riddle_id and riddle["status"] == "gaveup":
            return True

    return False
