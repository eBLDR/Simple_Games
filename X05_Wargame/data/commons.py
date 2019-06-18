import math as m
import random
import sys

import pygame
from X05_Wargame.data import squad
from X05_Wargame.data import player, battle

# ------------------------------ CONSTANTS
map_W = 1536
map_H = 1024

# No full screen mode
# screen_W = 0  # 1280
# screen_H = 0  # 704

INIT_CAMERA = (0, 0)
CAMERA_JUMP = 2  # divisible by map_W and map_H (W,H%CAMERA_JUMP = 0)

MARGIN = 32

FPS = 30

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (180, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 155)
GRAY = (128, 128, 128)


# ------------------------------ GAME CLASS
class Game:
    def __init__(self):
        self.players = []
        self.current_player = None
        self.phase = None  # PREPARE, MOVEMENT, DIST_ATTACK, MELEE_SOLVE, CHECK_DEATH
        self.last_action = 'Peace'

    @staticmethod
    def set_players(num):
        for n in range(0, num):
            game.players.append(player.Player(n + 1, 'Player_{}'.format(n + 1)))

    def who_starts(self):
        self.current_player = random.randint(1, len(self.players))

    def next_phase(self):
        clean_highlights()

        if self.phase == 'PREPARING...':
            self.phase = 'MOVEMENT'

        elif self.phase == 'MOVEMENT':
            self.phase = 'DIST ATK'

        elif self.phase == 'DIST ATK':
            self.phase = 'SOLVE MELEE'

        elif self.phase == 'SOLVE MELEE':
            if all_combats_solved():
                self.phase = 'CHECK DEATH'
            else:
                self.last_action = 'Still combats for solving'

        elif self.phase == 'CHECK DEATH':
            while True:
                self.current_player += 1
                self.current_player = self.current_player % len(self.players)
                if self.current_player == 0:
                    self.current_player = len(self.players)
                if not self.players[self.current_player - 1].is_death:
                    break

            self.phase = 'PREPARING...'


# ------------------------------ CAMERA CLASS
class Camera:
    def __init__(self):
        self.X, self.Y = INIT_CAMERA

    def update(self, direction):
        if direction == 'right':
            if self.X + CAMERA_JUMP <= map_H - screen_W:
                self.X += CAMERA_JUMP
                return True

        elif direction == 'down':
            if self.Y + CAMERA_JUMP <= map_H - screen_H:
                self.Y += CAMERA_JUMP
                return True

        elif direction == 'left':
            if self.X - CAMERA_JUMP >= 0:
                self.X -= CAMERA_JUMP
                return True

        elif direction == 'up':
            if self.Y - CAMERA_JUMP >= 0:
                self.Y -= CAMERA_JUMP
                return True


# ------------------------------ INIT/EXIT FUNCTIONS
def init_game():
    pygame.mixer.music.play(-1, 0.0)
    num_of_players = 3
    game.set_players(num_of_players)
    game.who_starts()
    set_army()
    game.phase = 'PREPARING...'


def exit_game():
    pygame.mixer.music.stop()
    pygame.quit()
    sys.exit()


# ------------------------------ SET GAME FUNCTIONS
def set_bg_texture():
    return random.choice(
        ['grass00', 'snow00', 'sand00']
    )


def set_music():
    return random.choice(
        ['douce_dame_jolie_tocs_occitans']
    )


# ------------------------------ RUN GAME FUNCTION
def run_game(mouse_x, mouse_y, mouse_clicked, arrow_pressed):
    if game.phase == 'PREPARING...':
        prepare_phase()
    elif game.phase == 'MOVEMENT':
        movement_phase(mouse_x, mouse_y, mouse_clicked, arrow_pressed)
    elif game.phase == 'DIST ATK':
        dist_attack_phase(mouse_x, mouse_y, mouse_clicked)
    elif game.phase == 'SOLVE MELEE':
        solve_melee_phase(mouse_x, mouse_y, mouse_clicked)
    elif game.phase == 'CHECK DEATH':
        check_death()

    blit()
    pygame.display.update()
    fpsClock.tick(FPS)


