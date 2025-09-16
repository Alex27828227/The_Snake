from random import randrange

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

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

# Скорость движения змейки:
SPEED = 5

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


# Тут опишите все классы игры.
class GameObject():
    """
    Создаем класс.

    В нём прописываем общие атрибуты будущих игровых объектов.
    """

    def __init__(self, body_color=None):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = body_color

    def draw(self):
        """Метод для отрисовки объектов."""
        pass


class Apple(GameObject):
    """
    Создаём дочерний класс Яблоко.

    Переопределяем в нём атрибуты <body_color> - берём из константы
    а позицию - получаем из описанного ниже метода - <randomize_position>!.
    """

    def __init__(self, body_color=APPLE_COLOR, occupied_positions=[]):
        super().__init__(body_color=APPLE_COLOR)
        self.body_color = body_color
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions):
        """
        Генерируем случайную позицию яблока.

        С помощью параметра <occupied_positions> исключаем
        появления яблока на месте змеи.
        """
        while True:
            self.position = (
                randrange(0, SCREEN_WIDTH, 20),
                randrange(0, SCREEN_HEIGHT, 20)
            )
            if self.position not in occupied_positions:
                break

    def draw(self):
        """
        Метод <draw>.

        Метод отрисовывает объект Яблоко на игровом поле.
        """
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """
    Создаём атрибуты класса.

    -<next_direction> - будет известно после итерации цикла, поэтому
      по умолчанию содержит None.
    -<length> - все объекты Змея создаются с длинной 1 элемент.
    -<direction> - направление куда движется змея на старте.
    -В дочернем классе Змея переопределяем атрибут объекта класса
     <body_color> - присваеваем из константы.
    - <reset> метод сброса объекта змея к начальным  настройкам.
    -Определяем атрибут <next_direction> - ему присваеваем значение метода
     который обновляет направление движения Змеи.
    Определяем атрибут <last>- атрибут с координатами последнего элемента Змеи.
    """

    next_direction = None

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color=SNAKE_COLOR)
        self.length = 1
        self.body_color = body_color
        self.direction = RIGHT
        self.reset()
        self.next_direction = self.update_direction()
        self.last = self.position

    def update_direction(self):
        """Метод в котором мы обновляем текущее направление движения Змеи."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def reset(self):
        """
        Метод сброса.

        Сбрасывает длинну объекта змея, а так же
        присваивает ему начальные координаты.
        """
        self.positions = [self.position]
        self.length = 1

    def get_head_position(self):
        """Метод возвращает первый элемент списка координат объекта змея."""
        return self.positions[0]

    def move(self):
        """
        Метод <move>.

        Вычисляет координаты следующей позиции змеи, вставляет в начало
        списка координат и удаляет последний элемент списка координат.
        Или не удаляет последний элемент, если объект съел яблоко.
        """
        self.position = (
            (self.get_head_position()[0] + self.direction[0] * GRID_SIZE)
            % SCREEN_WIDTH,
            (self.get_head_position()[1] + self.direction[1] * GRID_SIZE)
            % SCREEN_HEIGHT
        )
        self.positions.insert(0, self.position)
        if len(self.positions) > self.length:
            self.last = self.positions.pop(-1)
        else:
            self.last = None

    def draw(self):
        """Метод отрисовки тела Змеи."""
        for position in self.positions[:-1]:
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pg.Rect(self.get_head_position(), (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """Метод управления человеком игрой через клавиатуру."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Главная."""
    pg.init()
    snake = Snake(SNAKE_COLOR)
    apple = Apple(APPLE_COLOR, snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
