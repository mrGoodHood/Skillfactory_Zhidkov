import random


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!"


class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку!"


class BoardWrongShipException(BoardException):
    pass


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Dot({self.x}, {self.y})"


class Ship:
    def __init__(self, length, bow, orientation):
        self.length = length
        self.bow = bow
        self.orientation = orientation
        self.lives = length

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.length):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.orientation == "H":
                cur_y += i
            elif self.orientation == "V":
                cur_x += i

            ship_dots.append(Dot(cur_x, cur_y))
        return ship_dots

    def hit(self, shot):
        return shot in self.dots


class Board:
    def __init__(self, hid=False, size=10):
        self.size = size
        self.hid = hid
        self.count = 0

        self.field = [["O"] * size for _ in range(size)]

        self.busy = []
        self.ships = []

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:
            if ship.hit(d):
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен!")
                    return True
                else:
                    print("Корабль ранен!")
                    return True

        self.field[d.x][d.y] = "."
        print("Мимо!")
        return False

    def begin(self):
        self.busy = []

    def display(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:
            res = res.replace("■", "O")
        print(res)


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(random.randint(0, 9), random.randint(0, 9))
        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        return d


class User(Player):
    def ask(self):
        while True:
            coords = input("Ваш ход: ").split()
            if len(coords) != 2:
                print(" Введите 2 координаты! ")
                continue

            x, y = coords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size=10):
        self.size = size
        user_board = self.random_board()
        ai_board = self.random_board()
        ai_board.hid = True

        self.user = User(user_board, ai_board)
        self.ai = AI(ai_board, user_board)

    def random_board(self):
        board = None
        attempts = 0
        while board is None:
            board = self.try_create_board()
            attempts += 1
            if attempts > 2000:
                raise Exception("Не удалось создать игровую доску.")
        return board

    def try_create_board(self):
        length_ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for length in length_ships:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(length, Dot(random.randint(0, self.size - 1),
                                        random.randint(0, self.size - 1)),
                            random.choice(['H', 'V']))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    continue
        board.begin()
        return board

    def greet(self):
        print("Добро пожаловать в игру Морской бой!")
        print("формат ввода: x y")
        print("x - номер строки")
        print("y - номер столбца")

    def loop(self):
        num = 0
        while True:
            print()
            print("Ваша доска:")
            self.user.board.display()
            print()
            print("Доска компьютера:")
            self.ai.board.display()
            print()
            if num % 2 == 0:
                print("Ваш ход!")
                repeat = self.user.move()
            else:
                print("Ход компьютера!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == len(self.ai.board.ships):
                print("Вы выиграли!")
                break

            if self.user.board.count == len(self.user.board.ships):
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


if __name__ == "__main__":
    game = Game()
    game.start()
