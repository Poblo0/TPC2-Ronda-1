import pygame

# Read the text file of the map
def read_map(file_path):
    with open(file_path, 'r') as file:
        # Read each line, strip the newline, and convert to a list of characters
        return make_rectangle([list(line.strip('\n')) for line in file])

def get_inital_pos(matrix, character):
    for i, line in enumerate(matrix):
        for j, elem in enumerate(line):
            if (character == elem):
                return (j * 64 + 64, i *64 + 128)

# Makes the map a rectangle
def make_rectangle(double_list):
    max_size = 0
    for i in double_list:
        if (len(i) > max_size):
            max_size = len(i)
    for i, _  in enumerate(double_list):
        while(len(double_list[i]) < max_size):
            double_list[i].append('_')
    return double_list, (max_size, len(double_list)), get_inital_pos(double_list, '1'), get_inital_pos(double_list, '2'), get_inital_pos(double_list, 'B')

# Draw the map on screen
def draw_map(map, tileset, surface):
    just_in_platform = True
    color = 0
    for y, line in enumerate(map):
        for x, character in enumerate(line):
            match character:
                case '.':
                    if (not just_in_platform):
                        color = (color + 1) % 4
                    spawn_tile(map, surface, tileset, color, x, y)
                    just_in_platform = True
                case _:
                    just_in_platform = False
        just_in_platform = False

# Draw the background
def draw_background(surface, background, background_extra, map_size):
    for i in range(0, map_size[0] + 2):
        surface.blit(background, (i * 64, 0))
    for i in range(0, map_size[0] + 2):
        for j in range(7, map_size[1] + 1):
            surface.blit(background_extra, (i * 64, j * 64 + 64))


# Spawn a tile in the screen
def spawn_tile(map, surface, tileset, color, x, y):
    if (x == 0 or map[y][x - 1] != '.'):
        if (x == len(map[y]) - 1 or map[y][x + 1] != '.'):
            surface.blit(tileset[color][1], (x * 64 + 64, y * 64 + 128))
            cascade_tile(map, surface, tileset, color, 2, x, y + 1)
        else:
            surface.blit(tileset[color][3], (x * 64 + 64, y * 64 + 128))
            cascade_tile(map, surface, tileset, color, 6, x, y + 1)
    elif (x == len(map[y]) - 1 or map[y][x + 1] != '.'):
        surface.blit(tileset[color][5], (x * 64 + 64, y * 64 + 128))
        cascade_tile(map, surface, tileset, color, 8, x, y + 1)
    else:
        surface.blit(tileset[color][4], (x * 64 + 64, y * 64 + 128))
        cascade_tile(map, surface, tileset, color, 7, x, y + 1)

# Cascade down a tile to create a cliff and not a floating island
def cascade_tile(map, surface, tileset, color, tile, x, y):
    if (y == len(map) or x >= len(map[y])):
        return
    if (map[y][x] != '.'):
        surface.blit(tileset[color][tile], (x * 64 + 64, y * 64 + 128))
        cascade_tile(map, surface, tileset, color, tile, x, y + 1)
    elif (x == 0 or x == len(map[y]) - 1 or map[y][x - 1] != '.' or map[y][x + 1] != '.'):
        surface.blit(tileset[color][tile], (x * 64 + 64, y * 64 + 128))

# Draw straberry soda sea
def draw_soda(surface, tiles, frame, sea_level, x_size, y_size):
    x = 0
    while (x < x_size):
        surface.blit(tiles[frame], (x, sea_level))
        y = sea_level + 64
        while (y < y_size):
            surface.blit(tiles[frame + 2], (x, y))
            y += 64
        x += 64