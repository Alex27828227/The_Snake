from random import randrange

import pygame

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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject():
    """
    Создаем класс в котором прописываем
    общие атрибуты будущих игровых объектов
    """

    def __init__(self):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """
        Хз зачем это тут, взял из вебинара,
        один из тестов без него не проходит
        """
        pass


class Apple(GameObject):
    """
    Создаём дочерний класс Яблоко и переопределяем в нём
    атрибуты <body_color> - берём из константы и <позиция> - берём
    из описанного ниже метода - <случайная позиция>
    """

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()

    def randomize_position(self):
        """
        Метод <случайная позиция> возвращает случайные координаты,
        где должен появиться объект Яболоко в рамках игрового поля
        Здесь используем атрибут дочернего класса Змея <positions_for_aplee>
        """
        birth_apple = None
        while True:
            birth_apple = tuple(
                [randrange(0, SCREEN_WIDTH, 20),
                 randrange(0, SCREEN_HEIGHT, 20)]
            )
            if birth_apple not in Snake.check_positions_for_aplee:
                return birth_apple

    def draw(self):
        """
        Этот метод отрисовывает объект
        Яблоко на игровом поле
        """
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """
    Создаём атрибуты класса:
     <length> - все объекты Змея создаются с длинной 1 элемент
     <next_direction> - будет известно после итерации цикла, поэтому
      по умолчанию содержит None
     <direction> - направление куда движется змея сейчас
     <check_positions_for_aplee> - атрибут класса Змея для метода рандомного
      появления объекта яблоко в классе Яблоко.
    В дочернем классе Змея переопределяем атрибут объекта класса
     <body_color> - присваеваем из константы.
    с это атрибут хранящий список всех координат
     Змеи и присваиваем ему стартовую позицию из родительского класса.
    Определяем атрибут <next_direction> - ему присваеваем значение метода
     который обновляет направление движения Змеи
    Определяем атрибут <last> - атрибут с координатами последнего элемента Змеи
    """

    length = 1
    next_direction = None
    direction = RIGHT
    check_positions_for_aplee = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.positions = [self.position]
        self.next_direction = self.update_direction()
        self.last = self.position

    def update_direction(self):
        """
        Метод в котором мы обновляем текущее
        направление движения Змеи
        """
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def reset(self):
        """
        Метод сброса списка координат объекта змея
        и присванивания ему начальных координат.
        """
        self.positions = [self.position]

    def get_head_position(self):
        """Метод возвращает первый элемент списка координат объекта змея"""
        return self.positions[0]

    def next_position_head(self):
        """
        Метод, путём сложения первого элемента змеи и направления движения
        змие возвращает координаты следующей головы змеи
        """
        head_positions = self.get_head_position()
        return ((
            head_positions[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (head_positions[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        )

    def move(self):
        """
        Метод получает координаты следующей позиции змеи, вставляет в начало
        списка координат и удаляет последний элемент списка координат.
        А так же передаём координаты змеи атрибуту <check_positions_for_aplee>
        для проверки места появления яблока.
        """
        head_positions = self.next_position_head()
        self.last = self.positions[-1]
        self.positions.insert(0, head_positions)
        self.positions.pop(-1)
        self.check_positions_for_aplee = self.positions

    def draw(self):
        """Метод отрисовки тела Змеи"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """Метод управления человека и игрой через клавиатуру"""
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
    """Главная"""
    # Инициализация PyGame:
    pygame.init()
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            apple = Apple()
            snake.positions.append(apple.position)
        if snake.next_position_head() in snake.positions:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()


# Метод draw класса Apple
# def draw(self):
#     rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, rect)
#     pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self):
#     for position in self.positions[:-1]:
#         rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
#         pygame.draw.rect(screen, self.body_color, rect)
#         pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, head_rect)
#     pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя
# def handle_keys(game_object):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             raise SystemExit
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pygame.K_DOWN and game_object.direction != UP:
#                 game_object.next_direction = DOWN
#             elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
#                 game_object.next_direction = LEFT
#             elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
#                 game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None
