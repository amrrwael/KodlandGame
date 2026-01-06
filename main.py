import pgzrun
import math
import random
from pygame import Rect

# Game constants
WIDTH = 800
HEIGHT = 600
PlayerSpeed = 5
BulletSpeed = 10
EnemySpeed = 1
BossSpeed = 0.5
BossSpawnTime = 10  #In Seconds
WinningScore = 500 # Change the diffculity by increasing the number

Menu = 0
Playing = 1
GameOver = 2
GameWin = 3

MusicOn = True
SoundOn = True

GameState = Menu
score = 0
PlayerHealth = 100

# Global variables for mouse position
mouse_x, mouse_y = WIDTH // 2, HEIGHT // 2

class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.width = 30
        self.height = 30
        self.speed = PlayerSpeed
        self.idle_sprites = [Actor('ladybug_rest'), Actor('ladybug_fly')]
        self.move_sprites = [Actor('ladybug_walk_a'), Actor('ladybug_walk_b')]
        self.animation_frame = 0
        self.animation_timer = 0
        self.moving = False

    def update(self):
        #Handle keyboard Movements
        moving = False
        if keyboard.RIGHT or keyboard.d:
            self.x += self.speed
            moving = True
        if keyboard.LEFT or keyboard.a:
            self.x -= self.speed
            moving = True
        if keyboard.UP or keyboard.w:
            self.y -= self.speed
            moving = True
        if keyboard.DOWN or keyboard.s:
            self.y += self.speed
            moving = True
        self.moving = moving

        self.x = max(self.width/2, min(WIDTH - self.width/2, self.x))
        self.y = max(self.height/2, min(HEIGHT - self.height/2, self.y))

        self.animation_timer += 1
        if self.animation_timer >= 10:
            self.animation_frame = (self.animation_frame + 1) % 2
            self.animation_timer = 0

    def draw(self):
        angle = math.degrees(math.atan2(mouse_y - self.y, mouse_x - self.x))
        sprite = self.move_sprites[self.animation_frame] if self.moving else self.idle_sprites[self.animation_frame]
        sprite.pos = (self.x, self.y)
        sprite.angle = -angle
        sprite.draw()

class Bullet:
    def __init__(self, x, y, mouse_x, mouse_y):
        self.x = x
        self.y = y
        self.radius = 5
        self.speed = BulletSpeed
        dx = mouse_x - x
        dy = mouse_y - y
        distance = math.hypot(dx, dy)
        self.dx = (dx / distance) * self.speed if distance != 0 else 0
        self.dy = (dy / distance) * self.speed if distance != 0 else 0

    def update(self):
        self.x += self.dx
        self.y += self.dy
        return 0 <= self.x <= WIDTH and 0 <= self.y <= HEIGHT

    def draw(self):
        screen.draw.filled_circle((self.x, self.y), self.radius, (255, 255, 0))

class Enemy:
    def __init__(self):
        edge = random.randint(0, 3)
        if edge == 0:
            self.x = random.randint(0, WIDTH)
            self.y = -20
        elif edge == 1:
            self.x = WIDTH + 20
            self.y = random.randint(0, HEIGHT)
        elif edge == 2:
            self.x = random.randint(0, WIDTH)
            self.y = HEIGHT + 20
        else:
            self.x = -20
            self.y = random.randint(0, HEIGHT)
        self.width = 25
        self.height = 25
        self.speed = EnemySpeed
        self.move_sprites = [Actor('fly_a'), Actor('fly_b')]
        self.animation_frame = 0
        self.animation_timer = 0

    def update(self, player_x, player_y):
        # Move towards player
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.hypot(dx, dy)
        if distance != 0:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed

        self.animation_timer += 1
        if self.animation_timer >= 15:
            self.animation_frame = (self.animation_frame + 1) % 2
            self.animation_timer = 0

    def draw(self):
        sprite = self.move_sprites[self.animation_frame]
        sprite.pos = (self.x, self.y)
        sprite.draw()

