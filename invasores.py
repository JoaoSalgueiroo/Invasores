import pygame
import random

pygame.init()

WIDTH = 1920
HEIGHT = 1080

screen = pygame.display.set_mode((WIDTH,HEIGHT))


clock = pygame.time.Clock()

class Enemy:
    def __init__(self,position):
        self.position = position
        self.color = (random.randint(0, 255), random.randint(0, 200), random.randint(0, 255))  # Unique color
    def draw(self):
        x = self.position[0]
        y = self.position[1]
        pygame.draw.rect(screen, (self.color), pygame.Rect(x,y,50,50))
    def get_position(self):
        return [self.position[0],self.position[1]] 


class Projectile:
    def __init__(self, position):
        self.position = list(position)
    def draw(self):
        x = self.position[0]
        y = self.position[1]
        pygame.draw.circle(screen, (200,0,0), (x,y), 10)


class Spaceship:
    def __init__(self, color, position):
        self.color = color
        self.position = list(position)
    def create(self):
        x = self.position[0]
        y = self.position[1]
        pygame.draw.rect(screen,self.color,pygame.Rect(x,y,100,20))
    def move(self):
        if key[pygame.K_d]:
            self.position[0] += 8
        elif key[pygame.K_a]:
            self.position[0] -= 8
    def outofbounds(self):
        if self.position[0] >= WIDTH - 200:
            self.position[0] = WIDTH - 200
        elif self.position[0] <= 0:
            self.position[0] = 0
    def get_position(self):
        return [self.position[0]+50,self.position[1]] 

def random_position():
    x = random.randint(300,1620)
    y = 0
    return [x, y]

def scoreboard(kill_counter,lifes):
    font1 = pygame.font.SysFont("HomeVideo",100)
    font2 = pygame.font.SysFont("HomeVideo",30)
    x = 1800
    if kill_counter > 999:
        x = 1650
    elif kill_counter > 99:
        x = 1700
    elif kill_counter > 9:
        x = 1750
    x2 = 1790
    if lifes < 10:
        x2 += 7
    score_table = font1.render(f"{kill_counter}", True, (250,250,250))
    life_table = font2.render(f"HP{lifes}", True, (250,250,250))
    screen.blit(score_table, (x,50))
    screen.blit(life_table, (x2, 150))


def end_screen(kill_counter, current_time):
    mock_time = current_time + 5000
    print("YOU LOST!")
    font = pygame.font.SysFont("HomeVideo",100) 
    end_screen1 = font.render(f"YOU LOST!", True, (250,250,250))
    end_screen2 = font.render(f"Score {kill_counter}", True, (250,250,250))
    while current_time < mock_time:
        current_time = pygame.time.get_ticks()
        screen.fill((0,0,0))
        screen.blit(end_screen1, (end_screen1.get_rect(center=(WIDTH/2, HEIGHT/2-100))))
        screen.blit(end_screen2, (end_screen2.get_rect(center=(WIDTH/2, HEIGHT/2+100))))
        pygame.display.update()
    return


ship = Spaceship(color = (0,100,0), position = (WIDTH//2,HEIGHT-20))
bullets = []
enemies = []
mock_time = 0  
lifes = 10
kill_counter = 0
time = 3000

run = True
while run:

    screen.fill((0,0,0))

    key = pygame.key.get_pressed()

    current_time = pygame.time.get_ticks()

    if current_time - mock_time >= time:
        time -= 200 
        if time <= 500:
            time = 500
        mock_time = current_time
        enemies.append(Enemy(random_position()))

    ship.create()
    ship.move()
    ship.outofbounds()
    
    color = (random.randint(0,200),random.randint(0,200),random.randint(0,200))

    for enemy in enemies:
        enemy.position[1] += 3
        enemy.draw()
        enemy_rect = pygame.Rect(enemy.position[0], enemy.position[1],50,50)
        for bullet in bullets:
            bullet_rect = pygame.Rect(bullet.position[0] - 5, bullet.position[1] - 5, 10, 10)
            if (enemy_rect.colliderect(bullet_rect)):
                enemies.remove(enemy) 
                bullets.remove(bullet)
                kill_counter +=1
        if enemy.position[1] >= HEIGHT:
            enemies.remove(enemy)
            lifes -=1

    for bullet in bullets:
        bullet.position[1] -= 10
        bullet.draw()

        if bullet.position[1] < -10:
            bullets.remove(bullet)

    scoreboard(kill_counter,lifes)

    if lifes <= 0:
        end_screen(kill_counter,current_time)
        run = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append(Projectile(ship.get_position()))

    pygame.display.update()
    clock.tick(60)

pygame.quit()

