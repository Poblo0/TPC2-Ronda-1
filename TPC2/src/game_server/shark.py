coordinates = [[0, 0, -256, 0], [0, 0, -256, 0]]  # 2 sets of 4 each for a player (x,y) (bomb x, bomb y)

class Shark:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walk_speed = 2
        self.jump_speed = 8
        self.y_speed = 0
        self.alive = True
        self.in_ground = False
        self.facing = True
        self.bombs = 0

    def control(self, map, left, right, jump, bomb):
        if (right):
            self.x += self.walk_speed
            self.facing = False
        if (left):
            self.x -= self.walk_speed
            self.facing = True
        if (jump and self.in_ground):
            self.y_speed -= 14
        self.y_speed += 1
        self.in_ground = False
        self.collision(map)
        if (self.in_ground):
            new_y = self.y - (self.y + self.y_speed + 64) % 64 + 1
            if (new_y > self.y):
                self.y = new_y
            self.y_speed = 0
        self.y += self.y_speed

    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getFacing(self):
        return self.facing
    
    def get_tile(self, x, y, map):
        if (x <= 64 or x >= len(map[0]) * 64 + 64 or y < 128 or y >= len(map) * 64 + 128):
            return '_'
        return map[(y - 128) // 64][(x - 64) // 64]

    def inBox(self, x_min, y_min, x_max, y_max):
        if (self.x >= x_min and self.x <= x_max and self.y >= y_min and self.y < y_max):
            return True
        return False
    
    def check_getting_bomb(self,x_min, y_min, x_max, y_max):
        if self.inBox(x_min, y_min, x_max, y_max):
            self.bombs += 1
            return True
            
    def use_bomb(self, use):
        if (use and self.bombs > 0):
            self.bombs -= 1
            return True
        False
    
    def collision(self, map):
        if (self.y_speed >= 0 and (self.get_tile(self.x + 16, self.y + self.y_speed + 64, map) == '.' or 
                                   self.get_tile(self.x + 48, self.y + self.y_speed + 64, map) == '.')
                                and (self.y - 1) // 64 != (self.y + self.y_speed) // 64):
            self.in_ground = True

    def has_bomb(self):
        return self.bombs == 1