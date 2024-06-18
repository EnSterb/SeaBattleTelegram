import os
from random import randrange
from random import choice
import telebot
from telebot import types
import photo


class Cell:
    empty_cell = ' '
    ship_cell = 's'
    destroyed_ship = 'd'
    damaged_ship = 'dam'
    miss_cell = 'm'


class FieldPart:
    main = 'map'
    enemy_map = 'enemy_map'
    weight = 'weight'


class Field:
    def __init__(self, size):
        self.size = size
        self.map = [[Cell.empty_cell for _ in range(size)] for _ in range(size)]
        self.enemy_map = [[Cell.empty_cell for _ in range(size)] for _ in range(size)]
        self.weight = [[1 for _ in range(size)] for _ in range(size)]

    def get_part(self, item):
        if item == FieldPart.main:
            return self.map
        if item == FieldPart.enemy_map:
            return self.enemy_map
        if item == FieldPart.weight:
            return self.weight

    def draw_game_field(self, item, number):
        global id
        global flag_bot
        field = self.get_part(item)
        pre_result = []
        for x in range(-1, self.size):
            for y in range(-1, self.size):
                if x == -1 and y == -1:
                    pre_result.append(' ')
                    continue
                if x == -1 and y >= 0:
                    pre_result.append(y + 1)
                    continue
                if x >= 0 and y == -1:
                    pre_result.append(Game.letters[x])
                    continue
                pre_result.append(str(field[x][y]))
        result = [pre_result[i:i + 11] for i in range(0, len(pre_result), 11)]
        photo.draw_image(result, flag_bot)
        if flag_bot == 1:
            photo.draw_result(number, bot_name, game.current_player.name)
        else:
            photo.draw_result(number, game.next_player.name, game.current_player.name)
        if number == 2:
            res_photo = open('result.png', 'rb')
            bot.send_photo(id, res_photo)

    def correct_ship_place(self, ship, item):

        field = self.get_part(item)

        if ship.x + ship.height - 1 >= self.size or ship.x < 0 or ship.y + ship.width - 1 >= self.size or ship.y < 0:
            return False
        x, y, width, height = ship.x, ship.y, ship.width, ship.height

        for c_x in range(x, x + height):
            for c_y in range(y, y + width):
                if str(field[c_x][c_y]) == Cell.miss_cell:
                    return False

        for c_x in range(x - 1, x + height + 1):
            for c_y in range(y - 1, y + width + 1):
                if c_x < 0 or c_x >= len(field) or c_y < 0 or c_y >= len(field):
                    continue
                if str(field[c_x][c_y]) in (Cell.ship_cell, Cell.destroyed_ship):
                    return False
        return True

    def destroy(self, ship, item):
        field = self.get_part(item)

        x, y, width, height = ship.x, ship.y, ship.width, ship.height

        for c_x in range(x - 1, x + height + 1):
            for c_y in range(y - 1, y + width + 1):
                if c_x < 0 or c_x >= len(field) or c_y < 0 or c_y >= len(field):
                    continue
                field[c_x][c_y] = Cell.miss_cell
        for c_x in range(x, x + height):
            for c_y in range(y, y + width):
                field[c_x][c_y] = Cell.destroyed_ship

    def add_ship(self, ship, item):
        field = self.get_part(item)
        x, y, width, height = ship.x, ship.y, ship.width, ship.height

        for c_x in range(x, x + height):
            for c_y in range(y, y + width):
                field[c_x][c_y] = ship

    def get_max_weight(self):
        weights = {}
        max_weight = 0
        for x in range(self.size):
            for y in range(self.size):
                if self.weight[x][y] > max_weight:
                    max_weight = self.weight[x][y]
                weights.setdefault(self.weight[x][y], []).append((x, y))
        return weights[max_weight]

    def recalculate_weight(self, ships):
        self.weight = [[1 for _ in range(self.size)] for _ in range(self.size)]
        for x in range(self.size):
            for y in range(self.size):
                if self.enemy_map[x][y] == Cell.damaged_ship:
                    self.weight[x][y] = 0
                    if x - 1 >= 0:
                        if y - 1 >= 0:
                            self.weight[x - 1][y - 1] = 0
                        self.weight[x - 1][y] *= 10
                        if y + 1 < self.size:
                            self.weight[x - 1][y + 1] = 0
                    if y - 1 >= 0:
                        self.weight[x][y - 1] *= 10
                    if y + 1 < self.size:
                        self.weight[x][y + 1] *= 10
                    if x + 1 < self.size:
                        if y - 1 >= 0:
                            self.weight[x + 1][y - 1] = 0
                        self.weight[x + 1][y] *= 10
                        if y + 1 < self.size:
                            self.weight[x + 1][y + 1] = 0
        for ship_type in ships:
            ship = Ship(ship_type, 1, 1, 0)
            for x in range(self.size):
                for y in range(self.size):
                    if self.enemy_map[x][y] in (Cell.destroyed_ship, Cell.damaged_ship, Cell.miss_cell) or \
                            self.weight[x][y] == 0:
                        self.weight[x][y] = 0
                        continue
                    for rotation in range(0, 4):
                        ship.position(x, y, rotation)
                        if self.correct_ship_place(ship, FieldPart.enemy_map):
                            self.weight[x][y] += 1


