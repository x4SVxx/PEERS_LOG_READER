class Tag:
    def __init__(self, name, color, width, x, y, z):
        self.name = name
        self.color = color
        self.width = width
        self.tail_length = 5
        self.current_time = 0

        self.x = x
        self.y = y
        self.z = z
        self.mas_time = []
        self.mas_time_with_flag_0 = []

        self.mas_x = []
        self.mas_y = []
        self.mas_z = []
        self.mas_x_f = []
        self.mas_y_f = []

        # self.log_for_beacons_mas = []

