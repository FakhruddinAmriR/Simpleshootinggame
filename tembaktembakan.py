import pygame
import random
import sys
import math

# ================= INIT =================
pygame.init()
WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🔥 Python Shooter Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 26)

# ================= COLORS =================
WHITE = (255,255,255)
RED   = (255,80,80)
GREEN = (80,255,80)
BLUE  = (80,80,255)
YELLOW = (255,255,0)
PURPLE = (180,80,255)
BG_COLOR = (20,20,30)

# ================= PLAYER =================
player_pos = pygame.Vector2(WIDTH//2, HEIGHT//2)
player_size = 45
player_speed = 5
lives = 3

# ================= BULLETS =================
bullets = []
bullet_speed = 12

# ================= ENEMIES =================
enemies = []
spawn_delay = 55
spawn_timer = 0

NORMAL_SPEED = 1.0
TANK_SPEED = 0.5

# ================= GAME =================
score = 0
game_over = False

# ================= FUNCTIONS =================
def draw_player():
    pygame.draw.circle(screen, BLUE, player_pos, player_size//2)
    
    # Arahkan moncong ke mouse
    mouse_pos = pygame.mouse.get_pos()
    direction = pygame.Vector2(mouse_pos) - player_pos
    if direction.length() > 0:
        direction = direction.normalize()
        end_pos = player_pos + direction * (player_size//2 + 10)
        pygame.draw.line(screen, YELLOW, player_pos, end_pos, 4)

def draw_bullets():
    for bullet in bullets:
        pygame.draw.circle(screen, RED, bullet["pos"], 5)

def draw_enemies():
    for enemy in enemies:
        color = GREEN if enemy["type"] == "normal" else PURPLE
        pygame.draw.circle(screen, color, enemy["pos"], enemy["radius"])

def show_text(text, x, y, color=WHITE):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def spawn_enemy():
    side = random.choice(["top", "bottom", "left", "right"])

    if side == "top":
        pos = pygame.Vector2(random.randint(0, WIDTH), -40)
    elif side == "bottom":
        pos = pygame.Vector2(random.randint(0, WIDTH), HEIGHT + 40)
    elif side == "left":
        pos = pygame.Vector2(-40, random.randint(0, HEIGHT))
    else:
        pos = pygame.Vector2(WIDTH + 40, random.randint(0, HEIGHT))

    if random.random() < 0.3:
        enemy = {
            "pos": pos,
            "speed": TANK_SPEED,
            "hp": random.randint(2, 3),
            "radius": 26,
            "type": "tank"
        }
    else:
        enemy = {
            "pos": pos,
            "speed": NORMAL_SPEED,
            "hp": 1,
            "radius": 20,
            "type": "normal"
        }

    enemies.append(enemy)

def shoot():
    mouse_pos = pygame.mouse.get_pos()
    direction = pygame.Vector2(mouse_pos) - player_pos
    if direction.length() == 0:
        return

    direction = direction.normalize()

    bullet = {
        "pos": player_pos.copy(),
        "vel": direction * bullet_speed
    }
    bullets.append(bullet)

# ================= MAIN LOOP =================
running = True
while running:
    dt = clock.tick(60) / 1000
    screen.fill(BG_COLOR)

    # -------- EVENT --------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not game_over:
                shoot()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                bullets.clear()
                enemies.clear()
                score = 0
                lives = 3
                game_over = False
                player_pos.update(WIDTH//2, HEIGHT//2)

    # -------- PLAYER MOVE (WASD) --------
    keys = pygame.key.get_pressed()
    move = pygame.Vector2(0, 0)

    if keys[pygame.K_w]:
        move.y -= 1
    if keys[pygame.K_s]:
        move.y += 1
    if keys[pygame.K_a]:
        move.x -= 1
    if keys[pygame.K_d]:
        move.x += 1

    if move.length() > 0:
        move = move.normalize()

    if not game_over:
        player_pos += move * player_speed * 60 * dt

    player_pos.x = max(player_size//2, min(WIDTH - player_size//2, player_pos.x))
    player_pos.y = max(player_size//2, min(HEIGHT - player_size//2, player_pos.y))

    # -------- SPAWN ENEMY --------
    if not game_over:
        spawn_timer += 1
        if spawn_timer >= spawn_delay:
            spawn_timer = 0
            spawn_enemy()

    # -------- UPDATE BULLETS --------
    for bullet in bullets[:]:
        bullet["pos"] += bullet["vel"]

        # Hapus jika keluar layar
        if (bullet["pos"].x < 0 or bullet["pos"].x > WIDTH or
            bullet["pos"].y < 0 or bullet["pos"].y > HEIGHT):
            bullets.remove(bullet)

    # -------- UPDATE ENEMIES (CHASE PLAYER) --------
    for enemy in enemies[:]:
        direction = player_pos - enemy["pos"]
        if direction.length() > 0:
            direction = direction.normalize()

        enemy["pos"] += direction * enemy["speed"] * 60 * dt

        # Collision with player
        if enemy["pos"].distance_to(player_pos) < enemy["radius"] + player_size//2:
            enemies.remove(enemy)
            lives -= 1
            if lives <= 0:
                game_over = True
            continue

        # Collision with bullets
        for bullet in bullets[:]:
            if enemy["pos"].distance_to(bullet["pos"]) < enemy["radius"] + 5:
                bullets.remove(bullet)
                enemy["hp"] -= 1

                if enemy["hp"] <= 0:
                    enemies.remove(enemy)
                    score += 2 if enemy["type"] == "tank" else 1
                break

    # -------- DRAW --------
    draw_player()
    draw_bullets()
    draw_enemies()

    show_text(f"Score: {score}", 10, 10)
    show_text(f"Lives: ❤️ {lives}", 10, 40)

    if game_over:
        show_text("💀 GAME OVER", WIDTH//2 - 120, HEIGHT//2 - 40, RED)
        show_text("Tekan R untuk Restart", WIDTH//2 - 170, HEIGHT//2 + 10)

    pygame.display.flip()

pygame.quit()
sys.exit()
