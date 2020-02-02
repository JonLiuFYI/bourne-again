from math import sin, cos, radians

import pyxel
import signals
from target import Target
from solid_sprite import Solid
from player import Player
from flag import Flag

INPUT_PREAMBLE = 'from signals import *\n'


class Game():

    def __init__(self):
        pyxel.init(240, 240, caption='Bourne Again', fps=30)
        pyxel.mouse(True)

        pyxel.load('stuff.pyxres')

        self.seemsg = ''
        self.seemsg_iter = ''
        self.seemsg_out = ''

        self.player = Player(30, 120)

        self.beam_angle = None
        self.beam_start_time = 0

        self.targets = {
            'A': Target(200, 100, 'Target A feels lonely'),
            'B': Target(1, 20, 'Fortune awaits Target B'),
            'C': Target(120, 199, 'Target C is in the mood for shawarma')
        }

        self.walls = [
            Solid(30, 160),
            Solid(100, 45),
            Solid(24, 200)
        ]

        self.flag = Flag(60, 24)

        self.locked = False
        self.has_won = False

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_W):
            self.has_won = True

        if not self.locked and pyxel.btnr(pyxel.KEY_SPACE):
            script = INPUT_PREAMBLE + self.read_input()
            self.reset_vars()
            try:
                self.locked = True
                exec(script)

            except signals.Help:
                self.set_msg(signals.HELP)

            except signals.Credits:
                self.set_msg(signals.CREDITS)

            except signals.See as see:
                """Start typing out info on the named target."""
                if see.msg in self.targets:
                    tgt: Target = self.targets[see.msg]
                    self.set_msg(
                        f'{see.msg} ({tgt.x}, {tgt.y}) - Relative to you: ({tgt.x-self.player.x}, {tgt.y-self.player.y})\n{tgt.comment}')
                else:
                    self.set_msg(f'{see.msg}: no such target')

            except signals.Right as right:
                self.player.deltax = right.dist

            except signals.Left as left:
                self.player.deltax = -left.dist

            except signals.Up as up:
                self.player.deltay = -up.dist

            except signals.Down as down:
                self.player.deltay = down.dist

            except signals.Shoot as shot:
                self.beam_angle = radians(-shot.angle)
                self.beam_start_time = pyxel.frame_count

            except:
                pass

        self.move_player()

        if len(self.seemsg) > 0:
            self.typeout()

    def draw(self):
        pyxel.cls(12)

        # targets
        [self.draw_target(k, t) for k, t in self.targets.items()]

        # walls
        [self.draw_wall(w) for w in self.walls]

        # player
        pyxel.blt(self.player.x, self.player.y, 0,
                  *self.player.sprite(),
                  16, 16,
                  0)

        # shot beam
        if self.beam_angle is not None:
            self.draw_beam(self.beam_angle, self.beam_start_time)

        # draw flag
        pyxel.blt(self.flag.x, self.flag.y, 0,
                  16, 0,
                  16, 16,
                  0)

        # see() text background
        for l, txt in enumerate(self.seemsg_out.splitlines()):
            pyxel.rect(0, 6*l,
                       4*len(txt) + 2, 7,
                       1)

        # see() text
        pyxel.text(1, 1, self.seemsg_out, 7)

        # exec prompt
        if not self.locked:
            pyxel.rect(0, 232,
                       240, 8, 0)
            pyxel.text(0, 234, '[SPACE] run INPUT', 7)

        if self.has_won:
            pyxel.cls(0)
            pyxel.blt(64, 64, 0,
                      0, 32,
                      84, 20,
                      0)

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
        # block move if player would collide
        if ((self.player.deltax > 0 and self.player_will_collide(1, 0))
                or (self.player.deltax < 0 and self.player_will_collide(-1, 0))
                or (self.player.deltay > 0 and self.player_will_collide(0, 1))
                or (self.player.deltay < 0 and self.player_will_collide(0, -1))):
            self.player.stop()
        else:
            self.player.update_pos()

        if self.player.stopped():
            self.locked = False
            self.player.reset_anim()
        else:
            if pyxel.frame_count % 6 == 0:
                self.player.step_anim()

        self.has_won = self.player_touching_flag()
        if self.has_won:
            self.player.stop()

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

        eye1 = (self.player.x + 5, self.player.y + 4)
        eye2 = (self.player.x + 10, self.player.y + 4)
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
                  16, 16,
                  0)

    def player_will_collide(self, xdir, ydir):
        """Will the player enter a solid thing if they move in the given direction?"""
        out: bool = False
        for w in self.walls:
            if (self.player.x + xdir + 14 >= w.x
                    and self.player.x + xdir <= w.x + 14
                    and self.player.y + ydir + 15 >= w.y
                    and self.player.y + ydir <= w.y + 15):
                out = True
        return out

    def player_touching_flag(self):
        """Is the player touching the flag?"""
        if (self.player.x + 9 >= self.flag.x
                and self.player.x <= self.flag.x + 9
                and self.player.y + 16 >= self.flag.y
                and self.player.y <= self.flag.y + 16):
            return True
        return False


Game()
