class Flag():
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

        self._anim_state = 0
        self._sprite_pos = [
            (16, 0),
            (48, 16),
            (64, 16),
            (48, 16),
        ]

    def step_anim(self, framecount: int):
        if framecount % 16 == 0:
            self._anim_state = (self._anim_state + 1) % len(self._sprite_pos)
        return self._sprite_pos[self._anim_state]
