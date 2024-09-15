import random
from datetime import datetime
from pprint import pprint

# Kichik do'st sonlar
small_friends = [(1, 4), (2, 3), (3, 2), (4, 1)]

def find_small_friend_pair(num):
    for pair in small_friends:
        if num in pair:
            return pair
    return None

def get_digit_range(digits):
    if digits == 1:
        return 1, 9
    elif digits == 2:
        return 10, 99
    elif digits == 3:
        return 100, 999
    elif digits == 4:
        return 1000, 9999
    elif digits == 5:
        return 10000, 99999
    else:
        raise ValueError("Digits must be between 1 and 5.")

def generate_example_parallel(column, digits):
    min_val, max_val = get_digit_range(digits)
    while True:
        if digits == 1:
            current_result = random.randint(1, 9)
        elif digits == 2:
            current_result = random.choice([i * 11 for i in range(1, 10)])
        elif digits == 3:
            current_result = random.choice([i * 111 for i in range(1, 10)])
        elif digits == 4:
            current_result = random.choice([i * 1111 for i in range(1, 10)])
        elif digits == 5:
            current_result = random.choice([i * 11111 for i in range(1, 10)])
        else:
            raise ValueError("Digits must be between 1 and 5.")

        numbers = [current_result]
        operations = []
        small_friend_found = False

        for _ in range(column - 1):
            operation = random.choice(['+', '-'])
            num = random.choice([i * 11111 for i in range(1, 10)])

            small_friend_pair = find_small_friend_pair(num // 10 ** (digits - 1))
            if not small_friend_pair:
                continue

            if operation == '+':
                if current_result + num <= max_val:
                    current_result += num
                    numbers.append(num)
                    operations.append(operation)
                    if current_result // 10 ** (digits - 1) in small_friend_pair:
                        small_friend_found = True
                else:
                    continue
            elif operation == '-':
                if current_result - num >= min_val:
                    current_result -= num
                    numbers.append(num)
                    operations.append(operation)
                    if current_result // 10 ** (digits - 1) in small_friend_pair:
                        small_friend_found = True
                else:
                    continue

        if len(numbers) == column and small_friend_found and min_val <= current_result <= max_val:
            expression = f'{numbers[0]}'
            for i in range(column - 1):
                expression += f" {operations[i]}{numbers[i + 1]}"
            return expression, current_result

def generate_example_mixed(column, digits):
    min_val, max_val = get_digit_range(digits)
    while True:
        current_result = random.randint(min_val, max_val)
        numbers = [current_result]
        operations = []
        small_friend_found = False

        for _ in range(column - 1):
            operation = random.choice(['+', '-'])
            num = random.randint(min_val, max_val)

            small_friend_pair = find_small_friend_pair(num % 10)
            if not small_friend_pair:
                continue

            if operation == '+':
                if current_result + num <= max_val:
                    current_result += num
                    numbers.append(num)
                    operations.append(operation)
                    if current_result % 10 in small_friend_pair:
                        small_friend_found = True
                else:
                    continue
            elif operation == '-':
                if current_result - num >= min_val:
                    current_result -= num
                    numbers.append(num)
                    operations.append(operation)
                    if current_result % 10 in small_friend_pair:
                        small_friend_found = True
                else:
                    continue

        if len(numbers) == column and small_friend_found and min_val <= current_result <= max_val:
            expression = f'{numbers[0]}'
            for i in range(column - 1):
                expression += f" {operations[i]}{numbers[i + 1]}"
            return expression, current_result

def generate_example_tenner(column, digits):
    min_val, max_val = get_digit_range(digits)
    while True:
        if digits == 1:
            current_result = random.randint(1, 9)
        elif digits == 2:
            current_result = random.choice([i * 10 for i in range(1, 10)])
        elif digits == 3:
            current_result = random.choice([i * 100 for i in range(1, 10)])
        elif digits == 4:
            current_result = random.choice([i * 1000 for i in range(1, 10)])
        elif digits == 5:
            current_result = random.choice([i * 10000 for i in range(1, 10)])
        else:
            raise ValueError("Digits must be between 1 and 5.")

        numbers = [current_result]
        operations = []
        small_friend_found = False

        for _ in range(column - 1):
            operation = random.choice(['+', '-'])
            num = random.choice([i * 10000 for i in range(1, 10)])

            small_friend_pair = find_small_friend_pair(num // 10 ** (digits - 1))
            if not small_friend_pair:
                continue

            if operation == '+':
                if current_result + num <= max_val:
                    current_result += num
                    numbers.append(num)
                    operations.append(operation)
                    if current_result // 10 ** (digits - 1) in small_friend_pair:
                        small_friend_found = True
                else:
                    continue
            elif operation == '-':
                if current_result - num >= min_val:
                    current_result -= num
                    numbers.append(num)
                    operations.append(operation)
                    if current_result // 10 ** (digits - 1) in small_friend_pair:
                        small_friend_found = True
                else:
                    continue

        if len(numbers) == column and small_friend_found and min_val <= current_result <= max_val:
            expression = f'{numbers[0]}'
            for i in range(column - 1):
                expression += f" {operations[i]}{numbers[i + 1]}"
            return expression, current_result

def small_friend(column=5, digits=1, count=10, requirement='+3', method='mixed'):
    print("Generating...")
    response = {
        'examples': [],
        'results': []
    }

    for _ in range(count):
        if method == 'parallel':
            example, result = generate_example_parallel(column, digits)
        elif method == 'mixed':
            example, result = generate_example_mixed(column, digits)
        elif method == 'tenner':
            example, result = generate_example_tenner(column, digits)
        else:
            raise ValueError("Method must be 'parallel', 'mixed', or 'tenner'.")

        if example and result:
            td = example.split(' ')
            response['examples'].append(td)
            response['results'].append(result)

    return response


if __name__ == '__main__':
    start = datetime.now()
    for _ in range(10):
        print(_ + 1)
        pprint(small_friend(column=10, digits=5, method='mixed'))
    end = datetime.now()
    print(f"Execution time: {end - start}")
