import pygame

# Function to chop the image into tiles
def chop_image(image, tile_width, tile_height):
    image_width, image_height = image.get_size()
    tiles = []

    for y in range(0, image_height, tile_height):
        for x in range(0, image_width, tile_width):
            # Create a new surface for each tile
            tile = pygame.Surface((tile_width, tile_height), pygame.SRCALPHA)
            # Copy the portion of the original image onto the new surface
            tile.blit(image, (0, 0), pygame.Rect(x, y, tile_width, tile_height))
            tiles.append(tile)

    return tiles

# Function to chop the image into tiles
def chop_image_specific(image, type, color):
    image_width, _ = image.get_size()
    tiles = []
    type = type * 64
    for x in range(0, image_width, 64):
        # Create a new surface for each tile
        tile = pygame.Surface((64, 64), pygame.SRCALPHA)
        # Copy the portion of the original image onto the new surface
        tile.blit(image, (0, 0), pygame.Rect(x, type, 64, 64))

        match color:
            case 0:
                recolor_three(tile, (164, 211, 242), (164, 211, 242), (106, 155, 232), (106, 155, 232), (191, 70, 0), (113, 193, 66))
            case 1:
                recolor_three(tile, (164, 211, 242), (199, 222, 151), (106, 155, 232), (113, 193, 66), (191, 70, 0), (219, 138, 228))
            case 2:
                recolor_three(tile, (164, 211, 242), (221, 198, 229), (106, 155, 232), (219, 138, 228), (191, 70, 0), (193, 206, 86))
            case 3:
                recolor_three(tile, (164, 211, 242), (221, 219, 182), (106, 155, 232), (193, 206, 86), (191, 70, 0), (106, 155, 232))
        tiles.append(tile)
    return tiles

def recolor_three(surface, original_color_a, new_color_a, original_color_b, new_color_b, original_color_c, new_color_c):
    # Lock the surface to directly access pixel data (improves performance)
    surface.lock()
    width, height = surface.get_size()

    for x in range(width):
        for y in range(height):
            # Get the color of the current pixel
            current_color = surface.get_at((x, y))
            # Replace if it matches the original colors
            if current_color[:3] == original_color_a:  # Ignore the alpha channel
                surface.set_at((x, y), new_color_a + (current_color.a,))
            elif current_color[:3] == original_color_b:  # Ignore the alpha channel
                surface.set_at((x, y), new_color_b + (current_color.a,))
            elif current_color[:3] == original_color_c:  # Ignore the alpha channel
                surface.set_at((x, y), new_color_c + (current_color.a,))


# Recolors all pixels of original_color to new_color in the given surface
# For the current game we have 2 channels
def recolor_image(surface, original_color_a, new_color_a, original_color_b, new_color_b):
    # Lock the surface to directly access pixel data (improves performance)
    surface.lock()
    width, height = surface.get_size()
    
    for x in range(width):
        for y in range(height):
            # Get the color of the current pixel
            current_color = surface.get_at((x, y))
            # Replace if it matches the original color
            if current_color[:3] == original_color_a:  # Ignore the alpha channel
                surface.set_at((x, y), new_color_a + (current_color.a,))
            elif current_color[:3] == original_color_b:  # Ignore the alpha channel
                surface.set_at((x, y), new_color_b + (current_color.a,))
    
    # Unlock the surface after modifying pixels
    surface.unlock()

