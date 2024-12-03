import pygame
import random
import time
import sqlite3

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (15, 255, 15)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
SPACESHIP_WIDTH = 30
SPACESHIP_HEIGHT = 30
ASTEROID_RADIUS = 15
SUPER_ASTEROID_RADIUS = 20
LASER_WIDTH = 5
LASER_HEIGHT = 20
LASER_SPEED = 10
ASTEROID_SPEED = 5
LIVES = 3
GAME_DURATION = 40
SUPER_ASTEROID_INTERVAL = 10
SPEED_BOOST_DURATION = 5
NUM_STARS = 100

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Shooter")

laser_image = pygame.Surface((LASER_WIDTH, LASER_HEIGHT))
laser_image.fill(WHITE)

class Spaceship:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2 - SPACESHIP_WIDTH // 2, SCREEN_HEIGHT - SPACESHIP_HEIGHT - 10, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
        self.speed = 5
        self.laser_interval = 1

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed

    def draw(self):
        pygame.draw.polygon(screen, GREEN, [
            (self.rect.centerx, self.rect.top),
            (self.rect.left, self.rect.bottom),
            (self.rect.right, self.rect.bottom)
        ])

class Laser:
    def __init__(self, x, y):
        self.image = laser_image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

    def update(self):
        self.rect.y -= LASER_SPEED

    def draw(self):
        screen.blit(self.image, self.rect)

class Asteroid:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, SCREEN_WIDTH - ASTEROID_RADIUS * 2), random.randint(-100, -40), ASTEROID_RADIUS * 2, ASTEROID_RADIUS * 2)
        self.speed = ASTEROID_SPEED

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH - ASTEROID_RADIUS * 2)
            self.rect.y = random.randint(-100, -40)

    def draw(self):
        pygame.draw.circle(screen, RED, self.rect.center, ASTEROID_RADIUS)

class SuperAsteroid:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, SCREEN_WIDTH - SUPER_ASTEROID_RADIUS * 2), random.randint(-100, -40), SUPER_ASTEROID_RADIUS * 2, SUPER_ASTEROID_RADIUS * 2)
        self.speed = ASTEROID_SPEED

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH - SUPER_ASTEROID_RADIUS * 2)
            self.rect.y = random.randint(-100, -40)

    def draw(self):
        pygame.draw.circle(screen, YELLOW, self.rect.center, SUPER_ASTEROID_RADIUS)

def draw_stars():
    for _ in range(NUM_STARS):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        color = random.choice([WHITE, BLUE, PURPLE])
        pygame.draw.circle(screen, color, (x, y), 2)

def show_start_screen():
    font = pygame.font.Font(None, 74)
    text = font.render("Стартуем!", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))

    description_font = pygame.font.Font(None, 24)
    description_text = (
        "Твоя задача уничтожить как можно больше астероидов за 40 секунд. "
        "Управление осуществляется стрелочками. Уничтожение желтых астероидов дает бафф "
        "скорострельности на несколько секунд. Попадание астероида по кораблю снимает одну жизнь, "
        "всего их 3. Будь осторожен и удачи!"
    )
    description_lines = description_text.split(' ')
    description_surface = []
    current_line = ''

    for word in description_lines:
        if description_font.size(current_line + word)[0] < SCREEN_WIDTH - 20:
            current_line += word + ' '
        else:
            description_surface.append(description_font.render(current_line, True, WHITE))
            current_line = word + ' '
    description_surface.append(description_font.render(current_line, True, WHITE))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if text_rect.collidepoint(event.pos):
                    running = False

        screen.fill(BLACK)
        draw_stars()
        screen.blit(text, text_rect)

        y_offset = SCREEN_HEIGHT // 2
        for line in description_surface:
            screen.blit(line, (10, y_offset))
            y_offset += line.get_height()

        pygame.display.flip()

def show_game_over_screen(score):
    font = pygame.font.Font(None, 74)
    text = font.render("Вы проиграли!", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))

    score_text = font.render(f"Счет: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50)
    quit_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 120, 200, 50)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    return True
                if quit_button.collidepoint(event.pos):
                    return False

        screen.fill(BLACK)
        draw_stars()
        screen.blit(text, text_rect)
        screen.blit(score_text, score_rect)
        pygame.draw.rect(screen, GREEN, restart_button)
        pygame.draw.rect(screen, RED, quit_button)

        font = pygame.font.Font(None, 36)
        restart_text = font.render("Рестарт", True, WHITE)
        screen.blit(restart_text, (restart_button.x + 50, restart_button.y + 10))

        quit_text = font.render("Выход", True, WHITE)
        screen.blit(quit_text, (quit_button.x + 50, quit_button.y + 10))

        pygame.display.flip()

def show_game_win_screen(score, top_scores):
    font = pygame.font.Font(None, 74)
    text = font.render("Вы выиграли!", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))

    score_text = font.render(f"Счет: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))

    top_scores_text = font.render("Топ 5 игроков:", True, WHITE)
    top_scores_rect = top_scores_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))

    restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 150, 200, 50)
    quit_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 220, 200, 50)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    return True
                if quit_button.collidepoint(event.pos):
                    return False

        screen.fill(BLACK)
        draw_stars()
        screen.blit(text, text_rect)
        screen.blit(score_text, score_rect)
        screen.blit(top_scores_text, top_scores_rect)

        y_offset = SCREEN_HEIGHT // 2
        for score in top_scores:
            score_text = font.render(f"{score.name}: {score.score}", True, WHITE)
            screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, y_offset))
            y_offset += score_text.get_height() + 10

        pygame.draw.rect(screen, GREEN, restart_button)
        pygame.draw.rect(screen, RED, quit_button)

        font = pygame.font.Font(None, 36)
        restart_text = font.render("Рестарт", True, WHITE)
        screen.blit(restart_text, (restart_button.x + 50, restart_button.y + 10))

        quit_text = font.render("Выход", True, WHITE)
        screen.blit(quit_text, (quit_button.x + 50, quit_button.y + 10))

        pygame.display.flip()

