import random
import pprint
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed


def family_juftligi(requirement):
    """Ikkinchi sonni oila konsepsiyasiga muvofiq tanlaydi."""
    number = int(requirement[1])
    if number == 9:
        return 5
    elif number == 8:
        return random.choice([5, 6])
    elif number == 7:
        return random.choice([5, 6, 7])
    else:
        return random.choice([5, 6, 7, 8])


def get_number(current_result):
    if current_result % 10 == 0:
        number, operation = random.choice([
            (1, '+'), (2, '+'),
            (3, '+'), (4, '+'),
            (5, '+'), (6, '+'),
            (7, '+'), (8, '+'),
            (9, '+')
        ])
    elif current_result % 10 == 1:
        number, operation = random.choice([
            (1, '-'), (1, '+'), (2, '+'),
            (3, '+'),
            (5, '+')
        ])

    elif current_result % 10 == 2:
        number, operation = random.choice([
            (1, '-'), (1, '+'), (2, '-'), (2, '+'),
            (5, '+')
        ])

    elif current_result % 10 == 3:
        number, operation = random.choice([
            (1, '-'), (1, '+'), (2, '-'), (2, '+'),
            (3, '-'), (5, '+')
        ])

    elif current_result % 10 == 4:
        number, operation = random.choice([
            (1, '-'), (2, '-'),
            (3, '-'), (4, '-'), (5, '+')
        ])
    elif current_result % 10 == 5:
        number, operation = random.choice([
            (1, '+'), (2, '+'), (3, '+'),
            (5, '-'), (4, '+'), (5, '+')
        ])

    elif current_result % 10 == 6:
        number, operation = random.choice([
            (1, '-'), (1, '+'), (2, '+'), (3, '+'),
            (5, '-'), (6, '-')
        ])

    elif current_result % 10 == 7:
        number, operation = random.choice([
            (1, '-'), (1, '+'), (2, '+'), (2, '-'),
            (5, '-'), (7, '-')
        ])

    elif current_result % 10 == 8:
        number, operation = random.choice([
            (1, '-'), (1, '+'), (2, '-'), (3, '-'),
            (5, '-'), (8, '-')
        ])

    else:
        number, operation = random.choice([
            (1, '-'), (2, '-'), (3, '-'), (4, '-'),
            (5, '-'), (9, '-')
        ])
    return number, operation


generate_count = 0


def generate_example(column, requirement, digits=1):
    """Oila konsepsiyasi bilan numbers yaratadi va oraliq natijalarni tekshiradi."""
    min_val, max_val = 0, 100
    global generate_count
    while True:  # Ustunlar soni to'g'ri bo'lmaguncha takrorlaymiz
        generate_count += 1
        if requirement and digits == 1:
            second_number = int(requirement[1])
            first_number = family_juftligi(requirement)
        else:
            operation = random.choice(['-', '+'])
            second_number = random.choice([1, 2, 3, 4])
            first_number = family_juftligi(operation + str(second_number))

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


def family(column=5, requirement='+1', count=1):
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
        pprint.pprint(family(column=5, requirement='+8', count=10))
    end = datetime.now()
    print(f"Ijro vaqt: {end - start}")
    print(f"Urinishlar soni: {generate_count}")
