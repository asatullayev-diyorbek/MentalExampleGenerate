import random
from datetime import datetime
from pprint import pprint
from concurrent.futures import ThreadPoolExecutor, as_completed
from .big_friend_requirements import generate_example as generate_example_requirements

# Katta do'st sonlar
large_friends = [(1, 9), (2, 8), (3, 7), (4, 6), (5, 5), (6, 4), (7, 3), (8, 2), (9, 1)]

def find_large_friend_pair(num):
    """Katta do'st juftligini topadi."""
    for pair in large_friends:
        if num in pair:
            return pair
    return None

def get_digit_range(digits):
    """Raqamlar uzunligi bo'yicha qiymatlar oraliqlarini qaytaradi."""
    if digits < 1 or digits > 5:
        raise ValueError("Raqamlar uzunligi 1 dan 5 gacha bo'lishi kerak.")

    # Raqamlar bo'yicha yangi oraliq
    if digits == 1:
        return 1, 9  # Faqat 1-9 gacha
    elif digits == 2:
        return 10, 99  # 10-99
    elif digits == 3:
        return 100, 999  # 100-999
    elif digits == 4:
        return 1000, 9999  # 1000-9999
    elif digits == 5:
        return 10000, 99999  # 10000-99999

def get_number(method, digits):
    """Random raqamni tanlaydi."""
    min_val, max_val = get_digit_range(digits)

    if method == "parallel":
        return random.choice([int(str(i) * digits) for i in range(1, 10)])  # 11, 22, ..., 99 or 11111, ..., 99999
    elif method == "mixed":
        return random.randint(min_val, max_val)  # Har qanday ixtiyoriy raqam
    elif method == "tenner":
        return random.choice([i * 10 ** (digits - 1) for i in range(1, 10)])  # 10, 20, ..., 90 or 10000, ..., 90000
    else:
        raise ValueError("Metod 'parallel', 'mixed' yoki 'tenner' bo'lishi kerak.")

def check_requirement(current_result, num, operation, requirement):
    """Requirement shartlarini tekshiradi va faqat 1 marta ishlatilishi kerak."""
    requirement_num = int(requirement[1])
    if operation == '+' and requirement[0] == '+' and num == requirement_num:
        if current_result < 10 and current_result + requirement_num >= 10:
            return True
    elif operation == '-' and requirement[0] == '-' and num == requirement_num:
        if current_result >= 10 and current_result - requirement_num <= 9:
            return True
    return False

def generate_large_friend_example(column, digits, requirement, method):
    """Katta do'st misollarini generatsiya qiladi."""
    min_val, max_val = get_digit_range(digits+1)  # max_val va min_val o'zgaruvchilarini aniqlash
    base_numbers = [get_number(method, digits) for _ in range(1, 10)]

    def process_operation(current_result):
        """Hisoblash va katta do'stni tekshirishni bajaradi."""
        operations = []
        numbers = [current_result]
        large_friend_found = False
        condition = 0

        if requirement and digits == 1:
            requirement_found = False
        else:
            requirement_found = True

        # Misol yaratish jarayoni
        while condition < column - 1:
            operation = random.choice(['+', '-'])
            num = get_number(method, digits)

            large_friend_pair = find_large_friend_pair(num % 10) if method != 'tenner' else find_large_friend_pair(
                num // 10 ** (digits - 1))
            if not requirement_found:
                requirement_found = check_requirement(current_result, num, operation, requirement)

            if not large_friend_pair:
                continue

            if operation == '+':
                if current_result + num <= max_val:
                    current_result += num
                    if current_result % 10 >= 10:  # Katta do'st qo'llanishi kerak
                        current_result += 10
                    numbers.append(num)
                    operations.append(operation)
                    large_friend_found = True
                else:
                    continue
            elif operation == '-':
                if current_result - num >= min_val:
                    current_result -= num
                    if current_result % 10 < 0:  # Katta do'st qo'llanishi kerak
                        current_result -= 10
                    numbers.append(num)
                    operations.append(operation)
                    large_friend_found = True
                else:
                    continue
            condition += 1

        if len(numbers) == column and large_friend_found and min_val <= current_result <= max_val and requirement_found:
            expression = f'{numbers[0]}'
            for i in range(column - 1):
                expression += f" {operations[i]}{numbers[i + 1]}"
            return expression, current_result
        return None, None

    # Misollarni generatsiya qilish
    while True:
        result = process_operation(get_number(method, digits))
        if result[0] is not None and result[1] is not None:
            return result

def large_friend(column=5, digits=1, count=10, requirement=None, method='mixed'):
    """Ko'p miqdordagi katta do'st misollarini generatsiya qiladi."""
    response = {
        'examples': [],
        'results': []
    }

    with ThreadPoolExecutor() as executor:
        if requirement and digits == 1:
            futures = [executor.submit(generate_example_requirements, column, requirement, digits) for _ in range(count)]
        else:
            futures = [executor.submit(generate_large_friend_example, column, digits, requirement, method) for _ in range(count)]
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
        print(_ + 1)
        pprint(large_friend(column=5, digits=2, method='parallel', requirement='+3'))
    end = datetime.now()
    print(f"Ijro vaqt: {end - start}")
