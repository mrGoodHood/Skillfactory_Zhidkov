field = list(range(1, 10))


def instruction():
    """ Инструкция к игре"""
    instructions = """
    Перед вами классическая игра крестики-нолики, в которую играют два игрока поочередно.
    Поле состоит из 9 клеток, пронумерованных от 1 до 9:
    Цель игры: Расставить свои символы так, чтобы заполнить три клетки по горизонтали, вертикали или диагонали.

    Как играть:
    Первый игрок играет за "X", второй — за "O".
    Игроки поочередно вводят номер клетки (от 1 до 9), куда хотят поставить свой символ.

    Игра заканчивается, когда один из игроков заполняет три клетки подряд своим символом.
    Если все клетки заполнены и никто не собрал три клетки подряд, объявляется ничья.

    Приятной игры!
    """
    print(instructions)


def print_field(field):
    """Функция выводит игровое поле"""
    for i in range(3):
        print(field[0+i*3], field[1+i*3], field[2+i*3])


def take_input(player_token):
    """Функция получает информацию от игрока"""
    valid = False
    while not valid:
        player_answer = input(f"Ход игрока {player_token}: ")
        print()
        try:
            player_answer = int(player_answer)
        except ValueError:
            print("Некорректный ввод. Введите номер клетки: ")
            continue
        if 1 <= player_answer <= 9:
            if str(field[player_answer-1]) not in "XO":
                field[player_answer-1] = player_token
                valid = True
            else:
                print("Клетка уже занята. Выберите другую клетку: ")
        else:
            print("Некорректный ввод. Введите номер клетки: ")


def win_combination(field):
    """Функция проверяет, есть ли победная комбинация"""
    win_coord = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
    for each in win_coord:
        if field[each[0]] == field[each[1]] == field[each[2]]:
            return field[each[0]]
    return False


def main(field):
    """ Функция собирает всё вместе"""
    counter = 0
    win = False
    while not win:
        print_field(field)
        if counter % 2 == 0:
            take_input("X")
        else:
            take_input("O")
        counter += 1

        tmp = win_combination(field)
        if tmp:
            print_field(field)
            print(tmp, "выиграл!")
            print()
            break
        if counter == 9:
            print_field(field)
            print("Ничья!")
            print()
            break


instruction()
while True:
    main(field)
