import random
import pprint
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed


def small_friend_juftligi(requirement):
    """Ikkinchi sonni kichik do'st konsepsiyasiga muvofiq tanlaydi."""
    operation, number = requirement[0], int(requirement[1])
    if operation == '+':
        if number == 4:
            return random.choice([1, 2, 3, 4])
        elif number == 3:
            return random.choice([2, 3, 4])
        elif number == 2:
            return random.choice([3, 4])
        else:
            return 4
    else:
        if number == 4:
            return random.choice([5, 6, 7, 8])
        elif number == 3:
            return random.choice([5, 6, 7])
        elif number == 2:
            return random.choice([5, 6])
        else:
            return 5


def get_number(current_result):
    if current_result == 0:
        number, operation = random.choice([
            (1, '+'), (2, '+'),
            (3, '+'), (4, '+'),
            (5, '+'), (6, '+'),
            (7, '+'), (8, '+'),
            (9, '+')
        ])
    elif current_result == 1:
        number, operation = random.choice([
            (1, '-'), (1, '+'), (2, '+'),
            (3, '+'),
            (5, '+'), (6, '+'),
            (7, '+'), (8, '+')
        ])

    elif current_result == 2:
        number, operation = random.choice([
            (1, '-'), (1, '+'), (2, '-'), (2, '+'),
            (5, '+'), (6, '+'),
            (7, '+')
        ])

    elif current_result == 3:
        number, operation = random.choice([
            (1, '-'), (1, '+'), (2, '-'), (2, '+'),
            (3, '-'), (5, '+'), (6, '+')
        ])

    elif current_result == 4:
        number, operation = random.choice([
            (1, '-'), (2, '-'),
            (3, '-'), (4, '-'), (5, '+'), (6, '+'),
            (7, '+'), (8, '+')
        ])
    elif current_result == 5:
        number, operation = random.choice([
            (1, '+'), (2, '+'), (3, '+'),
            (5, '-'), (4, '+')
        ])

    elif current_result == 6:
        number, operation = random.choice([
            (1, '-'), (1, '+'), (2, '+'), (3, '+'),
            (5, '-'), (6, '-')
        ])

    elif current_result == 7:
        number, operation = random.choice([
            (1, '-'), (1, '+'), (2, '+'), (2, '-'),
            (5, '-'), (6, '-'), (7, '-')
        ])

    elif current_result == 8:
        number, operation = random.choice([
            (1, '-'), (1, '+'), (2, '-'), (3, '-'),
            (5, '-'), (6, '-'), (7, '-'), (8, '-')
        ])

    else:
        number, operation = random.choice([
            (1, '-'), (2, '-'), (3, '-'), (4, '-'),
            (5, '-'), (6, '-'), (7, '-'), (8, '-'), (9, '-')
        ])
    return number, operation


generate_count = 0


def generate_example(column, requirement, digits=1):
    """Kichik do'st konsepsiyasi bilan numbers yaratadi va oraliq natijalarni tekshiradi."""
    min_val, max_val = 0, 9
    global generate_count
    while True:  # Ustunlar soni to'g'ri bo'lmaguncha takrorlaymiz
        generate_count += 1
        if requirement and digits == 1:
            second_number = int(requirement[1])
            first_number = small_friend_juftligi(requirement)
        else:
            operation = random.choice(['-', '+'])
            second_number = random.choice([1, 2, 3, 4])
            first_number = small_friend_juftligi(operation + str(second_number))

        numbers = [str(first_number), str(second_number)]

        if requirement[0] == '+':
            operations = ['+']
            current_result = first_number + second_number
        elif requirement[0] == '-':
            operations = ['-']
            current_result = first_number - second_number

        for _ in range(column - 2):
            number, operation = get_number(current_result)

            if operation == '+' and current_result + number <= max_val:
                operations.append(operation)
                numbers.append(str(number))
                current_result += number
            elif operation == '-' and current_result - number >= min_val:
                operations.append(operation)
                numbers.append(number)
                current_result -= number

        if len(numbers) == column:
            expression = f'{numbers[0]}'
            for i in range(column - 1):
                expression += f' {operations[i]}{numbers[i + 1]}'
            return expression, current_result


def small_friend(column=5, requirement='+1', count=1):
    """Foydalanuvchi tanlagan ustunlar soniga ko'ra misollarni yaratish."""
    response = {
        'examples': [],
        'results': []
    }
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(generate_example, column, requirement) for _ in range(count)]
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
        pprint.pprint(small_friend(column=5, requirement='+2', count=10))
    end = datetime.now()
    print(f"Ijro vaqt: {end - start}")
    print(f"Urinishlar soni: {generate_count}")