class Game(object):
    letters = tuple([chr(x) for x in range(ord('A'), ord('J') + 1)])
    ships_rules = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]
    field_size = len(letters)

    def __init__(self):
        self.players = []
        self.current_player = None
        self.next_player = None
        self.status = 'prepare'

    def start_game(self):
        self.current_player = self.players[0]
        self.next_player = self.players[1]

    def check_status(self):
        if self.status == 'prepare' and len(self.players) >= 2:
            self.status = 'in game'
            self.start_game()
            return True
        if self.status == 'in game' and len(self.next_player.ships) == 0:
            self.status = 'game over'
            return True

    def add_player(self, player):
        player.field = Field(Game.field_size)
        player.enemy_ships = list(Game.ships_rules)
        self.ships_setup(player)
        player.field.recalculate_weight(player.enemy_ships)
        self.players.append(player)

    def ships_setup(self, player):
        for ship_size in Game.ships_rules:
            retry_count = 30
            ship = Ship(ship_size, 0, 0, 0)
            while True:
                Game.clear_screen()
                if player.auto_ship_setup is not True:
                    player.field.draw_game_field(FieldPart.main)
                    player.message.append(f'Куда поставить {ship_size}-мерный корабль')
                    for i in player.message:
                        print(i)
                else:
                    print(f'{player.name},расставляем корабли')
                player.message.clear()
                x, y, r = player.get_input('ship_setup')
                if x + y + r == 0:
                    continue
                ship.position(x, y, r)
                if player.field.correct_ship_place(ship, FieldPart.main):
                    player.field.add_ship(ship, FieldPart.main)
                    player.ships.append(ship)
                    break
                player.message.append('Неправильная позиция!')
                retry_count -= 1
                if retry_count < 0:
                    player.field.map = [[Cell.empty_cell for _ in range(Game.field_size)] for _ in
                                        range(Game.field_size)]
                    player.ships = []
                    self.ships_setup(player)
                    return True

    def draw(self):
        for message in self.current_player.message:
            ...
            # print(message)
        return self.current_player.message

    def switch_players(self):
        self.current_player, self.next_player = self.next_player, self.current_player

    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')


class Ship:
    def __init__(self, size, x, y, rotation):
        self.size = size
        self.hp = size
        self.x = x
        self.y = y
        self.rotation = rotation
        self.set_rotation(rotation)

    def __str__(self):
        return Cell.ship_cell

    def position(self, x, y, phi):
        self.x = x
        self.y = y
        self.set_rotation(phi)

    def set_rotation(self, phi):
        self.rotation = phi
        if self.rotation == 0:
            self.width = self.size
            self.height = 1
        elif self.rotation == 1:
            self.width = 1
            self.height = self.size
        elif self.rotation == 2:
            self.y = self.y - self.size + 1
            self.width = self.size
            self.height = 1
        elif self.rotation == 3:
            self.x = self.x - self.size + 1
            self.width = 1
            self.height = self.size


