import pygame
import sys
import random

pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Turn-Based Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 100, 255)
RED = (255, 80, 80)
GREEN = (0, 255, 0)

# Fonts
font = pygame.font.Font("pokemon-bw.otf", 36)

# Game State
game_state = "title"   # title → battle

# 캐릭터 스텟
maxPlayer_hp = 100
player_hp = 100
player_damage = 15

# 상대 스텟 
level = 1
maxEnemy_hp = 100
enemy_hp = 100
enemy_damage = 10


turn = "player"

# Buttons
start_button = pygame.Rect(300, 250, 200, 60)
attack_button = pygame.Rect(500, 470, 200, 50)
heal_button   = pygame.Rect(500, 530, 200, 50)

# 기본 텍스트 출력
def draw_text(text, x, y, color):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# 데미지 텍스트 (떠올랐다 사라짐)
class DamageText:
    def __init__(self, text, x, y):
        self.text = text
        self.x = x
        self.y = y
        self.timer = 60

        if text.startswith("+"):
            self.color = (0, 180, 0)
        else:
            self.color = (255, 0, 0)

    def update(self):
        self.y -= 0.5
        self.timer -= 1

    def draw(self):
        img = font.render(self.text, True, self.color)
        screen.blit(img, (self.x, self.y))

damage_texts = []
clock = pygame.time.Clock()
running = True

while running:
    screen.fill(WHITE)

    # ===============================
    # 1) 타이틀 화면
    # ===============================
    if game_state == "title":
        draw_text("게임 이름 뭐하지", 190, 140, BLACK)

        pygame.draw.rect(screen, (200, 200, 200), start_button)
        draw_text("게임 시작", 330, 260, BLACK)

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    game_state = "battle"

        pygame.display.update()
        clock.tick(60)
        continue  # battle 코드 실행 막기

    # ===============================
    # 2) 전투 화면
    # ===============================

    # HP Bar (Player)
    pygame.draw.rect(screen, (5,5,5), (498, 338, 204, 34))
    pygame.draw.rect(screen, (220,220,220), (500, 340, 200, 30))
    pygame.draw.rect(screen, GREEN, (500, 340, 200 * (player_hp/maxPlayer_hp), 30))
    draw_text("Player", 500, 300, BLACK)
    draw_text("HP", 470, 337, BLACK)
    draw_text(f"{player_hp}/{maxPlayer_hp}", 500, 370, BLACK)

    # HP Bar (Enemy)
    pygame.draw.rect(screen, (5,5,5), (98, 68, 204, 34))
    pygame.draw.rect(screen, (220,220,220), (100, 70, 200, 30))
    pygame.draw.rect(screen, GREEN, (100, 70, 200 * (enemy_hp/maxEnemy_hp), 30))
    draw_text(f"Enemy Lv.{level}", 100, 30, BLACK)
    draw_text("HP", 70, 67, BLACK)

    # Enemy
    pygame.draw.ellipse(screen, (180, 180, 180), (510, 190, 200, 60))
    pygame.draw.rect(screen, RED, (550, 100, 120, 120))

    # Player
    pygame.draw.ellipse(screen, (180, 180, 180), (60, 400, 230, 80))
    pygame.draw.rect(screen, BLUE, (100, 290, 150, 150))

    # ======================
    # Player Turn
    # ======================
    if turn == "player":
        draw_text("Player Turn", 320, 120, BLACK)

        pygame.draw.rect(screen, (200,200,200), attack_button)
        draw_text("Attack", 560, 475, BLACK)

        pygame.draw.rect(screen, (200,200,200), heal_button)
        draw_text("Heal", 570, 535, BLACK)

    # ======================
    # Enemy Turn
    # ======================
    else:
        draw_text("Enemy Turn", 320, 120, BLACK)
        pygame.time.delay(700)

        action = random.choice(["attack", "attack", "heal"])

        if action == "attack":
            player_hp -= enemy_damage
            damage_texts.append(DamageText("-10", 100, 330))
        else:
            if enemy_hp >= maxEnemy_hp:
                pass
            else:
                enemy_hp += 5
                damage_texts.append(DamageText("+5", 550, 80))

        turn = "player"

    # ======================
    # Mouse Input
    # ======================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and turn == "player":
            if attack_button.collidepoint(event.pos):
                enemy_hp -= player_damage
                damage_texts.append(DamageText("-15", 550, 80))
                turn = "enemy"

            if heal_button.collidepoint(event.pos):
                if player_hp >= maxPlayer_hp:
                    pass
                else:
                    player_hp += 10
                    damage_texts.append(DamageText("+10", 100, 330))
                turn = "enemy"

    # ======================
    # Damage Text Update
    # ======================
    for dt in damage_texts[:]:
        dt.update()
        dt.draw()
        if dt.timer <= 0:
            damage_texts.remove(dt)

    # ======================
    # Message Box
    # ======================
    pygame.draw.rect(screen, WHITE, (10, 470, 450, 120))
    pygame.draw.rect(screen, BLACK, (10, 470, 450, 120), 4)

    if turn == "player":
        draw_text("무엇을 할까?", 30, 490, BLACK)
    else:
        draw_text("적 행동 중...", 30, 490, BLACK)

    # ======================
    # Win / Lose
    # ======================
    if player_hp <= 0:
        screen.fill(WHITE)
        draw_text("You Lose!", 330, 250, BLACK)
        pygame.display.update()
        pygame.time.delay(2000)

        # 초기화 후 타이틀로 복귀
        player_hp = maxPlayer_hp
        enemy_hp = maxEnemy_hp
        turn = "player"
        game_state = "title"
        continue

    if enemy_hp <= 0:
        screen.fill(WHITE)
        draw_text("You Win!", 330, 250, BLACK)
        pygame.display.update()
        pygame.time.delay(2000)

        # 다음 전투를 위해 초기화
        level += 1              
        maxEnemy_hp += 20       
        enemy_damage += 2       
        enemy_hp = maxEnemy_hp

        player_hp = maxPlayer_hp
        turn = "player"
        game_state = "title"
        continue


    pygame.display.update()
    clock.tick(60)
