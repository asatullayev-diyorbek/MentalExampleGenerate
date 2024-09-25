import random
from datetime import datetime
from pprint import pprint
from concurrent.futures import ThreadPoolExecutor, as_completed

# Kichik do'st sonlar
small_friends = [(1, 4), (2, 3), (3, 2), (4, 1)]

def find_small_friend_pair(num):
    """Kichik do'st juftligini topadi."""
    for pair in small_friends:
        if num in pair:
            return pair
    return None

def get_digit_range(digits):
    """Raqamlar uzunligi bo'yicha qiymatlar oraliqlarini qaytaradi."""
    if digits < 1 or digits > 5:
        raise ValueError("Raqamlar uzunligi 1 dan 5 gacha bo'lishi kerak.")
    return 10**(digits-1), 10**digits - 1

def generate_example(column, digits, requirement, method):
    """Misollarni generatsiya qiladi."""
    min_val, max_val = get_digit_range(digits)
    base_numbers = [i * 10**(digits - 1) for i in range(1, 10)]
    if method == "parallel":
        base_numbers = [int(str(i) * digits) for i in range(1, 10)]

    def get_number():
        """Random raqamni tanlaydi."""
        if method == "parallel":
            return random.choice(base_numbers)
        elif method == "mixed":
            return random.randint(min_val, max_val)
        elif method == "tenner":
            return random.choice([i * 10**(digits - 1) for i in range(1, 10)])
        else:
            raise ValueError("Metod 'parallel', 'mixed' yoki 'tenner' bo'lishi kerak.")

    def check_requirement(current_result, operation, num, requirement):
        """Requirement shartini tekshiradi."""
        if digits == 1 and requirement:
            required_num = int(requirement[1])  # Talab qilingan oxirgi raqam
            if operation == '+' and requirement[0] == '+':
                # Birinchi raqam 5 dan kichik bo'lishi kerak
                if current_result < 5 and current_result + num >= 5 and num == required_num:
                    return True
                else:
                    return False
            elif operation == '-' and requirement[0] == '-':
                # Birinchi raqam 5 yoki undan katta bo'lishi kerak
                if current_result >= 5 and current_result - num <= 4 and num == required_num:
                    return True
                else:
                    return False
        return True


    def process_operation(current_result):
        """Hisoblash va kichik do'stni tekshirishni bajaradi."""
        operations = []
        numbers = [current_result]
        small_friend_found = False

        condition = 0
        is_requirement_met = False

        while condition < column - 1:
            operation = random.choice(['+', '-'])
            num = get_number()

            if not is_requirement_met:
                is_requirement_met = check_requirement(current_result, operation, num, requirement)

            small_friend_pair = find_small_friend_pair(num % 10) if method != 'tenner' else find_small_friend_pair(num // 10**(digits - 1))

            if not small_friend_pair:
                continue

            if operation == '+':
                if current_result + num <= max_val:
                    current_result += num
                    numbers.append(num)
                    operations.append(operation)
                    if (method == 'tenner' and current_result // 10**(digits - 1) in small_friend_pair) or \
                       (method != 'tenner' and current_result % 10 in small_friend_pair):
                        small_friend_found = True
                else:
                    continue
            elif operation == '-':
                if current_result - num >= min_val:
                    current_result -= num
                    numbers.append(num)
                    operations.append(operation)
                    if (method == 'tenner' and current_result // 10**(digits - 1) in small_friend_pair) or \
                       (method != 'tenner' and current_result % 10 in small_friend_pair):
                        small_friend_found = True
                else:
                    continue

            condition += 1

        if len(numbers) == column and small_friend_found and min_val <= current_result <= max_val and is_requirement_met:
            expression = f'{numbers[0]}'
            for i in range(column - 1):
                expression += f" {operations[i]}{numbers[i + 1]}"
            return expression, current_result
        return None, None

    # Misollarni generatsiya qilish
    while True:
        result = process_operation(get_number())
        if result[0] is not None and result[1] is not None:
            return result

def small_friend(column=5, digits=1, count=10, requirement=' ', method='mixed'):
    """Ko'p miqdordagi kichik do'st misollarini generatsiya qiladi."""
    response = {
        'examples': [],
        'results': []
    }

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(generate_example, column, digits, requirement, method) for _ in range(count)]
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
        pprint(small_friend(column=5, digits=1, method='mixed', requirement='-3'))
    end = datetime.now()
    print(f"Ijro vaqt: {end - start}")
