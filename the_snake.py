"""Основной модуль игры."""
from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Центр экрана
START_X = SCREEN_WIDTH // 2
START_Y = SCREEN_HEIGHT // 2

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Словарь с направлениями:
KEY_TO_DIRECTION = {
    pg.K_UP: UP,
    pg.K_DOWN: DOWN,
    pg.K_LEFT: LEFT,
    pg.K_RIGHT: RIGHT,
}

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Цвет яда
POISON_COLOR = (128, 0, 128)

# Цвет камня
STONE_COLOR = (128, 128, 128)

# Скорость движения змейки:
SPEED = 15

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Класс с общими атрибутами игровых объектов."""

    def __init__(self, body_color=None):
        """Инициализация общих атрибутов игровых объектов."""
        self.position = (START_X, START_Y)
        self.body_color = body_color

    def _draw_cell(self):
        """Отрисовка квадрата."""
        rect = pg.Rect(self.position[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self, occupied_positions):
        """Получить рандомную позицию для квадрата."""
        occupied_positions = occupied_positions or set()
        while True:
            x_axis = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y_axis = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            self.position = [(x_axis, y_axis)]

            if self.position[0] not in occupied_positions:
                break


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self, occupied_positions=None):
        """Инициализация яблока."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position(occupied_positions)


class Poison(GameObject):
    """Класс ядовитого яблока."""

    def __init__(self, occupied_positions=None):
        """Инициализация ядовитого яблока."""
        super().__init__(body_color=POISON_COLOR)
        self.randomize_position(occupied_positions)


class Stone(GameObject):
    """Класс камня."""

    def __init__(self, occupied_positions=None):
        """Инициализация камня."""
        super().__init__(body_color=STONE_COLOR)
        self.randomize_position(occupied_positions)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
        """Инициализация змейки."""
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()

    def get_head_position(self):
        """Получить координаты головы змейки."""
        return self.positions[0]

    def move(self):
        """Смена координат змейки."""
        head_x_axis, head_y_axis = self.get_head_position()
        dx, dy = self.direction
        new_head_х_axis = (
            head_x_axis + dx * GRID_SIZE) % SCREEN_WIDTH
        new_head_y_axis = (
            head_y_axis + dy * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_head_х_axis, new_head_y_axis)
        self.positions.insert(0, new_head)

        self.last = (
            self.positions.pop()
            if len(self.positions) > self.length else None)

    def update_direction(self):
        """Проверка на разворот в 180."""
        if self.next_direction:
            dx, dy = self.next_direction
            if (dx * -1, dy * -1) != self.direction:
                self.direction = self.next_direction
                self.next_direction = None

    def shrink(self):
        """Удаление хвоста при поедании яда."""
        tail = self.positions.pop()
        delete_square(tail)
        self.length -= 1

    def reset(self):
        """Возвращает змейку в начальное состояние."""
        self.positions = [(START_X, START_Y)]
        self.length = 1
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            proposed_direction = KEY_TO_DIRECTION.get(event.key)
            if proposed_direction is not None:
                opposite = (-proposed_direction[0], -proposed_direction[1])
                if game_object.direction != opposite:
                    game_object.next_direction = proposed_direction


def get_occupied_positions(snake, apple, poison, stone):
    """Получить позиции игровых объектов."""
    occupied_positions = set()
    occupied_positions.update(snake.positions)
    occupied_positions.update(apple.position)
    occupied_positions.update(poison.position)
    occupied_positions.update(stone.position)
    return occupied_positions


def randomize(snake, apple, poison, stone):
    """Задать рандомные позиции для объектов без повторений."""
    occupierd_positions = get_occupied_positions(
        snake, apple, poison, stone)
    apple.randomize_position(occupierd_positions)
    occupierd_positions.add(apple.position[0])
    poison.randomize_position(occupierd_positions)
    occupierd_positions.add(poison.position[0])
    stone.randomize_position(occupierd_positions)
    occupierd_positions.add(stone.position[0])


def delete_square(position):
    """Удаление игрового объекта с поля."""
    rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
    pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)
    pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect, 1)


def game_reset(snake, apple, poison, stone):
    """Сброс игры."""
    randomize(snake, apple, poison, stone)
    snake.reset()


def main():
    """Основной игровой цикл."""
    # Инициализация pg:
    pg.init()

    screen.fill(BOARD_BACKGROUND_COLOR)

    # Экземпляры классов.
    snake = Snake()

    occupied_positions = set()
    occupied_positions.update(snake.positions)

    apple = Apple(occupied_positions)
    occupied_positions.add(apple.position[0])

    poison = Poison(occupied_positions)
    occupied_positions.add(poison.position[0])

    stone = Stone(occupied_positions)

    running = True

    # Игровой цикл
    while running:

        handle_keys(snake)
        snake.update_direction()
        snake.move()
        head = snake.get_head_position()

        # Удаление хвоста
        if snake.last is not None:
            delete_square(snake.last)

        # Проверка столкновения с яблоком
        if head == apple.position[0]:

            snake.length += 1
            occupied_positions = get_occupied_positions(snake, apple,
                                                        poison, stone)
            apple.randomize_position(occupied_positions)

        # Проверка столкновения с ядом
        if head == poison.position[0]:
            if len(snake.positions) > 1:
                snake.shrink()
                occupied_positions = get_occupied_positions(snake, apple,
                                                            poison, stone)
                poison.randomize_position(occupied_positions)
            else:
                game_reset(snake, apple, poison, stone)

        # Проверка столкновения с камнем или телом
        if head == stone.position[0] or head in snake.positions[1:]:
            game_reset(snake, apple, poison, stone)

        # Отрисовка объектов
        apple._draw_cell()
        snake._draw_cell()
        poison._draw_cell()
        stone._draw_cell()

        pg.display.update()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
