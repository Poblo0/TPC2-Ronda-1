class Bot:
    def __init__(self):
        self.__commands = ["_"] * 4
        self.__state = None
        self.__map = None
        self.__map_size = None
    
    def go_left(self):
        self.__commands[0] = 'L'
    
    def go_right(self):
        self.__commands[1] = 'R'
    
    def jump(self):
        self.__commands[2] = 'J'
    
    def use_bomb(self):
        self.__commands[3] = 'B'
    
    def clear_commands(self):
        self.__commands = ["_"] * 4

    def get_controls(self):
        return "".join(self.__commands)
    
    def set_state(self, state):
        self.__state = state

    def get_my_x(self):
        return self.__state['state'][0]
    
    def get_my_y(self):
        return self.__state['state'][1]
    
    def get_enemy_x(self):
        return self.__state['state'][4]
    
    def get_enemy_y(self):
        return self.__state['state'][5]
    
    def have_bomb(self):
        return self.__state['state'][2] == -128
    
    def enemy_has_bomb(self):
        return self.__state['state'][6] == -128
    
    def get_my_bomb_x(self):
        if (self.__state['state'][2] == -128 or  self.__state['state'][2] == -256):
            return None
        else: 
            return self.__state['state'][2]
    
    def get_my_bomb_y(self):
        if (self.__state['state'][2] == -128 or  self.__state['state'][2] == -256):
            return None
        else: 
            return self.__state['state'][3]
        
    def get_enemy_bomb_x(self):
        if (self.__state['state'][6] == -128 or  self.__state['state'][6] == -256):
            return None
        else: 
            return self.__state['state'][6]
        
    def get_enemy_bomb_y(self):
        if (self.__state['state'][7] == -128 or  self.__state['state'][7] == -256):
            return None
        else: 
            return self.__state['state'][7]
    
    # Read the text file of the map
    def read_map(self, file_path):
        with open(file_path, 'r') as file:
            # Read each line, strip the newline, and convert to a list of characters
            self.__map, self.__map_size = self.make_rectangle([list(line.strip('\n')) for line in file])

        
    # Makes the map a rectangle
    def make_rectangle(self, double_list):
        max_size = 0
        double_list.insert(0, list()); double_list.insert(0, list())
        for i in double_list:
            i.insert(0, '_')
        for i in double_list:
            if (len(i) > max_size):
                max_size = len(i)
        for i, _  in enumerate(double_list):
            while(len(double_list[i]) < max_size):
                double_list[i].append('_')
        
        return double_list, (max_size, len(double_list))
    
    def is_solid(self, x, y):
        if (x < 0 or x >= self.__map_size[0] or y < 0 or y >= self.__map_size[1]):
            return False
        if (self.__map[y][x] == '.'):
            return True
        return False