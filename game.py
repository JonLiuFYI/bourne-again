from time import sleep

import pyxel
import signals
from target import Target
from solid_sprite import Solid

INPUT_PREAMBLE = 'from signals import *\n'


class Game():

    def __init__(self):
        pyxel.init(240, 240, caption='Bourne Again', fps=30)
        pyxel.mouse(True)

        pyxel.load('stuff.pyxres')

        self.seemsg = ''
        self.seemsg_iter = ''
        self.seemsg_out = ''

        self.player_x = 30
        self.player_x_delta = 0
        self.player_y = 120
        self.player_y_delta = 0

        self.targets = {
            'A': Target(200, 100, 'Target A feels lonely'),
            'B': Target(1, 20, 'Fortune awaits Target B'),
            'C': Target(120, 220, 'Target C is in the mood for shawarma')
        }

        self.wall = [
            Solid(30,160),
            Solid(100,45),
            Solid(24,200)
        ]
        
        self.locked = False

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

        if not self.locked and pyxel.btnr(pyxel.KEY_SPACE):
            script = INPUT_PREAMBLE + self.read_input()
            self.reset_vars()
            try:
                self.locked = True
                exec(script)
            except signals.See as see:
                """Start typing out info on the named target."""
                if see.msg in self.targets:
                    tgt: Target = self.targets[see.msg]
                    self.seemsg = f'{see.msg} ({tgt.x}, {tgt.y})\n{tgt.comment}'
                else:
                    self.seemsg = f'{see.msg}: no such target'

                self.seemsg_iter = iter(self.seemsg)
            except signals.Right as right:
                self.player_x_delta = right.dist
            except signals.Left as left:
                self.player_x_delta = -left.dist
            except signals.Up as up:
                self.player_y_delta = -up.dist
            except signals.Down as down:
                self.player_y_delta = down.dist
            except:
                pass

        if self.player_x_delta != 0 or self.player_y_delta != 0:
            self.move_player()
        if len(self.seemsg) > 0:
            self.typeout()
        

    def draw(self):
        pyxel.cls(12)
        if not self.locked:
            pyxel.text(0, 234, '[SPACE] run INPUT', 1)

        [self.draw_target(k, t) for k, t in self.targets.items()]


        [self.draw_wall(w) for w in self.wall]


        # player
        pyxel.blt(self.player_x, self.player_y, 0,
                  0, 0,
                  16, 16,
                  0)

        # see() text
        pyxel.text(1, 1, self.seemsg_out, 0)

    def read_input(self):
        """Get all the text from the INPUT file."""
        f = open('INPUT', 'r')
        script = f.read()
        f.close()
        return script

    def reset_vars(self):
        """Clean up script execution state for the next run."""
        self.seemsg = ''
        self.seemsg_iter = ''
        self.seemsg_out = ''

    def move_player(self):
        """Move the player step by step to the new position."""
        if self.player_x_delta > 0:
            #if is there is no wall
            if self.detect_wall_collision(1,0) == False:
                self.player_x += 1
                self.player_x_delta -= 1
            else:
                self.player_x_delta = 0
                self.player_y_delta = 0
                self.locked = False

        elif self.player_x_delta < 0:
            #if there is no wall
            if self.detect_wall_collision(-1,0) == False:
                self.player_x -= 1
                self.player_x_delta += 1
            else:
                self.player_x_delta = 0
                self.player_y_delta = 0
                self.locked = False

            
        if self.player_y_delta > 0:
            if self.detect_wall_collision(0,1) == False:
                self.player_y += 1
                self.player_y_delta -= 1
            else:
                self.player_x_delta = 0
                self.player_y_delta = 0
                self.locked = False
        # if there is a wall
        elif self.player_y_delta < 0:
            if self.detect_wall_collision(0,-1) == False:
                self.player_y -= 1
                self.player_y_delta += 1
            else:
                self.player_x_delta = 0
                self.player_y_delta = 0
                self.locked = False

        if self.player_x_delta == self.player_y_delta == 0:
            self.locked = False

    def typeout(self):
        """Type out see() text one letter at a time."""
        if len(self.seemsg_out) < len(self.seemsg):
            self.seemsg_out += next(self.seemsg_iter)
        else:
            self.locked = False

    def draw_target(self, name: str, tgt: Target):
        pyxel.blt(tgt.x, tgt.y, 0,
                  32, 0,
                  16, 16,
                  0)
        pyxel.text(tgt.x, tgt.y+11, name, 0)

    def draw_wall(self, sld: Solid):
        pyxel.blt(sld.x, sld.y, 0,
                  0, 16,
                  56, 56,
                  0)
    def detect_wall_collision(self, x_inc, y_inc):
        for w in self.wall:
            if (
                self.player_x +x_inc + 14 >= w.x
                and self.player_x + x_inc <= w.x + 14
                and self.player_y + y_inc + 15 >= w.y
                and self.player_y + y_inc <= w.y + 15
            ):
                return True
            else:
                return False



Game()