def game_loop(player_name):
    global lives
    lives = LIVES
    destroyed_asteroids = 0
    start_time = time.time()
    last_super_asteroid_time = time.time()
    speed_boost_end_time = 0

    spaceship = Spaceship()
    lasers = []
    asteroids = [Asteroid() for _ in range(5)]
    super_asteroids = []

    last_shot_time = time.time()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        spaceship.update()

        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time >= GAME_DURATION:
            running = False
            score_manager.add_score(player_name, destroyed_asteroids)
            top_scores = score_manager.get_top_scores(5)
            if show_game_win_screen(destroyed_asteroids, top_scores):
                game_loop(player_name)
            else:
                pygame.quit()
                exit()

        if current_time - last_shot_time >= spaceship.laser_interval:
            lasers.append(Laser(spaceship.rect.centerx, spaceship.rect.top))
            last_shot_time = current_time

        if (current_time - last_super_asteroid_time) >= SUPER_ASTEROID_INTERVAL:
            super_asteroids.append(SuperAsteroid())
            last_super_asteroid_time = current_time

        for laser in lasers:
            laser.update()
            if laser.rect.bottom < 0:
                lasers.remove(laser)

        for asteroid in asteroids:
            asteroid.update()
            for laser in lasers:
                if laser.rect.colliderect(asteroid.rect):
                    lasers.remove(laser)
                    asteroids.remove(asteroid)
                    asteroids.append(Asteroid())
                    destroyed_asteroids += 1
                    break
            if asteroid.rect.colliderect(spaceship.rect):
                lives -= 1
                asteroids.remove(asteroid)
                asteroids.append(Asteroid())
                if lives <= 0:
                    running = False
                    if show_game_over_screen(destroyed_asteroids):
                        game_loop(player_name)
                    else:
                        pygame.quit()
                        exit()
                    break

        for super_asteroid in super_asteroids:
            super_asteroid.update()
            for laser in lasers:
                if laser.rect.colliderect(super_asteroid.rect):
                    lasers.remove(laser)
                    super_asteroids.remove(super_asteroid)
                    spaceship.laser_interval = 0.33
                    speed_boost_end_time = current_time + SPEED_BOOST_DURATION
                    break
            if super_asteroid.rect.colliderect(spaceship.rect):
                lives -= 1
                super_asteroids.remove(super_asteroid)
                if lives <= 0:
                    running = False
                    if show_game_over_screen(destroyed_asteroids):
                        game_loop(player_name)
                    else:
                        pygame.quit()
                        exit()
                    break

        if current_time >= speed_boost_end_time and speed_boost_end_time != 0:
            spaceship.laser_interval = 1
            speed_boost_end_time = 0

        screen.fill(BLACK)
        draw_stars()
        spaceship.draw()
        for laser in lasers:
            laser.draw()
        for asteroid in asteroids:
            asteroid.draw()
        for super_asteroid in super_asteroids:
            super_asteroid.draw()

        font = pygame.font.Font(None, 36)
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(lives_text, (10, 10))

        time_left = max(0, int(GAME_DURATION - elapsed_time))
        timer_text = font.render(f"Time: {time_left}", True, WHITE)
        screen.blit(timer_text, (10, 50))

        destroyed_text = font.render(f"Destroyed: {destroyed_asteroids}", True, WHITE)
        screen.blit(destroyed_text, (10, 90))

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    show_start_screen()

def show_input_screen():
    font = pygame.font.Font(None, 36)
    input_box = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 25, 300, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill(BLACK)
        draw_stars()

        # Отображение надписи "Введите свой ник"
        prompt_text = font.render("Введите свой ник:", True, WHITE)
        screen.blit(prompt_text, (SCREEN_WIDTH // 2 - prompt_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))

        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        input_box.w = max(200, txt_surface.get_width() + 10)
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()

    return text

# Создание таблицы
def create_scores_table():
    conn = sqlite3.connect('scores.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            score INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

class Score:
    def __init__(self, id, name, score):
        self.id = id
        self.name = name
        self.score = score

class ScoreManager:
    def __init__(self, db_name='scores.db'):
        self.db_name = db_name

    def add_score(self, name, score):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO scores (name, score) VALUES (?, ?)', (name, score))
        conn.commit()
        conn.close()

    def get_top_scores(self, limit=5):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT name, MAX(score) as max_score
            FROM scores
            GROUP BY name
            ORDER BY max_score DESC
            LIMIT ?
        ''', (limit,))
        rows = cursor.fetchall()
        conn.close()
        return [Score(None, name, score) for name, score in rows]

create_scores_table()

score_manager = ScoreManager()

player_name = show_input_screen()
show_start_screen()
game_loop(player_name)

pygame.quit()