class Boss:
    def __init__(self):
        # Boss starts Left side
        self.x = 50
        self.y = HEIGHT // 2
        self.width = 80
        self.height = 80
        self.speed = BossSpeed
        self.health = 100
        self.max_health = 100
        self.move_sprites = [Actor('slime_fire_walk_a'), Actor('slime_fire_walk_b')]
        self.animation_frame = 0
        self.animation_timer = 0

    def update(self, player_x, player_y):
        # Boss slowly pursues the player
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.hypot(dx, dy)
        if distance != 0:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
        self.animation_timer += 1
        if self.animation_timer >= 20:
            self.animation_frame = (self.animation_frame + 1) % 2
            self.animation_timer = 0

    def draw(self):
        # Draw boss health bar
        bar_width = self.width
        bar_height = 10
        bar_x = self.x - bar_width // 2
        bar_y = self.y - self.height // 2 - 15
        screen.draw.filled_rect(Rect(bar_x, bar_y, bar_width, bar_height), (255, 0, 0))
        health_width = max(0, int(bar_width * (self.health / self.max_health)))
        screen.draw.filled_rect(Rect(bar_x, bar_y, health_width, bar_height), (0, 255, 0))
        # Draw boss Char
        sprite = self.move_sprites[self.animation_frame]
        sprite.pos = (self.x, self.y)
        sprite.draw()

class Coin:
    def __init__(self):
        # Place Coins in Random PLcaces
        self.x = random.randint(50, WIDTH - 50)
        self.y = random.randint(50, HEIGHT - 50)
        self.radius = 8

    def draw(self):
        screen.draw.filled_circle((self.x, self.y), self.radius, (255, 215, 0))
        screen.draw.circle((self.x, self.y), self.radius, (200, 170, 0))

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = Rect(x, y, width, height)
        self.text = text
        self.hovered = False

    def draw(self):
        color = (100, 100, 255) if self.hovered else (70, 70, 200)
        screen.draw.filled_rect(self.rect, color)
        screen.draw.rect(self.rect, (200, 200, 255))
        text_width = len(self.text) * 10
        text_x = self.rect.centerx - text_width // 2
        text_y = self.rect.centery - 7
        screen.draw.text(self.text, (text_x, text_y), color="white")

    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        return self.hovered

# Game objects
player = Player()
bullets = []
enemies = []
coins = []
boss = None
BossSpawnTimer = 0

