"""
1. Создать новый проект "Игра лото""
2. Правила игры можно посмотреть тут:  
    https://github.com/dmitry-vs/python-loto-game (Если не получается перейти по ссылке, скопируйте и вставьте в строку браузера самостоятельно)
3. Написать игру лото.

    Возможные подходы к решению задачи:
        1) Проектирование на основании предметной области. Подумать какие объекты есть в игре и какие из них можно перенести в программу.
        Для них создать классы с соответствующими свойствами и методами. Проверить каждый класс отдельно. Написать программу с помощью этих классов;
    
        2) Метод грубой силы + рефакторинг. Написать программу как получиться. После этого с помощью принципа DRY убрать дублирование в коде;
    
        3) Процедурное программирование.

4. Минимальные требования: 2 игрока - человек играет с компьютером;
5. (Дополнительно *) возможность выбирать тип обоих игроков (компьютер или человек) таки образом чтобы можно было играть: компьютер - человек, человек - человек, компьютер - компьютер;
6. (Дополнительно *) возможность играть для любого количества игроков от 2 и более;
7. Выложите проект на github;
8. Можно сдать задание в виде pull request.
"""

import random
import threading
import queue

# Создадим класс для игровой карточки
class Card:
    def __init__(self):
        self.rows = 3
        self.cols = 9
        self.numbers_per_row = 5
        self.card = self.generate_card()

    def generate_card(self):
        card = [[' ' for _ in range(self.cols)] for _ in range(self.rows)]
        numbers = [set(range(1, 10))] + [set(range(10*i, 10*i+10)) for i in range(1, 8)] + [set(range(80, 91))]
        
        for row in range(self.rows):
            cols = random.sample(range(self.cols), self.numbers_per_row)
            for col in cols:
                if numbers[col]:
                    number = random.choice(list(numbers[col]))
                    card[row][col] = number
                    numbers[col].remove(number)

        return card

    def mark_number(self, number):
        for row in self.card:
            if number in row:
                index = row.index(number)
                row[index] = 'X'
                return True
        return False

    def is_complete(self):
        return all(row.count('X') == self.numbers_per_row for row in self.card)

    def __str__(self):
        card_str = "--------------------------\n"
        card_str += '\n'.join(' '.join(f'{num:2}' if isinstance(num, int) else ' X' if num == 'X' else '  ' for num in row) for row in self.card)
        card_str += "\n--------------------------"
        return card_str

# Создадим класс для бочонка
class Barrel:
    def __init__(self, number):
        if number < 1 or number > 90:
            raise ValueError("Номер бочонка должен быть от 1 до 90")
        self.number = number

    def __str__(self):
        return str(self.number)

# Создадим класс для игрока
class Player:
    def __init__(self, name, num_cards):
        self.name = name
        self.cards = [Card() for _ in range(num_cards)]

class HumanPlayer(Player):
    def make_move(self, barrel, time_limit):
        print(f"У вас есть {time_limit} секунд, чтобы решить, зачеркнуть ли цифру {barrel}.")
        q = queue.Queue()
        
        def input_thread():
            q.put(input("Зачеркнуть цифру? (д/н): "))
        
        thread = threading.Thread(target=input_thread)
        thread.daemon = True
        thread.start()
        
        try:
            choice = q.get(timeout=time_limit)
        except queue.Empty:
            print("Время вышло! Вы проиграли.")
            return False
        
        if choice.lower() not in ['д', 'н']:
            print("Некорректный ввод. Вы проиграли.")
            return False
        
        if choice.lower() == 'д':
            marked = False
            for card in self.cards:
                if card.mark_number(barrel.number):
                    marked = True
            if not marked:
                print("Этого числа нет на ваших карточках. Вы проиграли!")
                return False
            return True
        else:
            for card in self.cards:
                if card.mark_number(barrel.number):
                    print("Это число есть на одной из ваших карточек. Вы проиграли!")
                    return False
            return True

class ComputerPlayer(Player):
    def make_move(self, barrel):
        for card in self.cards:
            card.mark_number(barrel.number)
        return True

# Создадим класс для хода игры
class Game:
    def __init__(self):
        self.players = self.setup_players()
        self.barrels = list(range(1, 91))
        random.shuffle(self.barrels)
        self.time_limit = self.set_time_limit()

    def setup_players(self):
        players = []
        player_type = input("Выберите тип игры (1 - против компьютера, 2 - два игрока): ")
        num_cards = int(input("Сколько карточек выдать каждому игроку (1-3): "))
        
        players.append(HumanPlayer("Игрок 1", num_cards))
        if player_type == '1':
            players.append(ComputerPlayer("Компьютер", num_cards))
        else:
            players.append(HumanPlayer("Игрок 2", num_cards))
        
        return players

    def set_time_limit(self):
        return int(input("Установите ограничение времени на ход (в секундах): "))

    def start_game(self):
        while self.barrels:
            if self.next_turn():
                break
            if self.check_winner():
                break

    def next_turn(self):
        barrel = Barrel(self.barrels.pop())
        
        for player in self.players:
            print(f"\n-----Карточки {player.name}-----")
            for card in player.cards:
                print(card)
            print()
        
        print(f"\nВыпал бочонок с номером {barrel}.")
        
        for player in self.players:
            print(f"\nХод игрока: {player.name}")
            if isinstance(player, HumanPlayer):
                if not player.make_move(barrel, self.time_limit):
                    print(f"{player.name} проиграл! Игра окончена.")
                    return True
            else:
                player.make_move(barrel)
        
        return False

    def check_winner(self):
        for player in self.players:
            if all(card.is_complete() for card in player.cards):
                print(f"{player.name} выиграл! Игра окончена.")
                return True
        return False

if __name__ == "__main__":
    game = Game()
    game.start_game()

"""
1. Класс Game:

    Отвечает за общую логику игры
    Инициализирует игроков и бочонки
    Управляет ходами игры и проверяет победителя
    
2. Класс Player:

    Базовый класс для всех игроков
    Хранит имя игрока и его карточки

3. Класс HumanPlayer (наследуется от Player):

    Представляет игрока-человека
    Обрабатывает ввод пользователя с ограничением по времени

4. Класс ComputerPlayer (наследуется от Player):

    Представляет игрока-компьютера
    Автоматически делает ходы

5. Класс Card:

    Представляет карточку лото
    Генерирует числа на карточке
    Отмечает выпавшие числа

Класс Barrel:

    Представляет бочонок с номером
.
"""