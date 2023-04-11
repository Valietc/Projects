import pygame
import sys
import random


def game_floor():
    screen.blit(floor_base, (floor_x_pos, 600))
    screen.blit(floor_base, (floor_x_pos + 576, 600))


def check_collision(exams):
    # Условия столкновений с полом, потолком и экзаменами
    for exam in exams:
        if petr_rect.colliderect(exam):
            return False

    if petr_rect.top <= 0 or petr_rect.bottom >= 750:
        return False
    return True


def create_exam(exams):
    # Создание экзаменов
    random_exam_pos = random.choice(exam_height)
    top_exam = exam_surface.get_rect(midbottom=(700, random_exam_pos - 300))
    bottom_exam = exam_surface.get_rect(midtop=(700, random_exam_pos))
    return bottom_exam, top_exam


def move_exams(exams):
    # Движение экзаменов
    for exam in exams:
        exam.centerx -= 5

    return exams


def draw_exams(exams):
    # Ориентация в пространстве
    for exam in exams:
        if exam.bottom >= 600:
            screen.blit(exam_surface, exam)
        else:
            flip_exam = pygame.transform.flip(exam_surface, False, True)
            screen.blit(flip_exam, exam)


pygame.init()
clock = pygame.time.Clock()
# переменные
gravity = 0.25
petr_movement = 0
screen = pygame.display.set_mode((576, 800))
#
background = pygame.image.load("assets/gz.jpg").convert()

petr = pygame.image.load("assets/petr.png").convert_alpha()
petr = pygame.transform.scale(petr, (80, 48))
petr_rect = petr.get_rect(center=(100, 400))

floor_base = pygame.image.load("assets/floor.png").convert_alpha()
floor_base = pygame.transform.scale(floor_base, (576, 350))
floor_x_pos = 0

message = pygame.image.load("assets/message.png").convert_alpha()
game_over_rect = message.get_rect(center=(288, 400))

exam_surface = pygame.image.load("assets/exam1.png")
exam_surface = pygame.transform.scale(exam_surface, (100, 350))
exam_list = []
exam_height = [400, 475, 600]
SPAWNEXAM = pygame.USEREVENT
pygame.time.set_timer(SPAWNEXAM, 1200)
# Зацикливание
game_active = True
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                petr_movement = 0
                petr_movement -= 10
            if event.key == pygame.K_SPACE and game_active == False:
                petr_rect.center = (100, 400)
                petr_movement = 0
                exam_list.clear()
                game_active = True
        if event.type == SPAWNEXAM and game_active:
            exam_list.extend(create_exam(exam_list))
    screen.blit(background, (0, 0))
    if game_active:
        petr_movement += gravity
        petr_rect.centery += petr_movement
        screen.blit(petr, petr_rect)

        exam_list = move_exams(exam_list)
        draw_exams(exam_list)
        game_active = check_collision(exam_list)
    else:
        screen.blit(message, game_over_rect)

    floor_x_pos -= 1
    game_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0
    pygame.display.update()
    clock.tick(90)
