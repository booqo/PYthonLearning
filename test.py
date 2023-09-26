import pygame, sys, random

skier_images = ["1.png", "2.jpg", "3.jpg", "4.png", "5.png"]


class skierclass(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("1.png")
        self.rect = self.image.get_rect()
        self.rect.center = [320, 100]
        self.angle = 0

    def turn(self, direction):
        self.angle = self.angle + direction
        if self.angle < -2: self.angle = -2
        if self.angle > -2: self.angle = 2
        center = self.rect.center
        self.image = pygame.image.load(skier_images[self.angle])
        self.rect = self.image.get_rect()
        self.rect.center = center
        speed = [self.angle, 6 - abs(self.angle) * 2]
        return speed

    def move(self, speed):
        self.rect.center = self.rect.center + speed[0]
        if self.rect.center < 20: self.rect.center = 20
        if self.rect.center > 620: self.rect.center = 620


class obstacleClass(pygame.sprite.Sprite):
    def __init__(self, image_file, location, obs_type):
        pygame.sprite.Sprite.__init__(self)
        self.image_file = image_file
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.obs_type = obs_type
        self.passed = False

    def update(self):
        global speed
        self.rect.center -= speed[1]
        if self.rect.center < -32:
            self.kill()


def create_map():
    global obstacles
    locations= []
    for i in range(10):
        row = random.randint(0, 9)
        col = random.randint(0, 9)
        location = [col * 64 + 20, row * 64 + 20 + 640]
        if not (location in locations):
            locations.append(location)
            obs_type = random.choice(["tree", "flag"])
            if obs_type == "tree": img = "3.jpg"
            elif obs_type == "flag": img = "4.png"
            obstacle = obstacleClass(img, location, obs_type)
            obstacles.add(obstacle)

def animate():
    screen.fill([255, 255, 255])
    obstacles.draw(screen)
    screen.blit(skier.image, skier.rect)
    screen.blit(score_text, [10, 10])
    pygame.display.flip()

pygame.init()
screen = pygame.display.set_mode([640, 640])
clock = pygame.time.Clock()
skier = skierclass
speed = [0, 6]
obstacles = pygame.sprite.Group
map_position = 0
points = 0
create_map()
font = pygame.font.Font(None, 50)




running = True
while running:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:  # 使用 event.key 来检查按下的键
                speed = skier.turn(-1)
            elif event.key == pygame.K_RIGHT:  # 使用 event.key 来检查按下的键
                speed = skier.turn(1)

    skier.move(speed)  # 传递正确的速度参数给 skier.move()

    # 在这里执行其他游戏逻辑和渲染

    map_position += speed[1]

    if map_position >= 640:
        create_map()
        map_position = 0

    hit = pygame.sprite.spritecollide(skier, obstacles, False)
    if hit:
        if hit[0].obs_type == "tree" and not hit[0].passed:
            points = points - 100
            skier.image = pygame.image.load("2.jpg")
            animate()
            pygame.time.delay(1000)
            skier.image = pygame.image.load("5.png")
            skier.angle = 0
            speed = [0, 6]
            hit[0].passed = True
        elif hit[0].obs_type == "flag" and not hit[0].passed:
            points += 10
            hit[0].kill()
    obstacles.update()
    score_text = font.render("score:" + str(points), 1, (0, 0, 0))
    animate()
pygame.quit()


