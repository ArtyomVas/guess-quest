import random
import itertools

def generate_random_number():
    while True:
        number = [random.choice('0123456789') for _ in range(4)]
        digit_counts = {digit: number.count(digit) for digit in number}
        if all(count <= 2 for count in digit_counts.values()):
            return ''.join(number)

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

def choose_two_digits_and_indices(number):
    indices = random.sample(range(4), 2)
    digits = [number[i] for i in indices]
    return digits, indices

def generate_new_number_with_two_digits(digits, indices, original_digits):
    while True:
        new_number = list(generate_random_number())
        if any(digit in original_digits for digit in new_number):
            continue
        all_digits = [0, 1, 2, 3]
        filtered_list = [item for item in all_digits if item not in indices]
        permutations = list(itertools.permutations(filtered_list, 2))
        random.shuffle(permutations)
        new_indices = permutations[0]
        for i, digit in zip(new_indices, digits):
            new_number[i] = digit
        return ''.join(new_number)

def generate_new_number_with_two_digits_at_same_indices(digits, indices, original_digits):
    while True:
        new_number = list(generate_random_number())
        if any(new_number[i] in original_digits for i in range(4) if i not in indices):
            continue
        for i, digit in zip(indices, digits):
            new_number[i] = digit
        return ''.join(new_number)

def generate_unique_number(original_number):
    all_digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    original_digits = list(original_number)
    filtered_list = [item for item in all_digits if item not in original_digits]
    length = 4
    permutations = list(itertools.product(filtered_list, repeat=length))
    random.shuffle(permutations)
    return ''.join(permutations[0])

def is_valid_number(number):
    constraint1 = same_digit_number
    correct_count = sum(1 for i in range(4) if number[i] == constraint1[i])
    if correct_count < 1:
        return False

    constraint2 = different_places_number
    correct_digits = [i for i in range(4) if number[i] in constraint2 and number[i] != constraint2[i]]
    if len(correct_digits) != 2:
        return False

    constraint3 = same_places_number
    correct_count = sum(1 for i in range(4) if number[i] == constraint3[i])
    if correct_count != 2:
        return False

    constraint4 = unique_number
    if any(digit in constraint4 for digit in number):
        return False

    return True

def find_valid_numbers():
    valid_numbers = []
    for number in range(0, 10000):
        str_number = str(number).zfill(4)
        if is_valid_number(str_number):
            valid_numbers.append(str_number)
    return valid_numbers

def main():
    global same_digit_number, different_places_number, same_places_number, unique_number

    original_number = generate_random_number()
    one_digit = choose_digit_and_index(original_number)
    two_digits_diff = choose_two_digits_and_indices(original_number)
    two_digits_same = choose_two_digits_and_indices(original_number)
    unique_number = generate_unique_number(original_number)

    same_digit_number = generate_new_number_with_same_digit(one_digit[0], one_digit[1])
    different_places_number = generate_new_number_with_two_digits(two_digits_diff[0], two_digits_diff[1], set(original_number))
    same_places_number = generate_new_number_with_two_digits_at_same_indices(two_digits_same[0], two_digits_same[1], set(original_number))

    valid_numbers = find_valid_numbers()
    return len(valid_numbers)

if __name__ == "__main__":
    num_runs = 10000  # Number of runs to calculate the average
    total_valid_numbers = 0

    for _ in range(num_runs):
        total_valid_numbers += main()

    average_valid_numbers = total_valid_numbers / num_runs
    print(f"Average number of possible answers over {num_runs} runs: {average_valid_numbers}")
