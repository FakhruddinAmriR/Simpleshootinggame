import pygame
import random
import sys

# ================= INIT =================
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🔥 Python Shooter Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 32)

# ================= COLORS =================
WHITE = (255,255,255)
RED   = (255,80,80)
GREEN = (80,255,80)
BLUE  = (80,80,255)
YELLOW = (255,255,0)
BG_COLOR = (20,20,30)

# ================= PLAYER =================
player_width = 60
player_height = 40
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 80
player_speed = 7

# ================= BULLET =================
bullets = []
bullet_speed = 10

# ================= ENEMY =================
enemies = []
enemy_speed = 3
spawn_delay = 40
spawn_timer = 0

# ================= GAME =================
score = 0
game_over = False

# ================= FUNCTIONS =================
def draw_player():
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))
    pygame.draw.rect(screen, YELLOW, (player_x+10, player_y-10, 40, 10))  # cannon

def draw_bullets():
    for bullet in bullets:
        pygame.draw.rect(screen, RED, bullet)

def draw_enemies():
    for enemy in enemies:
        pygame.draw.rect(screen, GREEN, enemy)

def show_text(text, x, y, color=WHITE):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# ================= MAIN LOOP =================
running = True
while running:
    clock.tick(60)
    screen.fill(BG_COLOR)

    # -------- EVENT --------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bullet = pygame.Rect(player_x + player_width//2 - 5, player_y, 10, 20)
                bullets.append(bullet)

            if event.key == pygame.K_r and game_over:
                # restart game
                bullets.clear()
                enemies.clear()
                score = 0
                game_over = False

    keys = pygame.key.get_pressed()
    if not game_over:
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player_x += player_speed

    player_x = max(0, min(WIDTH - player_width, player_x))

    # -------- SPAWN ENEMY --------
    if not game_over:
        spawn_timer += 1
        if spawn_timer >= spawn_delay:
            spawn_timer = 0
            x = random.randint(0, WIDTH - 40)
            enemy = pygame.Rect(x, -40, 40, 40)
            enemies.append(enemy)

    # -------- UPDATE BULLETS --------
    for bullet in bullets[:]:
        bullet.y -= bullet_speed
        if bullet.y < 0:
            bullets.remove(bullet)

    # -------- UPDATE ENEMIES --------
    for enemy in enemies[:]:
        enemy.y += enemy_speed

        if enemy.y > HEIGHT:
            enemies.remove(enemy)

        # Collision with player
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        if enemy.colliderect(player_rect):
            game_over = True

        # Collision with bullets
        for bullet in bullets[:]:
            if enemy.colliderect(bullet):
                enemies.remove(enemy)
                bullets.remove(bullet)
                score += 1
                break

    # -------- DRAW --------
    draw_player()
    draw_bullets()
    draw_enemies()
    show_text(f"Score: {score}", 10, 10)

    if game_over:
        show_text("💀 GAME OVER", WIDTH//2 - 120, HEIGHT//2 - 40, RED)
        show_text("Tekan R untuk Restart", WIDTH//2 - 170, HEIGHT//2 + 10, WHITE)

    pygame.display.flip()

pygame.quit()
sys.exit()
