class Snake:
    def __init__(self):
        self.positions = []

    def grow(self, new_position):
        self.positions.append((0, 0))
        old_positions = self.positions.copy()
        for i in range(1, len(self.positions)):
            self.positions[i] = old_positions[i-1]
        self.positions[0] = new_position

    def get_head_position(self):
        return self.positions[0]

    def get_tail_position(self):
        return self.positions[-1]

    def move(self, new_position):
        old_positions = self.positions.copy()
        for i in range(1, len(self.positions)):
            self.positions[i] = old_positions[i-1]
        self.positions[0] = new_position

