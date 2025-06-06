# title: Pyxel Jump
# author: Takashi Kitao
# desc: A Pyxel simple game example
# site: https://github.com/kitao/pyxel
# license: MIT
# version: 1.0

import pyxel


class App:
    def __init__(self):
        self.screen_x = 160
        self.screen_y = 120
        pyxel.init(self.screen_x, self.screen_y, title="Platformer")
        pyxel.load("assets/platformer.pyxres")
        # self.score = 0
        self.ground_level = 72
        self.player_x = 16
        self.player_dx = 1
        self.player_y = self.ground_level
        self.player_dy = 0
        # self.is_alive = True
        # self.far_cloud = [(-10, 75), (40, 65), (90, 60)]
        # self.near_cloud = [(10, 25), (70, 35), (120, 15)]
        self.floor = [(i * 60, pyxel.rndi(8, 104), True) for i in range(4)]
        # self.fruit = [
        #     (i * 60, pyxel.rndi(0, 104), pyxel.rndi(0, 2), True) for i in range(4)
        # ]
        pyxel.playm(0, loop=True)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.update_player()
        # for i, v in enumerate(self.floor):
        #     self.floor[i] = self.update_floor(*v)
        # for i, v in enumerate(self.fruit):
        #     self.fruit[i] = self.update_fruit(*v)

    def update_player(self):
        # if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
        #     self.player_x = max(self.player_x - 2, 0)
        # if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
        #     self.player_x = min(self.player_x + 2, pyxel.width - 16)
        # self.player_y += self.player_dy
        # self.player_dy = min(self.player_dy + 1, 8)

        # if self.player_y > pyxel.height:
        #     if self.is_alive:
        #         self.is_alive = False
        #         pyxel.play(3, 5)
        #     if self.player_y > 600:
        #         self.score = 0
        #         self.player_x = 72
        #         self.player_y = -16
        #         self.player_dy = 0
        #         self.is_alive = True
        branch_left = 114
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            self.player_x = max(self.player_x - 4, 0)
            self.player_dx = -1
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            self.player_x = min(self.player_x + 4, self.screen_x-16)
            self.player_dx = 1
        if (pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP)) and self.player_dy == 0:
            self.player_dy = -6
        if self.player_y == 36:
            self.player_dy = 6
        if self.player_y < self.ground_level and self.player_dy == 0 and not (self.player_x >= branch_left and self.player_x < branch_left+7):
            self.player_dy = 6
        if self.player_dy < 0:
            self.player_y = max(self.player_y + self.player_dy, 36)
        elif self.player_dy > 0:
            if self.player_x >= branch_left and self.player_x < branch_left+7 and self.player_y > 53:
                self.player_y = min(self.player_y + self.player_dy, 53)
                if self.player_y == 53:
                    self.player_dy = 0
            else:
                self.player_y = min(self.player_y + self.player_dy, self.ground_level)
        if self.player_y == self.ground_level:
            self.player_dy = 0

    def update_floor(self, x, y, is_alive):
        if is_alive:
            if (
                self.player_x + 16 >= x
                and self.player_x <= x + 40
                and self.player_y + 16 >= y
                and self.player_y <= y + 8
                and self.player_dy > 0
            ):
                is_alive = False
                self.score += 10
                self.player_dy = -12
                pyxel.play(3, 3)
        else:
            y += 6
        x -= 4
        if x < -40:
            x += 240
            y = pyxel.rndi(8, 104)
            is_alive = True
        return x, y, is_alive

    # def update_fruit(self, x, y, kind, is_alive):
    #     if is_alive and abs(x - self.player_x) < 12 and abs(y - self.player_y) < 12:
    #         is_alive = False
    #         self.score += (kind + 1) * 100
    #         self.player_dy = min(self.player_dy, -8)
    #         pyxel.play(3, 4)
    #     x -= 2
    #     if x < -40:
    #         x += 240
    #         y = pyxel.rndi(0, 104)
    #         kind = pyxel.rndi(0, 2)
    #         is_alive = True
    #     return (x, y, kind, is_alive)

    def draw(self):
        pyxel.cls(6)

        # Draw sky
        # pyxel.blt(0, 88, 0, 0, 88, 160, 32)

        # Draw Floor
        for i in range(self.screen_x//16):
            pyxel.blt(i*16, 88, 0, 48, 0, 16, 8)
        for j in range(3):
            for i in range(self.screen_x//16):
                pyxel.blt(i*16, 88+(j+1)*8, 0, 48, 8, 16, 8)

        # Draw trees
        # offset = pyxel.frame_count % 160
        # for i in range(2):
        #     pyxel.blt(i * 160 - offset, 104, 0, 0, 48, 160, 16, 12)

        # # Draw clouds
        # offset = (pyxel.frame_count // 16) % 160
        # for i in range(2):
        #     for x, y in self.far_cloud:
        #         pyxel.blt(x + i * 160 - offset, y, 0, 64, 32, 32, 8, 12)
        # offset = (pyxel.frame_count // 8) % 160
        # for i in range(2):
        #     for x, y in self.near_cloud:
        #         pyxel.blt(x + i * 160 - offset, y, 0, 0, 32, 56, 8, 12)

        # # Draw floors
        # for x, y, is_alive in self.floor:
        #     pyxel.blt(x, y, 0, 0, 16, 40, 8, 12)

        # # Draw fruits
        # for x, y, kind, is_alive in self.fruit:
        #     if is_alive:
        #         pyxel.blt(x, y, 0, 32 + kind * 16, 0, 16, 16, 12)
                
        # Draw tree
        pyxel.blt(
            120, 45,
            0,
            16, 16,
            32, 48,
            6
        )

        # Draw player
        if self.player_dy == 0:
            pic = (0, 16)
        elif self.player_dy > 0:
            pic = (0, 32)
        elif self.player_dy < 0:
            pic = (0, 48)
        else:
            raise Exception(f"I don't know how you got here. self.player.dy = {self.player.dy}")
        pyxel.blt(
            self.player_x, self.player_y,
            0,
            # 16 if self.player_dy > 0 else 0,
            pic[0], pic[1],
            16 * self.player_dx, 16,
            6,
        )

        # # Draw score
        # s = f"SCORE {self.score:>4}"
        # pyxel.text(5, 4, s, 1)
        # pyxel.text(4, 4, f"{self.player_dy}", 7)
        # pyxel.text(4, 12, f"{self.player_y}", 1)


App()
