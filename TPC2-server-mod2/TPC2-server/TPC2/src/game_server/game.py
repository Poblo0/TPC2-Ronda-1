# Game imports
import pygame
import sys
import configparser

from image import *
from map import *
from shark import Shark, coordinates
from hazards import Bomb
from server import players
from server import update
from server import next_game

pygame.init()

# Load map
map_file = None
map = None; map_size = None;a_pos = None; b_pos = None; bomb_pos = None

# Fixed resolution (base) and window size
base_resolution = None
center = None
SCALE_FACTOR = 1  # Scale factor to enlarge the window
window = pygame.display.set_mode((512 * SCALE_FACTOR, 512 * SCALE_FACTOR), pygame.RESIZABLE) 
pygame.display.set_caption("TPC2")
# Create a counter for the points of each team
team_points = [0, 0]
# Create a list to check if a team has died
death = [False, False]
# Get team names
team_names = ["ElCamo2", "Macarrones"]
# Create the text font that counts each teams points
font = pygame.font.Font(None, 36)
# Create a fixed-resolution surface
base_surface = None
# Load images
# Load background
background = pygame.image.load("../../assets/background.png").convert()
background_extra = pygame.image.load("../../assets/extra_back.png").convert()
# Load sudden death
muerte_subita = pygame.image.load("../../assets/muerte_subita.png").convert_alpha()
muerte_subita_rect = None
# Load logos
logos = pygame.image.load("../../assets/logos.png").convert_alpha()
# Load bomb
bomb = chop_image(pygame.image.load("../../assets/bomb.png").convert_alpha(), 64, 64)
# Chop Sharkies
sharkies = pygame.image.load("../../assets/sharkies.png").convert_alpha()
teams_info = configparser.ConfigParser()
teams_info.read("../../equipos.ini")
team_names[0] = teams_info.get('Equipo0', 'nombre')
team_names[1] = teams_info.get('Equipo1', 'nombre')
players_img = chop_image_specific(sharkies, int(teams_info.get('Equipo0', 'tipo')), int(teams_info.get('Equipo0', 'color')))
players_img += chop_image_specific(sharkies, int(teams_info.get('Equipo1', 'tipo')), int(teams_info.get('Equipo1', 'color')))
# Chop tiles and recolor them
tileset_full_img = pygame.image.load("../../assets/tileset.png").convert_alpha()
blue_tiles = chop_image(tileset_full_img, 64, 64)
recolor_image(tileset_full_img, (164, 211, 242), (199, 222, 151), (106, 155, 232), (113, 193, 66))
green_tiles = chop_image(tileset_full_img, 64, 64)
recolor_image(tileset_full_img, (199, 222, 151), (221, 198, 229), (113, 193, 66), (219, 138, 228))
pink_tiles = chop_image(tileset_full_img, 64, 64)
recolor_image(tileset_full_img, (221, 198, 229), (221, 219, 182), (219, 138, 228), (193, 206, 86))
yellow_tiles = chop_image(tileset_full_img, 64, 64)
# Group tiles
tileset = [blue_tiles, green_tiles, pink_tiles, yellow_tiles]
# Chop Strawberry Soda
strawberry_soda = chop_image(pygame.image.load("../../assets/strawberry_soda.png").convert_alpha(), 64, 64)
# Animation loops
walk_loop = 0
soda_loop = 0
# Flag for knowing if the bomb has been picked
bomb_picked = False
# Game time
game_time = 0
# Sea level
sea_level = 0
# Create sharks
shark_a = None
shark_b = None

def set_up_game(map_file):
    global map,  map_size, a_pos, b_pos, bomb_pos, base_resolution, center, window, base_surface, bomb_picked, sea_level, shark_a, shark_b, muerte_subita, muerte_subita_rect, game_time

    # Read map
    map, map_size, a_pos, b_pos, bomb_pos = read_map(map_file)

    # Set up screen
    base_resolution = (map_size[0] * 64 + 128, map_size[1] * 64 + 256)
    center = (base_resolution[0] / 2, base_resolution[1] / 2)
    window = pygame.display.set_mode((base_resolution[0] * SCALE_FACTOR, base_resolution[1] * SCALE_FACTOR), pygame.RESIZABLE) 
    base_surface = pygame.Surface(base_resolution)

    bomb_picked = False

    sea_level = len(map) * 64 + 128

    shark_a = Shark(a_pos[0], a_pos[1])
    shark_b = Shark(b_pos[0], b_pos[1])

    muerte_subita_rect = muerte_subita.get_rect(center=center)

    game_time = 0
    

