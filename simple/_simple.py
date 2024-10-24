import random
import pprint
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed


def get_number(current_number, operation='+'):
    if operation == '+':
        if current_number == 0:
            number = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        elif current_number == 1:
            number = random.choice([1, 2, 3, 5])
        elif current_number == 2:
            number = random.choice([1, 2, 5])
        elif current_number == 3:
            number = random.choice([1, 2, 5])
        elif current_number == 4:
            number = random.choice([5])
        elif current_number == 5:
            number = random.choice([1, 2, 3, 4])
        elif current_number == 6:
            number = random.choice([1, 2, 3])
        elif current_number == 7:
            number = random.choice([1, 2])
        elif current_number == 8:
            number = random.choice([1])
        else:
            number = random.choice([1])
    else:
        if current_number == 0:
            return random.choice([0])
        elif current_number == 1:
            number = random.choice([1])
        elif current_number == 2:
            number = random.choice([1, 2])
        elif current_number == 3:
            number = random.choice([1, 2, 3])
        elif current_number == 4:
            number = random.choice([1, 2, 3, 4])
        elif current_number == 5:
            number = random.choice([5])
        elif current_number == 6:
            number = random.choice([1, 5, 6])
        elif current_number == 7:
            number = random.choice([1, 5, 7])
        elif current_number == 8:
            number = random.choice([1, 2, 3, 5, 8])
        else:
            number = random.choice([1, 2, 3, 4, 5, 9])
    return number


def modify_number(number):
    new_number_str = ''
    operation = random.choice(['+', '-'])  # Tasodifiy amal

    number_str = str(number)
    index = 0

    if number_str[0] in ['1', '5']:
        operation = '+'
    if number_str[-1] == '0':
        operation = '+'

    while index < len(number_str):
        current_digit = int(number_str[index])
        next_number = get_number(current_digit, operation)

        if next_number is not None:
            new_number_str += str(next_number)

        index += 1

    return int(new_number_str), operation


def modify_number_parallel(number, digits):
    new_number_str = ''
    operation = random.choice(['+', '-'])

    number_str = str(number)

    if number_str[0] in ['1', '5']:
        operation = '+'
    if number_str[-1] == '0':
        operation = '+'

    current_digit = int(number_str[0])
    next_number = get_number(current_digit, operation)

    if next_number is not None:
        new_number_str += str(next_number)

    return int(new_number_str * digits), operation


def modify_number_tenner(number, digits):
    new_number_str = ''
    operation = random.choice(['+', '-'])

    number_str = str(number)

    if number_str[0] in ['1', '5']:
        operation = '+'

    current_digit = int(number_str[0])
    next_number = get_number(current_digit, operation)

    if next_number is not None:
        new_number_str += str(next_number)

    return int(new_number_str) * 10 ** (digits - 1), operation


def get_limit(digits):
    return 0, 10 ** digits


generate_count = 0


def generate_example(column, digits, method='mixed'):
    min_val, max_val = get_limit(digits)
    global generate_count
    while True:
        generate_count += 1
        first_number = random.randint(min_val, max_val)
        second_number, operation = modify_number(first_number)

        if method == 'parallel':
            first_number = int(str(random.randint(1, 10)) * digits)
            second_number, operation = modify_number_parallel(first_number, digits)

        elif method == 'tenner':
            first_number = int(random.randint(1, 10) * 10 ** (digits - 1))
            second_number, operation = modify_number_tenner(first_number, digits)

        if operation == '+':
            current_result = first_number + second_number
        else:
            current_result = first_number - second_number

        numbers = [first_number, second_number]
        operations = [operation]

        for _ in range(column - 2):
            next_number, operation = modify_number(current_result)
            if method == 'parallel':
                next_number, operation = modify_number_parallel(current_result, digits)
            elif method == 'tenner':
                next_number, operation = modify_number_tenner(current_result, digits)

            if operation == '+' and current_result + next_number < max_val and len(
                    str(next_number)) == digits and next_number != 0:
                operations.append(operation)
                numbers.append(next_number)
                current_result += next_number

            elif operation == '-' and current_result - next_number >= min_val and len(
                    str(next_number)) == digits and next_number != 0:
                operations.append(operation)
                numbers.append(next_number)
                current_result -= next_number

        if len(numbers) == column:
            expression = f'{numbers[0]}'
            for i in range(column - 1):
                expression += f' {operations[i]}{numbers[i + 1]}'
            return expression, current_result


def simple(column=5, count=1, digits=1, method='mixed'):
    """Foydalanuvchi tanlagan ustunlar soniga ko'ra misollarni yaratish."""
    response = {
        'examples': [],
        'results': []
    }
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(generate_example, column, digits, method) for _ in range(count)]  # method passed
        for future in as_completed(futures):
            example, result = future.result()
            if example is not None and result is not None:
                td = example.split(' ')
                response['examples'].append(td)
                response['results'].append(result)
    return response


if __name__ == '__main__':
    start = datetime.now()
    for _ in range(1):
        pprint.pprint(simple(column=5, count=3, digits=3, method='tenner'))
    for _ in range(1):
        pprint.pprint(simple(column=5, count=3, digits=3, method='parallel'))
    for _ in range(1):
        pprint.pprint(simple(column=5, count=3, digits=3, method='mixed'))
    end = datetime.now()
    print(f"Ijro vaqt: {end - start}")
    print(f"Urinishlar soni: {generate_count}")
