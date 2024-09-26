import time
import random
import pygame
from pygame import mixer

pygame.font.init()
mixer.init()
icon = "images/BlockPic.png"
WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Junga")
BG = pygame.transform.scale(pygame.image.load("images/Background.jpg"), (1000, 800))

# SOUNDS
hit_sound = pygame.mixer.Sound('Sounds/end.mp3')
BGM = pygame.mixer.Sound('Sounds/Bg1.mp3')
BGM.play(-1)

# OBJECTS
PLAYER_WIDTH = 30
PLAYER_HEIGHT = 50
PLAYER_VEL = 5

STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 5

FONT = pygame.font.SysFont("comicsans", 30)


def draw(player, elapsed_time, stars):
    WIN.blit(BG, (0, 0))
    time_text = FONT.render(f"Time: {(round(elapsed_time))}s", 1, "white")
    WIN.blit(time_text, (10, 10))
    pygame.draw.rect(WIN, "black", player)
    for star in stars:
        pygame.draw.rect(WIN, "yellow", star)
    pygame.display.update()


def main():
    run = True

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    is_jump = False
    jump_count = 10

    clock = pygame.time.Clock()
    start_time = time.time()

    star_add_increment = 2000
    star_count = 0
    stars = []

    hit = False

    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)
            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                break
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_d] or keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL
        if player.y < 0:
            player.y = 0
        elif player.y > HEIGHT - PLAYER_HEIGHT:
            player.y = HEIGHT - PLAYER_HEIGHT

        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -10:
                neg = 1
                if jump_count < 0:
                    neg = -1
                player.y -= (jump_count ** 2) * 0.5 * neg
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 10

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break
        if hit:
            BGM.stop()
            hit_sound.play()
            lost_text = FONT.render("You Lost!", 1, "Red")
            WIN.blit(lost_text, (WIDTH / 2 - lost_text.get_width() / 2, HEIGHT / 2 - lost_text.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        draw(player, elapsed_time, stars)
    pygame.quit()


if __name__ == "__main__":
    main()
