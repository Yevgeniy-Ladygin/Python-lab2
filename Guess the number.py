import random
import time

# 1. Уровни сложности
LEVELS = {
    1: {"name": "Новичок", "range_max": 50, "attempts": 8},
    2: {"name": "Детектив", "range_max": 100, "attempts": 7},
    3: {"name": "Мастер-сыщик", "range_max": 200, "attempts": 6}
}

# 3. Детективные сообщения
MESSAGES = {
    "too_low": [
        "'Код больше!' утверждает свидетель",
        "Шериф считает, что нужно искать 'большее' число",
        "Похоже, код 'больше', чем вы думали"
    ],
    "too_high": [
        "'Код меньше!' шепчет информатор",
        "Секретный агент уверен: код 'меньше' вашей догадки",
        "ФБР сообщает: искомое число 'меньше'"
    ],
    "win": "** Дело раскрыто! Детектив Джава взломал код за {attempts} попыток!",
    "lose": "** Злодей сбежал! Сейф остался заперт...",
    "game_title": "Дело детектива Питона"
}

# 2. Система подсказок (не менее 4 разных типов)
def get_hints(secret_number, max_range, hints_given):
    """Генерирует уникальную детективную подсказку."""
    available_hints = []

    # Тип 1: Четное/Нечетное (Parity)
    if 'parity' not in hints_given:
        parity_hint = "Число " + ("чётное!" if secret_number % 2 == 0 else "нечётное!")
        available_hints.append(("Чутьё детектива", parity_hint, 'parity'))

    # Тип 2: Делимость на 5 (Divisibility by 5)
    if 'divisible_5' not in hints_given:
        div_5_hint = "Число " + ("кратное 5!" if secret_number % 5 == 0 else "не кратное 5!")
        available_hints.append(("Чутьё детектива", div_5_hint, 'divisible_5'))

    # Тип 3: Делимость на 3 (Divisibility by 3)
    if 'divisible_3' not in hints_given:
        div_3_hint = "Число " + ("делится на 3!" if secret_number % 3 == 0 else "не делится на 3!")
        available_hints.append(("Свидетель сообщает", div_3_hint, 'divisible_3'))
        
    # Тип 4: Диапазон (Range) - Улика, что число в первой/второй половине диапазона
    mid_range = max_range // 2
    if 'range' not in hints_given:
        if secret_number <= mid_range:
            range_hint = f"Число {mid_range} или меньше!"
        else:
            range_hint = f"Число больше {mid_range}!"
        available_hints.append(("Найдена улика", range_hint, 'range'))
        
    # Тип 5: Делимость на 7 (Divisibility by 7) - Дополнительная подсказка
    if 'divisible_7' not in hints_given:
        div_7_hint = "Число " + ("делится на 7!" if secret_number % 7 == 0 else "не делится на 7!")
        available_hints.append(("Информатор шепчет", div_7_hint, 'divisible_7'))

    if available_hints:
        # Выбираем случайную уникальную подсказку
        source, hint, type_key = random.choice(available_hints)
        hints_given.add(type_key)
        return f"• {source}: '{hint}'", type_key
    else:
        return "• Подсказок больше нет! Последняя попытка!", 'none'

# 4. Статистика игр
game_stats = {
    "played": 0,
    "successful": 0,
    "total_attempts": 0,
    "total_time": 0.0
}

def display_stats():
    """Выводит статистику игр."""
    success_rate = (game_stats["successful"] / game_stats["played"] * 100) if game_stats["played"] > 0 else 0.0
    avg_attempts = (game_stats["total_attempts"] / game_stats["played"]) if game_stats["played"] > 0 else 0.0
    avg_time = (game_stats["total_time"] / game_stats["played"]) if game_stats["played"] > 0 else 0.0

    print("\n" + "="*20)
    print("Статистика дела:")
    print(f"Игр сыграно: {game_stats['played']}")
    print(f"Процент успеха: {success_rate:.1f}%")
    print(f"Среднее число попыток: {avg_attempts:.1f}")
    # Среднее время игры (Опционально)
    print(f"Среднее время: {avg_time:.2f} секунд")
    print("="*20)

def choose_level():
    """Позволяет пользователю выбрать уровень сложности."""
    print(f"\n{MESSAGES['game_title']}\nВыберите уровень сложности:")
    for key, value in LEVELS.items():
        print(f"{key}. {value['name']} (1-{value['range_max']}, {value['attempts']} попыток)")

    while True:
        choice = input("Выберите сложность (1-3): ")
        if choice in ['1', '2', '3']:
            return LEVELS[int(choice)]
        print("Введите корректный номер сложности (1, 2 или 3)!")

def get_guess(min_val, max_val):
    """Обрабатывает пользовательский ввод, включая проверку на корректность и диапазон."""
    while True:
        try:
            guess_input = input("Введите вашу догадку: ")
            guess = int(guess_input)
            if min_val <= guess <= max_val:
                return guess
            else:
                print(f"Число должно быть от {min_val} до {max_val}!")
        except ValueError:
            # Преобразование типов и обработка ошибок
            print("Введите корректное число!")

def play_game(level_config):
    """Основной цикл одной игры."""
    max_range = level_config["range_max"]
    max_attempts = level_config["attempts"]
    secret_number = random.randint(1, max_range)
    attempts_made = 0
    hints_given = set()
    game_start_time = time.time()
    
    # Сюжетное вступление
    print(f"\nДЕТЕКТИВ ДЖАВА ВЫХОДИТ НА СЛЕД")
    print(f"Злодей украл код от сейфа!")
    print(f"Это число от 1 до {max_range}.")
    print(f"У вас {max_attempts} попыток, чтобы раскрыть тайну...")

    while attempts_made < max_attempts:
        attempts_made += 1
        print(f"\nПопытка {attempts_made}/{max_attempts}")
        
        guess = get_guess(1, max_range)
        
        # Проверка ответа
        if guess == secret_number:
            game_time = time.time() - game_start_time
            print(MESSAGES['win'].format(attempts=attempts_made))
            print(f"Время: {game_time:.2f} секунд")
            return attempts_made, game_time, True
        
        # Сюжетные сообщения
        if guess < secret_number:
            message = random.choice(MESSAGES["too_low"])
        else: # guess > secret_number
            message = random.choice(MESSAGES["too_high"])
        
        print(message)
        
        # Система подсказок
        if attempts_made < max_attempts:
            # Выдаем подсказку только если это не последняя попытка
            hint_output, hint_type = get_hints(secret_number, max_range, hints_given)
            print(hint_output)

    # Поражение
    game_time = time.time() - game_start_time
    print("\n" + MESSAGES['lose'])
    return attempts_made, game_time, False


def main():
    """Главная функция программы с циклом 'Новое расследование'."""
    global game_stats
    
    continue_game = True
    while continue_game:
        # Выбор уровня и начало игры
        level_config = choose_level()
        attempts, game_time, won = play_game(level_config)

        # Обновление статистики
        game_stats["played"] += 1
        game_stats["total_attempts"] += attempts
        game_stats["total_time"] += game_time
        if won:
            game_stats["successful"] += 1
        
        # Вывод статистики
        display_stats()
        
        # Предложение начать новую игру
        while True:
            new_game_choice = input("Хотите взяться за новое дело? (y/n): ").lower()
            if new_game_choice in ['y', 'n']:
                continue_game = (new_game_choice == 'y')
                break
            print("Введите 'y' для нового дела или 'n' для выхода.")

    print("\n• Детектив Питон завершает расследование. Отличная работа, напарник!")

if __name__ == "__main__":
    main()
