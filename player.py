class Player():
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.deltax = 0
        self.deltay = 0

        self._anim_state = 0
        self._sprite_pos = [
            (0, 0),
            (16, 16)
        ]

    def stop(self):
        self.deltax = 0
        self.deltay = 0

    def stopped(self):
        return self.deltax == self.deltay == 0

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

    def step_anim(self):
        self._anim_state = (self._anim_state + 1) % 2

    def sprite(self):
        return self._sprite_pos[self._anim_state]

    def reset_anim(self):
        self._anim_state = 0