def game_loop():
    # Create bomb array
    bomb_array = [None, None]
    # Integer variables are required to be stated as global but not any others ??
    global walk_loop, soda_loop, game_time, sea_level, bomb_picked

    photo_finish_time = 0

    # Main loop
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if (not death[0] and not death[1]):

            # Behavior based update
            if (update[0] and update[1]):
                update[0] = False
                update[1] = False

                # Update Sharks
                shark_a.control(map, players[0][0], players[0][1], players[0][2], False)
                shark_b.control(map, players[1][0], players[1][1], players[1][2], False)

                if (shark_a.use_bomb(players[0][3] and bomb_array[0] == None)):
                    bomb_array[0] = Bomb(shark_a.getX(), shark_a.getY())

                if (shark_b.use_bomb(players[1][3] and bomb_array[1] == None)):
                    bomb_array[1] = Bomb(shark_b.getX(), shark_b.getY())

                for i, e in enumerate(bomb_array):
                    if (e == None):
                        continue
                    e.update()
                    if(e.get_state() == 1):
                        if (shark_a.inBox(e.get_x() - 32, -128, e.get_x() + 32, e.get_y() + 64) or shark_a.inBox(-128, e.get_y() - 32, len(map[0])*64 + 128, e.get_y() + 32)):
                            death[0] = True
                            team_points[1] += 1
                        if (shark_b.inBox(e.get_x() - 32, -128, e.get_x() + 32, e.get_y() + 64) or shark_b.inBox(-128, e.get_y() - 32, len(map[0])*64 + 128, e.get_y() + 32)):
                            death[1] = True
                            team_points[0] += 1
                        if (e.get_state() == 2):
                            bomb_array[i] = None
                
                # Update time
                game_time += 1

                # Update strawberry soda sea
                if (game_time > 420):
                    sea_level -= 0.5

                if (sea_level // 1 < shark_a.getY() + 64):
                    team_points[1] += 1
                    death[0] = True

                if (sea_level // 1 < shark_b.getY() + 64):
                    team_points[0] += 1
                    death[1] = True

                # Update global data
                coordinates[0][0] = shark_a.getX(); coordinates[0][1] = shark_a.getY()
                coordinates[1][0] = shark_b.getX(); coordinates[1][1] = shark_b.getY()
                if (bomb_picked):
                    for i in range(0,2):
                        if (bomb_array[i] != None):
                            coordinates[i][2] = bomb_array[i].get_x(); coordinates[i][3] = bomb_array[i].get_y()
                        elif (i == 0 and shark_a.has_bomb() or i == 1 and shark_b.has_bomb()):
                            coordinates[i][2] = -128
                        else: coordinates[i][2] = -256; coordinates[i][3] = -256
                else: 
                    for i in range(0,2):
                        coordinates[i][2] = -256; coordinates[i][3] = -256


            # Animation updates
            walk_loop = (walk_loop + 1) % 32
            soda_loop = (soda_loop + 1) % 60
        else:
            photo_finish_time += 1
            if photo_finish_time > 60:
                death[0] = False
                death[1] = False
                next_game[0] = 1
                next_game[1] = 1
                return

        # Draw background
        draw_background(base_surface, background, background_extra, map_size)

        # Draw map
        draw_map(map, tileset, base_surface)

        # Draw logos
        base_surface.blit(logos, (base_resolution[0]-270, 20))

        # Check for sudden death
        if (game_time > 420):
            base_surface.blit(muerte_subita, muerte_subita_rect)

        # Draw Bomb
        if (not bomb_picked):
            base_surface.blit(bomb[0], bomb_pos)
            if (shark_a.check_getting_bomb(bomb_pos[0] - 48, bomb_pos[1] - 32, bomb_pos[0] + 48, bomb_pos[1] + 32)):
                bomb_picked = True
            if (shark_b.check_getting_bomb(bomb_pos[0] - 48, bomb_pos[1] - 32, bomb_pos[0] + 48, bomb_pos[1] + 32)):
                bomb_picked = True

        # Draw sharkies
        base_surface.blit(pygame.transform.flip(players_img[0 + walk_loop // 8], shark_a.getFacing(), False), (shark_a.getX(), shark_a.getY()))
        base_surface.blit(pygame.transform.flip(players_img[4 + walk_loop // 8], shark_b.getFacing(), False), (shark_b.getX(), shark_b.getY()))

        # Draw bombs
        for e in bomb_array:
            if (e == None):
                continue
            e.draw(base_surface, bomb, base_resolution)

        # Draw soda sea
        draw_soda(base_surface, strawberry_soda, soda_loop // 30, sea_level // 1, base_resolution[0], base_resolution[1])

        # Draw text of points
        text_of_points = font.render(team_names[0] + ": " + str(team_points[0]) + " - " + team_names[1] + ": " + str(team_points[1]), True, (255, 255, 255))
        base_surface.blit(text_of_points, (20, 20))

        # Scale the base surface to the window size
        scaled_surface = pygame.transform.scale(base_surface, window.get_size())
        window.blit(scaled_surface, (0, 0))

        # Update the display
        pygame.display.flip()

        # Limit to 60 FPS
        pygame.time.Clock().tick(60)