# Buttons for Menu
start_button = Button(WIDTH//2 - 75, HEIGHT//2 - 50, 150, 40, "Start Game")
music_button = Button(WIDTH//2 - 75, HEIGHT//2, 150, 40, "Music: ON")
sound_button = Button(WIDTH//2 - 75, HEIGHT//2 + 50, 150, 40, "Sound: ON")
exit_button = Button(WIDTH//2 - 75, HEIGHT//2 + 100, 150, 40, "Exit Game")

# Music variables
current_music = None
boss_music_playing = False
music_volume = 0.7

def play_sound(sound_name):
    global SoundOn
    if SoundOn:
        try:
            if sound_name == 'shoot':
                sounds.shoot.play()
            elif sound_name == 'hit':
                sounds.hit.play()
        except:
            pass

def play_music(music_name):
    global current_music, MusicOn, boss_music_playing
    if MusicOn:
        try:
            if current_music != music_name:
                music.play(music_name)
                music.set_volume(music_volume)
                current_music = music_name
                boss_music_playing = (music_name == 'boss')
        except Exception as e:
            print(f"Error playing music: {e}")
    else:
        stop_music()

def stop_music():
    global current_music, boss_music_playing
    try:
        music.stop()
    except:
        pass
    current_music = None
    boss_music_playing = False

def set_music_volume(volume):
    global music_volume
    music_volume = max(0.0, min(1.0, volume))
    try:
        music.set_volume(music_volume)
    except:
        pass

def draw():
    ProgressWidth = 200
    ProgressHeight = 15
    ProgressX = WIDTH - ProgressWidth - 10
    ProgressY = 45
    progress = min(1.0, score / WinningScore)
    screen.fill((18, 12, 36))  

    if GameState == Menu:
        screen.draw.text("Top-Down Shooter", (WIDTH//2 - 120, HEIGHT//4), fontsize=40, color=(255, 95, 135))
        start_button.draw()
        music_button.draw()
        sound_button.draw()
        exit_button.draw()
    elif GameState == Playing:
        player.draw()
        for bullet in bullets:
            bullet.draw()
        for enemy in enemies:
            enemy.draw()
        if boss is not None:
            boss.draw()
        for coin in coins:
            coin.draw()
        screen.draw.text(f"Score: {score}", (10, 10), fontsize=30, color=(102, 255, 255))
        screen.draw.text(f"Health: {PlayerHealth}", (10, 40), fontsize=30, color=(255, 165, 0))
        screen.draw.text(f"Target: {WinningScore}", (WIDTH - 200, 10), fontsize=30, color=(255, 215, 0))
        screen.draw.filled_rect(Rect(ProgressX, ProgressY, ProgressWidth, ProgressHeight), (50, 50, 50))
        screen.draw.filled_rect(Rect(ProgressX, ProgressY, int(ProgressWidth * progress), ProgressHeight), (0, 255, 0))
        screen.draw.rect(Rect(ProgressX, ProgressY, ProgressWidth, ProgressHeight), (200, 200, 200))
        screen.draw.line((mouse_x - 10, mouse_y), (mouse_x + 10, mouse_y), (57, 255, 20))
        screen.draw.line((mouse_x, mouse_y - 10), (mouse_x, mouse_y + 10), (57, 255, 20))
    elif GameState == GameOver:
        screen.draw.text("GAME OVER", (WIDTH//2 - 120, HEIGHT//2 - 50), fontsize=60, color=(255, 50, 50))
        screen.draw.text(f"Final Score: {score}", (WIDTH//2 - 90, HEIGHT//2 + 10), fontsize=40, color=(255, 220, 180))
        screen.draw.text("Press SPACE to return to Menu", (WIDTH//2 - 180, HEIGHT//2 + 60), fontsize=30, color=(180, 255, 255))
    elif GameState == GameWin:
        screen.draw.text("VICTORY!", (WIDTH//2 - 100, HEIGHT//2 - 80), fontsize=70, color=(255, 215, 0))
        screen.draw.text("YOU WIN!", (WIDTH//2 - 90, HEIGHT//2 - 10), fontsize=60, color=(50, 255, 100))
        screen.draw.text(f"Final Score: {score}", (WIDTH//2 - 90, HEIGHT//2 + 50), fontsize=40, color=(255, 220, 180))
        screen.draw.text("Press SPACE to return to Menu", (WIDTH//2 - 180, HEIGHT//2 + 100), fontsize=30, color=(180, 255, 255))

def update():
    global GameState, PlayerHealth, score, boss, BossSpawnTimer

    if GameState == GameWin or GameState == GameOver:
        return

    if GameState != Playing:
        return

    player.update()
    bullets[:] = [b for b in bullets if b.update()]

    for enemy in enemies:
        enemy.update(player.x, player.y)
        if Rect(player.x - player.width/2, player.y - player.height/2, player.width, player.height).colliderect(
           Rect(enemy.x - enemy.width/2, enemy.y - enemy.height/2, enemy.width, enemy.height)):
            PlayerHealth -= 1
            play_sound('hit')
            if PlayerHealth <= 0:
                GameState = GameOver

    if boss is not None:
        boss.update(player.x, player.y)
        player_rect = Rect(player.x - player.width/2, player.y - player.height/2, player.width, player.height)
        boss_rect = Rect(boss.x - boss.width/2, boss.y - boss.height/2, boss.width, boss.height)
        if player_rect.colliderect(boss_rect):
            PlayerHealth -= 2
            play_sound('hit')
            if PlayerHealth <= 0:
                GameState = GameOver

    # Bullet collisions with enemies & boss
    bullets_to_remove = []
    enemies_to_remove = []
    for i, bullet in enumerate(bullets):
        bullet_rect = Rect(bullet.x - bullet.radius, bullet.y - bullet.radius, bullet.radius*2, bullet.radius*2)
        for j, enemy in enumerate(enemies):
            enemy_rect = Rect(enemy.x - enemy.width/2, enemy.y - enemy.height/2, enemy.width, enemy.height)
            if bullet_rect.colliderect(enemy_rect) and j not in enemies_to_remove:
                bullets_to_remove.append(i)
                enemies_to_remove.append(j)
                score += 5
                play_sound('hit')
        if boss is not None:
            boss_rect = Rect(boss.x - boss.width/2, boss.y - boss.height/2, boss.width, boss.height)
            if bullet_rect.colliderect(boss_rect):
                boss.health -= 5
                bullets_to_remove.append(i)
                score += 10
                play_sound('hit')
                if boss.health <= 0:
                    boss = None
                    score += 50
                    # Switch back to background music when bosss is defeated
                    play_music('backgroundd')
                    break

    for i in reversed(bullets_to_remove):
        if i < len(bullets):
            del bullets[i]
    for i in reversed(enemies_to_remove):
        if i < len(enemies):
            del enemies[i]

    # Spawn enemies & Coins randomly
    if random.random() < 0.02:
        enemies.append(Enemy())
    if random.random() < 0.005:
        coins.append(Coin())

    BossSpawnTimer += 1/60  # 60FPS
    if BossSpawnTimer >= BossSpawnTime:
        BossSpawnTimer = 0
        if boss is None:
            boss = Boss()
            play_music('boss')
        elif boss and not boss_music_playing:
            play_music('boss')

    # Coin Collection
    player_rect = Rect(player.x - player.width/2, player.y - player.height/2, player.width, player.height)
    coins_to_remove = [i for i, coin in enumerate(coins)
                       if player_rect.colliderect(Rect(coin.x - coin.radius, coin.y - coin.radius, coin.radius*2, coin.radius*2))]
    for i in reversed(coins_to_remove):
        if i < len(coins):
            del coins[i]
            score += 10
    if score >= WinningScore:
        GameState = GameWin
        stop_music()

def on_key_down(key):
    global GameState, PlayerHealth, score, boss, BossSpawnTimer
    # Reset Game
    if (GameState == GameOver or GameState == GameWin) and key == keys.SPACE:
        player.x = WIDTH // 2
        player.y = HEIGHT // 2
        PlayerHealth = 100
        score = 0
        bullets.clear()
        enemies.clear()
        coins.clear()
        boss = None
        BossSpawnTimer = 0
        stop_music()
        play_music('backgroundd')
        GameState = Menu

def on_mouse_down(pos, button):
    global GameState, MusicOn, SoundOn
    if GameState == Menu:
        if start_button.check_hover(pos):
            GameState = Playing
            play_music('backgroundd')
        elif music_button.check_hover(pos):
            MusicOn = not MusicOn
            music_button.text = f"Music: {'ON' if MusicOn else 'OFF'}"
            if MusicOn:
                if GameState == Playing:
                    if boss:
                        play_music('boss')
                    else:
                        play_music('backgroundd')
            else:
                stop_music()
        elif sound_button.check_hover(pos):
            SoundOn = not SoundOn
            sound_button.text = f"Sound: {'ON' if SoundOn else 'OFF'}"
        elif exit_button.check_hover(pos):
            exit()
    elif GameState == Playing and button == mouse.LEFT:
        # Fire bullet Toward Mouse Position
        bullets.append(Bullet(player.x, player.y, pos[0], pos[1]))
        play_sound('shoot')

def on_mouse_move(pos):
    global mouse_x, mouse_y
    # Track Mouse Position
    mouse_x, mouse_y = pos
    if GameState == Menu:
        start_button.check_hover(pos)
        music_button.check_hover(pos)
        sound_button.check_hover(pos)
        exit_button.check_hover(pos)

set_music_volume(0.7)

pgzrun.go()