import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Adi 的平台跳躍遊戲（踩扁敵人版）")

WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
BROWN = (139, 69, 19)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
BLUE = (0, 128, 255)

clock = pygame.time.Clock()
FPS = 60

player_w, player_h = 40, 50
player_x, player_y = 100, 500  # 初始位置改一下，不重疊金幣
player_speed = 5
player_y_speed = 0
gravity = 0.5
jump_power = -10
on_ground = False

score = 0
font = pygame.font.SysFont(None, 36)

level_width = 1600

platforms = [
    pygame.Rect(0, 550, 400, 50),
    pygame.Rect(450, 480, 150, 20),
    pygame.Rect(650, 420, 150, 20),
    pygame.Rect(850, 360, 150, 20),
    pygame.Rect(1100, 500, 200, 20),
    pygame.Rect(1400, 550, 200, 50),
]

coins = [
    pygame.Rect(300, 520, 20, 20),
    pygame.Rect(500, 440, 20, 20),
    pygame.Rect(700, 380, 20, 20),
    pygame.Rect(900, 320, 20, 20),
    pygame.Rect(1200, 460, 20, 20),
    pygame.Rect(1500, 520, 20, 20),
]

class Goomba:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 2
        self.direction = 1
        self.w = 40
        self.h = 50
        self.y_speed = 0
        self.on_ground = False
        self.alive = True

    def move(self, platforms):
        if not self.alive:
            return
        self.x += self.speed * self.direction
        if self.x < 0 or self.x + self.w > level_width:
            self.direction *= -1

        self.y_speed += 0.5
        self.y += self.y_speed
        self.on_ground = False
        rect = pygame.Rect(self.x, self.y, self.w, self.h)
        for plat in platforms:
            if rect.colliderect(plat) and self.y_speed >= 0:
                self.y = plat.top - self.h
                self.y_speed = 0
                self.on_ground = True

        front_rect = pygame.Rect(self.x + self.direction * self.speed, self.y + self.h + 1, self.w, 5)
        on_platform_ahead = False
        for plat in platforms:
            if front_rect.colliderect(plat):
                on_platform_ahead = True
                break
        if not on_platform_ahead:
            self.direction *= -1

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def draw(self, surface, offset_x):
        if self.alive:
            rect = pygame.Rect(self.x - offset_x, self.y, self.w, self.h)
            pygame.draw.rect(surface, BROWN, rect)

running = True
player_rect = pygame.Rect(player_x, player_y, player_w, player_h)

enemies = [
    Goomba(300, 500),
    Goomba(600, 440),
    Goomba(900, 380),
    Goomba(1200, 500),
    Goomba(1400, 500),
]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    player_x = max(0, min(player_x, level_width - player_w))

    player_y_speed += gravity
    player_y += player_y_speed

    player_rect = pygame.Rect(player_x, player_y, player_w, player_h)
    on_ground = False
    for plat in platforms:
        if player_rect.colliderect(plat) and player_y_speed >= 0:
            player_y = plat.top - player_h
            player_y_speed = 0
            on_ground = True

    if keys[pygame.K_UP] and on_ground:
        player_y_speed = jump_power
        on_ground = False

    for enemy in enemies:
        enemy.move(platforms)
        if enemy.alive:
            enemy_rect = enemy.get_rect()
            if player_rect.colliderect(enemy_rect):
                if player_y + player_h <= enemy.y + 10 and player_y_speed > 0:
                    enemy.alive = False
                    player_y_speed = jump_power / 2
                    score += 10
                else:
                    print("Game Over!")
                    running = False

    new_coins = []
    for coin in coins:
        if player_rect.colliderect(coin):
            score += 1
        else:
            new_coins.append(coin)
    coins = new_coins

    offset_x = player_x - WIDTH // 2
    offset_x = max(0, min(offset_x, level_width - WIDTH))

    screen.fill(WHITE)
    for plat in platforms:
        rect = pygame.Rect(plat.x - offset_x, plat.y, plat.width, plat.height)
        pygame.draw.rect(screen, GREEN, rect)

    for coin in coins:
        coin_rect = pygame.Rect(coin.x - offset_x, coin.y, coin.width, coin.height)
        pygame.draw.rect(screen, GOLD, coin_rect)

    pygame.draw.rect(screen, BLUE, (player_x - offset_x, player_y, player_w, player_h))

    for enemy in enemies:
        enemy.draw(screen, offset_x)

    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
