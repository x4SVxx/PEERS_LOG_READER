class Tag:
    def __init__(self, name, color, width, start_x, start_y, start_z):
        self.name = name
        self.color = color
        self.width = width
        self.start_x = start_x
        self.start_y = start_y
        self.start_z = start_z
        self.x = start_x
        self.y = start_y
        self.z = start_z
        self.mas_time = []
        self.mas_false_time = []
        self.mas_x = []
        self.mas_y = []
        self.mas_z = []
        self.current_time = 0
        self.tail_length = 5
        self.mas_x_f = []
        self.mas_y_f = []