# ------------------------------ CAMERA FUNCTIONS
def move_camera(direction):
    delta_x = delta_y = None

    if direction == 'right' and camera.update(direction):
        delta_x = - CAMERA_JUMP

    elif direction == 'up' and camera.update(direction):
        delta_y = CAMERA_JUMP

    elif direction == 'left' and camera.update(direction):
        delta_x = CAMERA_JUMP

    elif direction == 'down' and camera.update(direction):
        delta_y = - CAMERA_JUMP

    for p in game.players:
        for s in p.army:
            s.move_squad(s.pos[0][0] + delta_x, s.pos[0][1] + delta_y)


# ------------------------------ BLIT FUNCTION
def blit():
    screen.fill(BLACK)

    for e in range(0, map_W, bg.get_width()):
        for f in range(0, map_H, bg.get_height()):
            screen.blit(bg, (e - camera.X, f - camera.Y))

    # Screen border
    pygame.draw.rect(screen, BLACK, (MARGIN - camera.X, MARGIN - camera.Y, map_W - (MARGIN * 2), map_H - (MARGIN * 2)), 3)

    display_player_phase_surf = display_player_phase.render('Ply %i: %s' % (game.current_player, game.phase), True, BLACK)
    display_player_phase_rect = display_player_phase_surf.get_rect(topleft=(MARGIN + 4, MARGIN + 4))
    display_gen_info_surf = display_gen_info.render('%s' % game.last_action, True, BLACK)
    display_gen_info_rect = display_gen_info_surf.get_rect(topleft=(MARGIN + 4, MARGIN + 30))
    screen.blit(display_player_phase_surf, display_player_phase_rect)
    screen.blit(display_gen_info_surf, display_gen_info_rect)

    for p in game.players:
        for s in p.army:
            if s.units > 0:
                screen.blit(s.img, s.pos[1])
                show_squad_info(s)
                if s.mouse_over or s.is_selected:
                    show_highlight(s)


# ------------------------------ PHASE FUNCTIONS
def next_phase():
    game.next_phase()


def prepare_phase():
    for p in game.players:
        for s in p.army:
            s.mouse_over = s.is_selected = s.engaged = False

    for s in game.players[(game.current_player - 1)].army:
        s.can_range_attack = True if s.get_dR() != 0 else False
        s.can_move = s.can_rotate = s.can_melee_attack = True
        check_collision(s)

    blit()
    pygame.display.update()
    tubular_bell_sound.play()
    pygame.time.wait(600)
    next_phase()


def movement_phase(mouse_x, mouse_y, mouse_clicked, arrow_pressed):
    if not mouse_clicked and not arrow_pressed:
        for p in game.players:
            for s in p.army:
                if s.pos[1].collidepoint(mouse_x, mouse_y):  # show highlight
                    s.mouse_over = True
                elif s.mouse_over:  # clean highlights
                    s.mouse_over = False

    elif mouse_clicked:
        for s in game.players[(game.current_player - 1)].army:
            if mouse_clicked == 'LEFT' and (s.can_move or s.can_rotate):

                # Check if selected
                if not s.is_selected and s.pos[1].collidepoint(mouse_x, mouse_y):
                    s.is_selected = True

                elif s.is_selected and s.can_move and is_inside(mouse_x, mouse_y):  # move
                    s.is_selected = False
                    move_sound_effect(s)
                    moving_squad(s, mouse_x, mouse_y)
                    s.can_move = False

            # Unselect
            elif mouse_clicked == 'RIGHT':
                s.is_selected = False

    # Flip
    elif arrow_pressed:
        for s in game.players[(game.current_player - 1)].army:
            if s.is_selected and s.can_rotate:
                if arrow_pressed == 'D':
                    new_direction = 0
                elif arrow_pressed == 'W':
                    new_direction = 90
                elif arrow_pressed == 'A':
                    new_direction = 180
                elif arrow_pressed == 'S':
                    new_direction = 270

                if new_direction != s.direction:
                    s.is_selected = False
                    s.change_direction(new_direction)
                    s.can_rotate = False
                    game.last_action = ('%s(%i) has rotated' % (s.name, s.player))


