import pygame
import sys
import random
import pygame_menu
import time

# Инициализация Pygame
pygame.init()

# Размеры экрана
width = 600
height = 400

# Цвета
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# Размер ячейки
cell_size = 20

# Скорость змейки
snake_speed = 15

# Создание экрана
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Змейка")

# Класс змейки
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((width // 2), (height // 2))]
        self.direction = random.choice([0, 1, 2, 3])  # 0: вверх, 1: вниз, 2: влево, 3: вправо
        self.color = red
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        x, y = self.positions[0]

        if self.direction == 0:
            new = (x, y - cell_size)
        elif self.direction == 1:
            new = (x, y + cell_size)
        elif self.direction == 2:
            new = (x - cell_size, y)
        elif self.direction == 3:
            new = (x + cell_size, y)

        self.positions = [new] + self.positions
        if len(self.positions) > self.length:
            self.positions = self.positions[:-1]

    def move(self, direction):
        if direction == 0 != self.direction == 1:
            self.direction = 0
        elif direction == 1 != self.direction == 0:
            self.direction = 1
        elif direction == 2 != self.direction == 3:
            self.direction = 2
        elif direction == 3 != self.direction == 2:
            self.direction = 3

    def reset(self):
        self.length = 1
        self.positions = [((width // 2), (height // 2))]
        self.direction = random.choice([0, 1, 2, 3])
        self.score = 0

    def draw(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, self.color, pygame.Rect(p[0], p[1], cell_size, cell_size))

    def increase_score(self, num):
        self.score += num


def game_over(self):
    font = pygame.font.Font(None, 36)
    text = font.render("Game Over", True, white)
    screen.blit(text, (50,100))
    pygame.display.flip()
    time.sleep(2)  # Пауза перед выходом
    pygame.quit()
    sys.exit()


# Класс фрукта
class Fruit:
    def __init__(self):
        self.position = (0, 0)
        self.color = white
        self.randomize_position()

    def randomize_position(self):
        self.position = (
            random.randint(0, (width - cell_size) // cell_size) * cell_size,
            random.randint(0, (height - cell_size) // cell_size) * cell_size
        )

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, pygame.Rect(self.position[0], self.position[1], cell_size, cell_size))


# Функция отрисовки сетки
def draw_grid(surface):
    for y in range(0, height, cell_size):
        for x in range(0, width, cell_size):
            rect = pygame.Rect(x, y, cell_size, cell_size)
            pygame.draw.rect(surface, black, rect, 1)


# Класс бонуса
class Bonus:
    def __init__(self):
        self.position = (0, 0)
        self.color = (223, 163, 49)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, (width - cell_size) // cell_size) * cell_size,
            random.randint(0, (height - cell_size) // cell_size) * cell_size)

    def render(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], cell_size, cell_size))


# Основная функция игры
def handle_keydown_event(event, snake):
    if event.key == pygame.K_UP:
        snake.move(0)
    elif event.key == pygame.K_DOWN:
        snake.move(1)
    elif event.key == pygame.K_LEFT:
        snake.move(2)
    elif event.key == pygame.K_RIGHT:
        snake.move(3)

def check_collision(snake, fruit, bonuses):
    if snake.get_head_position() == fruit.position:
        snake.length += 1
        snake.increase_score(1)
        fruit.randomize_position()

    if random.random() < 0.01:
        bonuses.append(Bonus())

    for bonus in bonuses:
        if snake.get_head_position() == bonus.position:
            snake.length += 1
            bonuses.remove(bonus)
            snake.increase_score(5)

    if (
        snake.get_head_position()[0] < 0 or
        snake.get_head_position()[1] < 0 or
        snake.get_head_position()[0] > width - cell_size or
        snake.get_head_position()[1] > height - cell_size
    ):
        snake.game_over()

    for segment in snake.positions[1:]:
        if segment == snake.get_head_position():
            snake.game_over()

def draw_elements(screen, snake, fruit, bonuses):
    screen.fill(black)
    draw_grid(screen)
    snake.draw(screen)
    fruit.draw(screen)
    for bonus in bonuses:
        bonus.render(screen)

def draw_score(screen, snake, font, white):
    score_text = font.render(f"Score: {snake.score}", True, white)
    screen.blit(score_text, (10, 10))

def main():
    clock = pygame.time.Clock()
    snake = Snake()
    fruit = Fruit()
    bonuses = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                handle_keydown_event(event, snake)

        snake.update()
        check_collision(snake, fruit, bonuses)

        draw_elements(screen, snake, fruit, bonuses)
        font = pygame.font.Font(None, 36)
        draw_score(screen, snake, font, white)

        pygame.display.update()
        clock.tick(snake_speed)


menu = pygame_menu.Menu('Welcome', width, height, theme=pygame_menu.themes.THEME_GREEN)

menu.add.text_input('Name: ', default='Player 1')
menu.add.button('Play', main)
menu.add.button('Quit', pygame_menu.events.EXIT)

if __name__ == "__main__":
    menu.mainloop(screen)
