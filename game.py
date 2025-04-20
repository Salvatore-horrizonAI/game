
import pygame
import sys
import random as rand

#gioco creato da salvatore per scopi personali dare i cr:salvatore-horrinaro
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
screen = pygame.display.set_mode((576, 624))
clock = pygame.time.Clock()


pygame.display.set_caption("Flappy Birdy by Salvatore Naro")
icon = pygame.image.load('C:/Users/salva/Downloads/redbird.png').convert_alpha()
pygame.display.set_icon(icon)



def draw_floor():
    global floor_x_position
    floor_x_position -= 1
    screen.blit(floor_surface, (floor_x_position, 530))
    screen.blit(floor_surface, (floor_x_position + 576, 530))
    if floor_x_position == -576:
        floor_x_position = 0


def draw_bird():
    global bird_movement
    bird_movement += gravity
    rotated_bird = rotate_bird(bird_surface)
    bird_rect.centery += bird_movement
    screen.blit(rotated_bird, bird_rect)


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 624:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird


def create_pipe():
    random_pipe_pos = rand.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_pos - 200))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
    return visible_pipes


def check_collision(pipes):
    global can_score
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            can_score = True
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 530:
        can_score = True
        return False
    return True


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


def show_text(text, pos, color, font_size):
    game_font = pygame.font.Font("04B_19.TTF", font_size)
    score_surface = game_font.render(text, True, color)
    score_rect = score_surface.get_rect(center=pos)
    screen.blit(score_surface, score_rect)


def score_display(game_state):
    show_text(f"Score: {int(score)}", (288, 100), (255, 255, 255), 35)
    if game_state == "game_over":
        show_text(f"Highest score: {int(highest_score)}", (288, 450), (255, 255, 255), 35)


def score_check():
    global score, can_score
    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105 and can_score:
                score += 1
                score_sound.play()
                can_score = False
            if pipe.centerx < 0:
                can_score = True



gravity = 0.25
bird_movement = 0
game_active = True
highest_score = 0
score = 0
can_score = True


bg_surface = pygame.image.load("day.png").convert()
bg_surface = pygame.transform.scale2x(bg_surface)


floor_surface = pygame.image.load("base.png").convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_position = 0


bird_downflap = pygame.transform.scale2x(pygame.image.load("bluebird-downflap.png").convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load("bluebird-midflap.png").convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load("bluebird-upflap.png").convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap]

bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 312))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

pipe_surface = pygame.image.load("pipe-green.png")
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
pipe_height = [250, 350, 450]

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)


flap_sound = pygame.mixer.Sound("sfx_wing.wav")
flap_sound.set_volume(0.08)

death_sound = pygame.mixer.Sound("sfx_hit.wav")
death_sound.set_volume(0.05)

score_sound = pygame.mixer.Sound("sfx_point.wav")
score_sound.set_volume(0.02)
score_sound_countdown = 100


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 7
                flap_sound.play()
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 312)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            bird_index += 1
            bird_index %= 3
            bird_surface, bird_rect = bird_animation()

    screen.blit(bg_surface, (0, -350))
    draw_floor()

    if game_active:
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        draw_bird()
        game_active = check_collision(pipe_list)

        score_check()
        score_display("main_game")
    else:
        show_text("Game Over", (288, 260), (255, 0, 0), 60)
        show_text("(Gioco sviluppato da Salvatore)", (288, 300), (255, 0, 0), 25)
        if score > highest_score:
            highest_score = score
        score_display("game_over")
    pygame.display.update()
    clock.tick(120)
