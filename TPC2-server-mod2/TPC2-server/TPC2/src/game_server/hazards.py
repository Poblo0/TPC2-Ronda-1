def check_sudden_death(y, sea_level):
    if (y < sea_level):
        return True
    return False

class Bomb:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.timer = 0
        self.state = 0
    
    def update(self,):
        self.timer += 1
        if (self.timer < 61):
            self.state = 0
        elif (self.timer < 121): self.state = 1
        else: self.state = 2
    
    def draw(self, surface, bomb_sprites, rez):
        if (self.state == 0):
            surface.blit(bomb_sprites[0], (self.x, self.y))
        else:
            self.explode(surface, bomb_sprites, rez)

    def explode(self, surface, bomb_sprites, rez):
        y = self.y - 64
        surface.blit(bomb_sprites[1], (self.x, self.y))
        while (y > -64):
            surface.blit(bomb_sprites[2], (self.x, y))
            y -= 64
        x = self.x - 64
        while (x > -64):
            surface.blit(bomb_sprites[3], (x, self.y))
            x -= 64
        x = self.x + 64
        while (x < rez[0] + 64):
            surface.blit(bomb_sprites[3], (x, self.y))
            x += 64

    def get_state(self):
        return self.state
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y