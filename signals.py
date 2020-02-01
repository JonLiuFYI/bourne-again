HELP = """Enter commands to do stuff.
    help() - See this message
    see(target_name) - See a target's info
    right(distance)
    left(distance)
    up(distance)
    down(distance) - Move that many pixels over
"""


class Help(Exception):
    def __init(self):
        pass


class See(Exception):
    def __init__(self, msg):
        self.msg = msg


class Move(Exception):
    def __init__(self, dist):
        self.dist = dist


class Right(Move):
    pass


class Left(Move):
    pass


class Up(Move):
    pass


class Down(Move):
    pass

###############################


def help():
    """Display a docstring with help info"""
    raise Help


def see(msg):
    """Display location of a target"""
    raise See(msg)


def right(dist):
    """Move right by the specified number of pixels."""
    raise Right(dist)


def left(dist):
    raise Left(dist)


def up(dist):
    raise Up(dist)


def down(dist):
    raise Down(dist)
