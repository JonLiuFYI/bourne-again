from math import sin, cos, radians

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

        self.beam_angle = None
        self.beam_start_time = 0

        self.targets = {
            'A': Target(200, 100, 'Target A feels lonely'),
            'B': Target(1, 20, 'Fortune awaits Target B'),
            'C': Target(120, 220, 'Target C is in the mood for shawarma')
        }

        self.walls = [
            Solid(30, 160),
            Solid(100, 45),
            Solid(24, 200)
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

            except signals.Help:
                self.set_msg(signals.HELP)

            except signals.See as see:
                """Start typing out info on the named target."""
                if see.msg in self.targets:
                    tgt: Target = self.targets[see.msg]
                    self.set_msg(
                        f'{see.msg} ({tgt.x}, {tgt.y})\n{tgt.comment}')
                else:
                    self.set_msg(f'{see.msg}: no such target')

            except signals.Right as right:
                self.player_x_delta = right.dist

            except signals.Left as left:
                self.player_x_delta = -left.dist

            except signals.Up as up:
                self.player_y_delta = -up.dist

            except signals.Down as down:
                self.player_y_delta = down.dist

            except signals.Shoot as shot:
                self.beam_angle = radians(-shot.angle)
                self.beam_start_time = pyxel.frame_count

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

        # targets
        [self.draw_target(k, t) for k, t in self.targets.items()]

        # walls
        [self.draw_wall(w) for w in self.walls]

        # player
        pyxel.blt(self.player_x, self.player_y, 0,
                  0, 0,
                  16, 16,
                  0)

        # shot beam
        if self.beam_angle is not None:
            self.draw_beam(self.beam_angle, self.beam_start_time)

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
            if self.player_will_collide(1, 0):
                self.stop()
            else:
                self.player_x += 1
                self.player_x_delta -= 1

        elif self.player_x_delta < 0:
            if self.player_will_collide(-1, 0):
                self.stop()
            else:
                self.player_x -= 1
                self.player_x_delta += 1

        if self.player_y_delta > 0:
            if self.player_will_collide(0, 1):
                self.stop()
            else:
                self.player_y += 1
                self.player_y_delta -= 1

        elif self.player_y_delta < 0:
            if self.player_will_collide(0, -1):
                self.stop()
            else:
                self.player_y -= 1
                self.player_y_delta += 1

        if self.player_x_delta == self.player_y_delta == 0:
            self.locked = False

    def stop(self):
        """Forcibly stop moving the player."""
        self.player_x_delta = 0
        self.player_y_delta = 0

    def set_msg(self, msg: str):
        """Change the see() message."""
        self.seemsg = msg
        self.seemsg_iter = iter(self.seemsg)

    def typeout(self):
        """Type out see() text one letter at a time."""
        if len(self.seemsg_out) < len(self.seemsg):
            self.seemsg_out += next(self.seemsg_iter)
        else:
            self.locked = False

    def draw_target(self, name: str, tgt: Target):
        """Draw the given Target. Put its name in the corner."""
        pyxel.blt(tgt.x, tgt.y, 0,
                  32, 0,
                  16, 16,
                  0)
        pyxel.text(tgt.x, tgt.y+11, name, 0)

    def draw_beam(self, angle: float, starttime: int):
        """Draw a beam at the angle for both eyes."""
        elapsed_frames = pyxel.frame_count - starttime

        color = 10
        if 3 <= elapsed_frames < 6:
            color = 11
        elif 6 <= elapsed_frames < 9:
            color = 3
        elif 9 <= elapsed_frames < 12:
            color = 1
        elif elapsed_frames >= 12:
            self.beam_angle = None
            self.locked = False
            return

        eye1 = (self.player_x + 5, self.player_y + 4)
        eye2 = (self.player_x + 10, self.player_y + 4)
        pyxel.line(eye1[0], eye1[1],
                   eye1[0] + 1000*cos(self.beam_angle),
                   eye1[1] + 1000*sin(self.beam_angle),
                   color)
        pyxel.line(eye2[0], eye2[1],
                   eye2[0] + 1000*cos(self.beam_angle),
                   eye2[1] + 1000*sin(self.beam_angle),
                   color)

    def draw_wall(self, sld: Solid):
        pyxel.blt(sld.x, sld.y, 0,
                  0, 16,
                  56, 56,
                  0)

    def player_will_collide(self, xdir, ydir):
        """Will the player enter a solid thing if they move in the given direction?"""
        out: bool = False
        for w in self.walls:
            if (self.player_x + xdir + 14 >= w.x
                    and self.player_x + xdir <= w.x + 14
                    and self.player_y + ydir + 15 >= w.y
                    and self.player_y + ydir <= w.y + 15):
                out = True
        return out


Game()