class Player(object):
    def __init__(self, name, is_ai, skill, auto_ship):
        self.name = name
        self.is_ai = is_ai
        self.auto_ship_setup = auto_ship
        self.skill = skill
        self.message = []
        self.ships = []
        self.enemy_ships = []
        self.field = None

    def get_input(self, input_type):
        global user_input
        if input_type == 'ship_setup':
            if self.is_ai or self.auto_ship_setup:
                user_input = str(choice(Game.letters)) + str(randrange(0, self.field.size)) + choice(['H', 'V'])
            else:
                user_input = user_input.upper().replace(" ", '')

            if len(user_input) < 3:
                return 0, 0, 0
            x, y, r = user_input[0], user_input[1:-1], user_input[-1]
            if x not in Game.letters or not y.isdigit() or int(y) not in range(1, Game.field_size + 1) or r not in (
                    "H", "V"):
                self.message.append('Приказ непонятен, ошибка формата данных')
                return 0, 0, 0
            return Game.letters.index(x), int(y) - 1, 0 if r == 'H' else 1
        if input_type == 'shot':
            if self.is_ai:
                if self.skill == 1:
                    x, y = choice(self.field.get_max_weight())
                if self.skill == 0:
                    x, y = randrange(0, self.field.size), randrange(0, self.field.size)
            else:
                user_input = user_input.upper().replace(" ", '')
                x, y = user_input[0].upper(), user_input[1:]
                if x not in Game.letters or not y.isdigit() or int(y) not in range(1, Game.field_size + 1):
                    self.message.append('Приказ непонятен, ошибка формата данных')
                    return 500, 0
                x = Game.letters.index(x)
                y = int(y) - 1
            return x, y

    def make_shot(self, target_player):
        x, y = self.get_input('shot')
        if x + y == 500 or self.field.enemy_map[x][y] != Cell.empty_cell:
            return 'retry'
        shot_result = target_player.receive_shot((x, y))
        if shot_result == 'miss':
            self.field.enemy_map[x][y] = Cell.miss_cell
        if shot_result == 'get':
            self.field.enemy_map[x][y] = Cell.damaged_ship
        if type(shot_result) == Ship:
            destroyed_ship = shot_result
            self.field.destroy(destroyed_ship, FieldPart.enemy_map)
            self.enemy_ships.remove(destroyed_ship.size)
            shot_result = 'kill'
        self.field.recalculate_weight(self.enemy_ships)
        return shot_result

    def receive_shot(self, shot):
        x, y = shot
        if type(self.field.map[x][y]) == Ship:
            ship = self.field.map[x][y]
            ship.hp -= 1
            if ship.hp <= 0:
                self.field.destroy(ship, FieldPart.main)
                self.ships.remove(ship)
                return ship
            self.field.map[x][y] = Cell.damaged_ship
            return 'get'
        else:
            self.field.map[x][y] = Cell.miss_cell
            return 'miss'


bot_name = ''
name = ''
user_input = ''

bot = telebot.TeleBot("6361479798:AAE4-jsSSAYE0YUHmfJA24bGFnCOsoZalao")


@bot.message_handler(commands=['start'])
def handle_start(message):
    global name
    global markup
    bot.reply_to(message, "Привет, я бот морской бой!")
    markup = types.ReplyKeyboardMarkup()
    game_button = types.InlineKeyboardButton('/new_game')
    markup.add(game_button)
    bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=markup)


def give_bot_name(message):
    global game
    global players
    global bot_name
    global ai
    bot_name = message.text
    players = []
    players.append(Player(name=f'{name}', is_ai=False, auto_ship=True, skill=1))
    players.append(Player(name=f'{bot_name}', is_ai=ai, auto_ship=True, skill=1))
    # создаем саму игру
    bot.send_message(message.chat.id, 'Основные правила:')
    bot.send_message(message.chat.id, 'Поле противника справа')
    bot.send_message(message.chat.id, 'Писать английскими буквами')
    bot.send_message(message.chat.id, 'Чтобы начать новую игру нажмите "/new_game"')
    bot.send_message(message.chat.id, 'Подождите, идёт расстановка кораблей')

    game = Game()
    game.check_status()
    game.add_player(players.pop(0))
    game.add_player(players.pop(0))
    bot.send_message(message.chat.id, 'Игра началась!')
    bot.send_message(message.chat.id, 'Вы ходите первым')
    bot.send_message(message.chat.id, 'Для первого хода необходимо написать команду "/first_move"')
    game.start_game()


