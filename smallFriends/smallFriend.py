import random
from pprint import pprint

from django.views.decorators.http import condition

# Kichik do'st sonlar
small_friends = [(1, 4), (2, 3), (3, 2), (4, 1)]

def find_small_friend_pair(num):
    for pair in small_friends:
        if num in pair:
            return pair
    return None

def generate_example(column, requirement):
    while True:
        current_result = random.randint(1, 9)
        numbers = [current_result]
        operations = []
        small_friend_found = False

        for _ in range(column-1):
            operation = random.choice(['+', '-'])
            num = random.randint(1, 4)

            small_friend_pair = find_small_friend_pair(num)
            if not small_friend_pair:
                continue

            if operation == '+':
                if current_result + num <= 9:
                    current_result += num
                    numbers.append(num)
                    operations.append(operation)
                    if current_result in small_friend_pair:
                        small_friend_found = True
                else:
                    continue
            elif operation == '-':
                if current_result - num >= 0:
                    current_result -= num
                    numbers.append(num)
                    operations.append(operation)
                    if current_result in small_friend_pair:
                        small_friend_found = True
                else:
                    continue

        if len(numbers) == column and small_friend_found and 0 <= current_result <= 9:
            expression = f"{numbers[0]}"
            for i in range(column-1):
                expression += f" {operations[i]}{numbers[i + 1]}"
            if not requirement in expression:
                continue
            return expression, current_result


def small_friend(column=5, size=1, count=10, requirement=' '):
    response = {
        'examples': [],
        'results': []
    }

    for i in range(count):
        example, result = generate_example(column=column, requirement=requirement)
        td = example.split(' ')
        response['examples'].append(td)
        response['results'].append(result)

    return response


if __name__ == '__main__':
    pprint(small_friend())