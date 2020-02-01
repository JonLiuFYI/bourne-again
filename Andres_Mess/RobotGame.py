import pyxel
import time
import math

class RobotGame:
    def __init__(self):
        pyxel.init(256,256, caption = "Robot")

        pyxel.load("assests/my_resource.pyxres")

        #self.robot = 0
        self.player_x = 15
        self.player_y = 16

        self.flag_x = 32
        self.flag_y = 64

        self.target_x = 15
        self.target_y = 60

        self.ball_x = 32
        self.ball_y = 16

        self.waitTime =0.2
        self.currentWaitTime = 0
        self.isWaiting = False

        self.info_text = ""
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        #move tests
        if pyxel.btnp(pyxel.KEY_LEFT):
            self.move_robot_left(4)

        if pyxel.btnp(pyxel.KEY_RIGHT):
            self.move_robot_right(4)

        #move tests
        if pyxel.btnp(pyxel.KEY_UP):
            self.move_robot_up(4)

        if pyxel.btnp(pyxel.KEY_DOWN):
            self.move_robot_down(4)

        if pyxel.btnp(pyxel.KEY_SPACE):
            print("space")
            self.setInfoText("Test")

        self.check_win_collision()

        if pyxel.btnp(pyxel.KEY_Y):
            self.get_target_location()

            print( math.degrees(math.atan2(self.target_y - self.player_y, self.target_x - self.player_x)))


    def move_robot_right(self, moveX):
        print("move right")
        for _ in range(moveX):
            self.player_x += 1
            #time.sleep(0.2)

    def move_robot_left(self, moveX):
        print("move left")
        for _ in range(moveX):
            self.player_x += -1
            #time.sleep(0.2)

    def move_robot_up(self, moveY):
        print("move up")
        for _ in range(moveY):
            self.player_y += -1
            #time.sleep(0.2)

    def move_robot_down(self, moveY):
        print("move down")
        for _ in range(moveY):
            self.player_y += 1
            #time.sleep(0.2)



    #set info text
    def setInfoText(self, message):
        self.info_text = message

    # print text to screen
    def writeToScreen(self):
        if self.info_text != "":
            pyxel.text(0,0,self.info_text, 6)
            #self.info_text = ""


    # MOVE PLAYER
    def update_robot(self, moveX, moveY):
            self.player_x += moveX
            self.player_y += moveY

    # MOVE TARGET
    def update_target(self, moveX, moveY):
            self.target_x += moveX
            self.target_y += moveY

    # MOVE BLL
    def update_ball(self, moveX, moveY):
            self.ball_x += moveX
            self.ball_y += moveY


    #SHOW LOCATION OF TARGET
    def get_target_location(self):
        print("Get target location")
        self.setInfoText("("+str(self.target_x)+", "+str(self.target_y)+")")
        #self.writeToScreen()

    #SHOOT
    def shoot_at_target(self, angle):
        if math.degrees(math.atan2(self.target_y - self.player_y, self.target_x - self.player_x)) < angle + 1 and  math.degrees(math.atan2(self.target_y - self.player_y, self.target_x - self.player_x)) > angle - 1:
            print("Corrcet!")

    #COLLISION BETWEEN PLAYER AND FLAG
    def check_win_collision(self):
         if (
                self.player_x + 9 >= self.flag_x
                and self.player_x <= self.flag_x + 9
                and self.player_y + 16 >= self.flag_y
                and self.player_y <= self.flag_y + 16
            ):
                print("WIN!")







    def draw(self):
        #draw background
        pyxel.cls(12)
         # draw robot
        pyxel.blt(
            self.player_x,
            self.player_y,
            0,
            0,
            0,
            16,
            16,
            0,
            )

         #draw target
        pyxel.blt(
            self.flag_x,
            self.flag_y,
            0,
            16,
            0,
            16,
            16,
            0,
            )

        #draw target
        pyxel.blt(
            self.target_x,
            self.target_y,
            0,
            32,
            0,
            16,
            16,
            0,
            )
         #draw ball
        pyxel.blt(
            self.ball_x,
            self.ball_y,
            0,
            48,
            0,
            16,
            16,
            0,
            )


        self.writeToScreen()

RobotGame()