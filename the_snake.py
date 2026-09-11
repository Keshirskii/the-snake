from random import choice, randint

import pygame

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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Класс с общими атрибутами игровых объектов"""

    def __init__(self, position=None, body_color=None):
        self.position = [(START_X, START_Y)]
        self.body_color = body_color

    def draw(self):
        """Заглушка"""
        pass

    @staticmethod
    def draw_square(position, body_color):
        """Отрисовка квадрата"""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    @staticmethod
    def randomize_position_square():
        """Получить рандомную позицию для квадрата"""
        х = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        return (х, y)


class Apple(GameObject):
    """Класс яблока"""

    def __init__(self):
        super().__init__(position=[(0, 0)], body_color=APPLE_COLOR)

    def randomize_position(self):
        """Получить рандомную позицию яблока в зоне игрового поля"""
        self.position = GameObject.randomize_position_square()

    def draw(self):
        """Отрисовка яблока"""
        GameObject.draw_square(self.position, self.body_color)


class Poison(GameObject):
    """Класс ядовитого яблока"""

    def __init__(self):
        super().__init__(position=[(0, 0)], body_color=POISON_COLOR)

    def randomize_position(self):
        """Получить рандомную позицию яда в зоне игрового поля"""
        self.position = GameObject.randomize_position_square()

    def draw(self):
        """Отрисовка яда"""
        GameObject.draw_square(self.position, self.body_color)


class Stone(GameObject):
    """Класс камня"""

    def __init__(self):
        super().__init__(position=[(0, 0)], body_color=STONE_COLOR)

    def randomize_position(self):
        """Получить рандомную позицию камня в зоне игрового поля"""
        self.position = GameObject.randomize_position_square()

    def draw(self):
        """Отрисовка камня"""
        GameObject.draw_square(self.position, self.body_color)


class Snake(GameObject):
    """Класс змейки"""

    def __init__(self):
        super().__init__(position=[(START_X, START_Y)],
                         body_color=SNAKE_COLOR)
        self.positions = self.position
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Получить координаты головы змейки"""
        return self.position[0]

    def move(self):
        """Смена координат змейки"""
        dx, dy = self.get_head_position()
        new_head_х = (dx + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH
        new_head_y = (dy + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_head_х, new_head_y)
        self.position.insert(0, new_head)

        if len(self.position) > self.length:
            self.last = self.position.pop()

    def update_direction(self):
        """Проверка на разворот в 180"""
        if self.next_direction:
            dx, dy = self.next_direction
            if (dx * -1, dy * -1) != self.direction:
                self.direction = self.next_direction
                self.next_direction = None

    def draw(self):
        """Отрисовка змейки"""
        for position in self.position:
            GameObject.draw_square(position, self.body_color)

    def reset(self):
        """Возвращает змейку в начальное состояние"""
        self.position = [(START_X, START_Y)]
        self.length = 1
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основной игровой цикл"""
    # Инициализация PyGame:
    pygame.init()

    # Экземпляры классов.
    apple = Apple()
    snake = Snake()
    poison = Poison()
    stone = Stone()

    def randomize():
        """Задать рандомные позиции для объектов"""
        apple.randomize_position()
        poison.randomize_position()
        stone.randomize_position()

    randomize()

    running = True

    # Игровой цикл
    while running:
        screen.fill(BOARD_BACKGROUND_COLOR)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        head = snake.get_head_position()

        # Проверка столкновения с яблоком
        if head == apple.position:
            snake.length += 1
            apple.randomize_position()

        # Проверка столкновения с ядом
        if head == poison.position:
            if len(snake.position) > 1:
                snake.position.pop()
                snake.length -= 1
                poison.randomize_position()
            else:
                randomize()
                snake.reset()

        # Проверка столкновения с камнем
        if head == stone.position:
            randomize()
            snake.reset()

        # Проверка столкновения с телом
        if head in snake.position[1:]:
            randomize()
            snake.reset()

        # Отрисовка объектов
        apple.draw()
        snake.draw()
        poison.draw()
        stone.draw()

        pygame.display.update()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