players = []
game = Game()
field = Field(10)
flag = False


@bot.message_handler(commands=['new_game'])
def start_func(message):
    global id
    global game
    global players
    global flag
    global name

    id = message.chat.id
    name = message.from_user.first_name
    flag = True
    send = bot.send_message(id, 'Будете играть против бота (Да/Нет)?')
    bot.register_next_step_handler(send, ai_check)


def ai_check(message):
    global ai
    global flag_bot
    text = message.text
    text = text.upper().replace(' ', '')
    if text == 'ДА' or text == 'YES':
        ai = True
        flag_bot = 1
        sent = bot.send_message(id, f'{name}, дайте имя противнику')
        bot.register_next_step_handler(sent, give_bot_name)
    elif text == 'НЕТ' or text == 'NO':
        ai = False
        flag_bot = 2
        sent = bot.send_message(id, f'{name}, дайте имя противнику')
        bot.register_next_step_handler(sent, give_bot_name)
    else:
        send = bot.send_message(id, 'Будете играть против бота (Да/Нет)?')
        bot.register_next_step_handler(send, ai_check)


@bot.message_handler(commands=['first_move'])
def func(message):
    global flag
    global id
    if flag:
        if not game.current_player.is_ai:
            game.check_status()
            if game.status != 'game over':
                Game.clear_screen()
                sa = game.draw()
                game.current_player.field.draw_game_field(FieldPart.main, 1)
                game.current_player.field.draw_game_field(FieldPart.enemy_map, 2)
                for a in sa:
                    bot.send_message(message.chat.id, a)
                game.current_player.message.clear()
                sent = bot.send_message(message.chat.id, f'Ваш ход, {game.current_player.name}\nСтреляйте!')
                bot.register_next_step_handler(sent, call)

        while game.current_player.is_ai:
            game.check_status()
            if game.status == 'game over':
                break
            bot.send_message(message.chat.id, f'ход {bot_name}')
            # В основной части игры мы очищаем экран добавляем сообщение для текущего игрока и отрисовываем игру
            # Очищаем список сообщений для игрока. В следующий ход он уже получит новый список сообщений
            game.current_player.message.clear()
            shot_result = game.current_player.make_shot(game.next_player)

            if shot_result == 'miss':
                game.switch_players()
                bot.send_message(message.chat.id, f'{bot_name} промазал')
                func(message)
                continue

            if shot_result == 'get':
                bot.send_message(message.chat.id, f'{bot_name} попал')

            if shot_result == 'retry':
                continue

            if shot_result == 'kill':
                bot.send_message(message.chat.id, f'{bot_name} убил ваш корабль')
                continue

        game.check_status()
        if game.status == 'game over':
            global flag_bot
            flag_bot = 1
            Game.clear_screen()
            id = message.chat.id
            if game.current_player.is_ai:
                game.next_player.field.draw_game_field(FieldPart.main, 1)
                game.current_player.field.draw_game_field(FieldPart.main, 2)
            else:
                game.current_player.field.draw_game_field(FieldPart.main, 1)
                game.next_player.field.draw_game_field(FieldPart.main, 2)
            bot.send_message(message.chat.id, f'Это был последний корабль, {game.next_player.name}')
            bot.send_message(message.chat.id, f'{game.current_player.name} умничка -  выиграл матч! Поздравляем!')
            bot.send_message(message.chat.id, 'Чтобы начать новую игру нажмите "/new_game"')
            flag = False


def call(mess):
    global user_input
    user_input = mess.text
    shot_result = game.current_player.make_shot(game.next_player)

    if shot_result == 'miss':
        bot.send_message(mess.chat.id, f'{game.current_player.name} промахнулся!')
        game.switch_players()
        func(mess)

    if shot_result == 'get':
        bot.send_message(mess.chat.id, 'Отличный выстрел, продолжайте!')
        func(mess)

    if shot_result == 'retry':
        if mess.text == '/new_game':
            start_func(mess)
        else:
            bot.send_message(mess.chat.id, 'Попробуйте ещё раз!')
            func(mess)

    if shot_result == 'kill':
        bot.send_message(mess.chat.id, f'Корабль {game.next_player.name} уничтожен')
        func(mess)


if __name__ == '__main__':
    bot.polling(skip_pending=True)