def dist_attack_phase(mouse_x, mouse_y, mouse_clicked):
    if not mouse_clicked:
        for p in game.players:
            for s in p.army:
                if s.pos[1].collidepoint(mouse_x, mouse_y):
                    s.mouse_over = True
                elif s.mouse_over:
                    s.mouse_over = False

    elif mouse_clicked == 'LEFT':
        for s in game.players[(game.current_player - 1)].army:
            if not s.is_selected and s.can_range_attack:
                if s.pos[1].collidepoint(mouse_x, mouse_y):
                    s.is_selected = True

            elif s.is_selected and s.can_range_attack:  # attack
                for p2 in game.players:
                    for s2 in p2.army:
                        if s2.player != game.current_player and s2.pos[1].collidepoint(mouse_x, mouse_y):
                            shot_sound_effect(s)
                            pygame.time.wait(1000)
                            if is_in_range(s, s2):
                                if s.category != 'artillery':
                                    kills = battle.calculate_distance_kills(s, s2)
                                    hit_sound.play()
                                else:
                                    kills = battle.calculate_artillery_kills(s, s2)
                                    if kills == 0:
                                        game.last_action = ('%s(%i) bad shot' % (s.name, s.player))
                                    else:
                                        hit_sound.play()
                                s2.units -= kills
                                if s2.units > 0:
                                    s2.update_img()
                                else:
                                    eliminate_squad(p2, s2)
                            s.is_selected = s.can_range_attack = False

    elif mouse_clicked == 'RIGHT':
        for s in game.players[(game.current_player - 1)].army:
            s.is_selected = False


def solve_melee_phase(mouse_x, mouse_y, mouse_clicked):
    if not mouse_clicked:
        for p in game.players:
            for s in p.army:
                if s.pos[1].collidepoint(mouse_x, mouse_y):
                    s.mouse_over = True
                elif s.mouse_over:
                    s.mouse_over = False

    elif mouse_clicked == 'LEFT':
        for s in game.players[(game.current_player - 1)].army:
            if s.pos[1].collidepoint(mouse_x, mouse_y) and s.engaged and s.can_melee_attack:
                battle_sound.play()
                pygame.time.wait(1000)
                for p in game.players:
                    for s2 in p.army:
                        if s.player != s2.player:
                            if s.pos[1].colliderect(s2.pos[1]):
                                s1_kills, s2_kills = battle.calculate_melee_kills(s, s2)
                                s.units -= s2_kills
                                s2.units -= s1_kills
                                if s.units > 0:
                                    s.update_img()
                                else:
                                    eliminate_squad(game.players[(game.current_player - 1)], s)
                                if s2.units > 0:
                                    s2.update_img()
                                else:
                                    eliminate_squad(p, s2)
                                game.last_action = ('%s(%i) and %s(%i) have fought' % (s.name, s.player, s2.name, s2.player))
                s.can_melee_attack = False

    elif mouse_clicked == 'RIGHT':
        for s in game.players[(game.current_player - 1)].army:
            s.is_selected = False


def check_death():
    for p in game.players:
        if not p.army:
            p.is_death = True
    blit()
    pygame.display.update()
    pygame.time.wait(300)
    next_phase()


