import random
import pprint
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from .family_requirements import generate_example as generate_example_requirements


def family_juftligi(son):
    """Ikkinchi sonni family konsepsiyasiga muvofiq tanlaydi."""
    if son == 6:
        return random.choice([5, 6, 7, 8])
    elif son == 7:
        return random.choice([5, 6, 7])
    elif son == 8:
        return random.choice([5, 6])
    elif son == 9:
        return 5
    return None

def get_digit_range(digits):
    """Raqamlar uzunligi bo'yicha qiymatlar oraliqlarini qaytaradi."""
    if digits < 1 or digits > 5:
        raise ValueError("Raqamlar uzunligi 1 dan 5 gacha bo'lishi kerak.")
    return 10**(digits-1), 10**digits - 1  # Maximal qiymatni -1 qilib qaytaramiz

def generate_example(column, requirement, digits, method='tenner'):
    """family konsepsiyasi bilan numbers yaratadi va oraliq natijalarni tekshiradi."""
    min_val, max_val = get_digit_range(digits)
    def get_number():
        """Random orqali sonni tanlaydi."""
        if method == "parallel":
            return int(str(random.randint(1, 9)) * digits)
        elif method=="mixed":
            return random.randint(min_val, max_val)
        elif method == 'tenner':
            return random.choice([i * 10**(digits - 1) for i in range(1, 10)])

    while True:  # Ustunlar soni to'g'ri bo'lmaguncha takrorlaymiz
        if requirement and digits == 1:
            birinchi_son = family_juftligi(son=int(requirement[1]))
            ikkinchi_son = int(requirement[1])
        else:
            son2 = random.choice([6, 7, 8, 9])  # family juftligi sifatida 2-chi son
            son1 = family_juftligi(son2)  # 1-chi son
            # get_digit_range(digits-1) ni unpack qilamiz
            min_val, max_val = get_digit_range(digits)
            birinchi_son = random.randint(min_val, max_val)//10 * 10 + son1
            ikkinchi_son = random.randint(min_val, max_val)//10 * 10 + son2
            if method == 'parallel':
                birinchi_son = int(str(son1) * digits)
                ikkinchi_son = int(str(son2) * digits)
            elif method == 'mixed':
                birinchi_son = random.randint(min_val, max_val)//10 * 10 + son1
                ikkinchi_son = random.randint(min_val, max_val)//10 * 10 + son2
            elif method == 'tenner':
                birinchi_son = son1 * 10 ** (digits - 1)
                ikkinchi_son = son2 * 10 ** (digits - 1)

        numbers = [str(birinchi_son), str(ikkinchi_son)]  # numbersning boshlanishi
        operations = ['+'] # Boshlang'ich amal
        natija = birinchi_son + ikkinchi_son  # Boshlang'ich natija

        # Qolgan ustunlar soni
        for _ in range(column - 2):  # -2 chunki 1-chi va 2-chi sonlar allaqachon qo'shilgan
            amal = random.choice(['+', '-'])  # Aralash amallar
            # get_digit_range(digits) ni unpack qilamiz
            min_val, max_val = get_digit_range(digits)
            if amal == '+':
                son = get_number()  # mos ravishda ixtiyoriy son
                operations.append(amal)
                numbers.append(str(son))
                natija += son  # Natijaga qo'shamiz
            else:  # Ayirish
                son = get_number()  # mos ravishda ixtiyoriy son
                if son <= natija:  # Natijadan katta bo'lmasligini ta'minlaymiz
                    operations.append(amal)
                    numbers.append(str(son))
                    natija -= son  # Natijadan ayiramiz

        if len(numbers) == column:  # misollar soni kerakli ustunlar soniga teng bo'lsa
            expression = f'{numbers[0]}'
            for i in range(column - 1):
                expression += f" {operations[i]}{numbers[i + 1]}"
            return expression, natija

def family(column=5, digits=1, count=1, method='mixed'):
    """Foydalanuvchi tanlagan ustunlar soniga ko'ra misollarni yaratish."""
    response = {
        'examples': [],
        'results': []
    }
    with ThreadPoolExecutor() as executor:
        if requirement and digits == 1:
            futures = [executor.submit(generate_example_requirements, column, requirement, digits) for _ in range(count)]
        else:
            futures = [executor.submit(generate_example, column, requirement, digits, method) for _ in range(count)]
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
        pprint.pprint(family(column=5, requirement='+6', digits=1, count=10, method='tenner'))
    end = datetime.now()
    print(f"Ijro vaqt: {end - start}")
