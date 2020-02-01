import pyxel


class Game:

    def __init__(self):
        pyxel.init(240, 240, caption='Bourne Again', fps=30)
        self.read_input()
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnr(pyxel.KEY_SPACE):
            self.read_input()
            exec(self.text)

    def draw(self):
        pyxel.cls(0)
        pyxel.text(0, 235, '[SPACE] run INPUT', 10)

    def read_input(self):
        """Get all the text from the INPUT file."""
        self.f = open('INPUT', 'r')
        self.text = self.f.read()
        self.f.close()


if __name__ == '__main__':
    Game()