# ------------------------------ SET ARMY
def set_army():
    """INSERT HERE YOUR COMPLETE ARMY"""
    # PLAYER 1
    generate_squad(1, 'archers', 42, 450 - INIT_CAMERA[0], 800 - INIT_CAMERA[1], 90)
    generate_squad(1, 'archers', 24, 750 - INIT_CAMERA[0], 850 - INIT_CAMERA[1], 90)
    generate_squad(1, 'swordsmen', 50, 550 - INIT_CAMERA[0], 900 - INIT_CAMERA[1], 90)
    generate_squad(1, 'cavalry', 36, 150 - INIT_CAMERA[0], 760 - INIT_CAMERA[1], 90)
    generate_squad(1, 'canon', 1, 160 - INIT_CAMERA[0], 860 - INIT_CAMERA[1], 90)
    # PLAYER 2
    generate_squad(2, 'archers', 36, 750 - INIT_CAMERA[0], 150 - INIT_CAMERA[1], 270)
    generate_squad(2, 'archers', 24, 280 - INIT_CAMERA[0], 150 - INIT_CAMERA[1], 270)
    generate_squad(2, 'spearmen', 54, 490 - INIT_CAMERA[0], 110 - INIT_CAMERA[1], 270)
    generate_squad(2, 'cavalry', 22, 800 - INIT_CAMERA[0], 80 - INIT_CAMERA[1], 270)
    generate_squad(2, 'spearmen', 42, 650 - INIT_CAMERA[0], 220 - INIT_CAMERA[1], 270)
    # PLAYER 3
    generate_squad(3, 'swordsmen', 36, 1300 - INIT_CAMERA[0], 320 - INIT_CAMERA[1], 180)
    generate_squad(3, 'spearmen', 42, 1350 - INIT_CAMERA[0], 750 - INIT_CAMERA[1], 180)
    generate_squad(3, 'cavalry', 38, 1360 - INIT_CAMERA[0], 530 - INIT_CAMERA[1], 180)
    generate_squad(3, 'canon', 1, 1440 - INIT_CAMERA[0], 480 - INIT_CAMERA[1], 180)
    generate_squad(3, 'canon', 1, 1400 - INIT_CAMERA[0], 350 - INIT_CAMERA[1], 180)
    # PLAYER 4


# ------------------------------  SOUND EFFECTS FUNCTIONS
def move_sound_effect(squad):
    if squad.category == 'infantry':
        inf_move_sound.play()
    elif squad.category == 'cavalry':
        cavalry_move_sound.play()
    elif squad.category == 'artillery':
        artillery_move_sound.play()


def shot_sound_effect(squad):
    if squad.category == 'artillery':
        canon_sound.play()
    else:
        archers_sound.play()


# ------------------------------ OTHER FUNCTIONS
def generate_squad(player, name, units, init_x, init_y, init_direction):
    test_squad = squad.Squad(player, name, units, init_x, init_y, init_direction)
    game.players[player - 1].add_squad(test_squad)


def eliminate_squad(player, squad):
    player.lose_squad(squad)
    pygame.time.wait(200)
    death_squad_sound.play()
    game.last_action = ('%s(%i) has been destroyed' % (squad.name, squad.player))


def show_squad_info(squad):
    if squad.direction == 0:
        x, y = squad.pos[1].bottomleft
    elif squad.direction == 90 or squad.direction == 180:
        x, y = squad.pos[1].bottomright
    elif squad.direction == 270:
        x, y = squad.pos[1].topright

    display_number_units_surf = display_number_units.render('%s (%i)' % (squad.units, squad.player), True, BLACK)
    display_number_units_rect = display_number_units_surf.get_rect(topleft=(x, y))
    screen.blit(display_number_units_surf, display_number_units_rect)


def show_highlight(squad):
    color = BLUE if game.current_player == squad.player else RED
    x, y = squad.pos[1].topleft
    w, h = squad.img.get_size()
    pygame.draw.rect(screen, color, (x - 1, y - 1, w + 2, h + 2), 1)


def clean_highlights():
    for s in game.players[(game.current_player - 1)].army:
        s.is_selected = False


def is_inside(mouse_x, mouse_y):
    if (MARGIN - camera.X) < mouse_x < (map_W - camera.X - MARGIN) and (MARGIN - camera.Y) < mouse_y < (map_H - camera.Y - MARGIN):
        return True
    return False


