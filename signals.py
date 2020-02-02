HELP = """Enter commands to do stuff.
    help() - See this message
    see('target_name') - See a target's info
    right(distance)
    left(distance)
    up(distance)
    down(distance) - Move that many pixels over
    shoot(angle) - Shoot a beam at that angle

    credits() - Who made this, anyway?
"""

START_HELP = """Enter commands to do stuff.
    help() - See this message
    see('target_name') - See a target's info
    right(distance) - Move that many pixels over
    shoot(angle) - Shoot a beam at that angle

    credits() - Who made this, anyway?
"""

CREDITS = """Bourne Again
by Team Absolute Baseline

Jon Liu: code, music
Andre Giroux: code, graphics

Global Game Jam 2020 at Shopify, in Ottawa
"""


class Help(Exception):
    def __init__(self):
        pass


class See(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class Credits(Exception):
    def __init__(self):
        pass


class Move(Exception):
    def __init__(self, dist: int):
        self.dist = dist


class Right(Move):
    pass


class Left(Move):
    pass


class Up(Move):
    pass


class Down(Move):
    pass


class Shoot(Exception):
    def __init__(self, angle: float):
        self.angle = angle

###############################


def help():
    """Display a docstring with help info"""
    raise Help


def see(msg: str):
    """Display location of a target"""
    raise See(msg)


def credits():
    """Show credits."""
    raise Credits


def right(dist: int):
    """Move right by the specified number of pixels."""
    raise Right(dist)


def left(dist: int):
    raise Left(dist)


def up(dist: int):
    raise Up(dist)


def down(dist: int):
    raise Down(dist)


def shoot(angle: float):
    raise Shoot(angle)
