class Player():
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.deltax = 0
        self.deltay = 0

    def stop(self):
        self.deltax = 0
        self.deltay = 0

    def update_pos(self):
        if self.deltax > 0:
            self.x += 1
            self.deltax -= 1
        elif self.deltax < 0:
            self.x -= 1
            self.deltax += 1

        if self.deltay > 0:
            self.y += 1
            self.deltay -= 1
        elif self.deltay < 0:
            self.y -= 1
            self.deltay += 1