def moving_squad(squad, destination_x, destination_y):
    current_x = squad.pos[0][0]
    current_y = squad.pos[0][1]
    dx = float(destination_x - current_x)
    dy = float(destination_y - current_y)
    max_move = squad.get_mov()
    attempt_move = m.sqrt((dx ** 2.) + (dy ** 2.))
    if attempt_move > max_move:
        k = float(attempt_move) / float(max_move)
        dx = dx / k
        dy = dy / k
    dx = dx / FPS
    dy = dy / FPS
    frame = 0
    while frame <= FPS:
        game.last_action = ('%s(%i) has moved' % (squad.name, squad.player))
        current_x += dx
        current_y += dy
        squad.move_squad(current_x, current_y)
        if check_collision(squad) == 2:  # collision to ally
            current_x -= dx
            current_y -= dy
            squad.move_squad(current_x, current_y)
            break
        elif check_collision(squad) == 1:  # collision to enemy
            game.last_action = ('%s(%i) has charged' % (squad.name, squad.player))
            break
        frame += 1
        blit()
        pygame.display.update()
        fpsClock.tick(FPS)


def check_collision(squad):
    val = 0
    for p in game.players:
        for s in p.army:
            if not squad.pos[0] == s.pos[0] and squad.pos[1].colliderect(s.pos[1]):  # if collision
                if squad.player != s.player:  # if is enemy
                    squad.engaged = s.engaged = True
                    squad.can_move = squad.can_rotate = squad.can_range_attack = False
                    val = 1
                else:
                    squad.engaged = s.engaged = False  # if is ally
                    val = 2
    return val


def is_in_range(squad, squad2):
    current_x = squad.pos[0][0]
    current_y = squad.pos[0][1]
    objective_x = squad2.pos[0][0]
    objective_y = squad2.pos[0][1]
    dx = float(objective_x - current_x)
    dy = float(objective_y - current_y)
    max_range = squad.get_dR()
    attempt_range = m.sqrt((dx ** 2.) + (dy ** 2.))
    if attempt_range > max_range:
        game.last_action = ('%s(%i) failed, target out of range' % (squad.name, squad.player))
        return False

    game.last_action = ('%s(%i) successfully attacked %s(%i)' % (squad.name, squad.player, squad2.name, squad2.player))
    return True


def all_combats_solved():
    val = True
    for s in game.players[(game.current_player - 1)].army:
        if s.engaged and s.can_melee_attack:
            val = False
    return val


# ------------------------------ SET AND UPLOAD
game = Game()
camera = Camera()

fpsClock = pygame.time.Clock()

# screen = pygame.display.set_mode((screen_W,screen_H),0,32)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_W = screen.get_width()
screen_H = screen.get_height()
pygame.display.set_caption('X-05 WARGAME (Beta)')
# pygame.display.set_icon(pygame.image.load('...

bg_texture = set_bg_texture()
bg = pygame.image.load('data/src/bg/%s.jpg' % bg_texture).convert()
bgRect = bg.get_rect()

music = set_music()
pygame.mixer.music.load('data/src/music/%s.mp3' % music)

display_player_phase = pygame.font.Font('data/src/font/SketchRockwell_Bold.ttf', 24)
display_player_phaseSurf = display_player_phase.render(None, True, BLACK)

display_gen_info = pygame.font.Font('data/src/font/brankovic.ttf', 14)
display_gen_infoSurf = display_gen_info.render(None, True, BLACK)

display_number_units = pygame.font.Font('data/src/font/SketchRockwell_Bold.ttf', 12)

tubular_bell_sound = pygame.mixer.Sound('data/src/sound/tubular_bell.wav')  # next player
inf_move_sound = pygame.mixer.Sound('data/src/sound/footsteps.wav')
cavalry_move_sound = pygame.mixer.Sound('data/src/sound/horses_riding.wav')
artillery_move_sound = pygame.mixer.Sound('data/src/sound/metal_cart.wav')
archers_sound = pygame.mixer.Sound('data/src/sound/archers_shooting.wav')
canon_sound = pygame.mixer.Sound('data/src/sound/explosion.wav')
hit_sound = pygame.mixer.Sound('data/src/sound/snaredrum.wav')  # distance impact
battle_sound = pygame.mixer.Sound('data/src/sound/tom_moyen.wav')  # melee solve
death_squad_sound = pygame.mixer.Sound('data/src/sound/dark_bell.wav')
