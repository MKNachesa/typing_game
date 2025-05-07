# title: Pyxel Jump
# author: Takashi Kitao
# desc: A Pyxel simple game example
# site: https://github.com/kitao/pyxel
# license: MIT
# version: 1.0

import json
import pyxel
import random

# TO-DO: add victory dance (without conflicting with player movements)
class App:
    def __init__(self):
        self.mapping = {"а": "f",
                     "о": "j",
                     "в": "d",
                     "л": "k",
                     "ы": "s",
                     "д": "l",
                     "ф": "a",
                     "ж": ";",
                     "п": "g",
                     "р": "h",
                     "к": "r",
                     "г": "u",
                     "е": "t",
                     "н": "y",
                     "м": "v",
                     "ь": "m",
                     "и": "b",
                     "т": "n",
                     "у": "e",
                     "ш": "i", # TODO: make bird face forward when pressing the arrow key down
                     "щ": "o", # TODO: make bird face backward when entering door to next level (also, delay next level animation to achieve that)
                     "с": "c",
                     "ц": "w",
                     "щ": "o",
                     "ч": "x",
                     "й": "q",
                     "з": "p",
                     "я": "z",
                     "б": ",",
                     "ю": ".",
                     "х": "[",
                     "э": "'",
                     "ъ": "]",
                     "ё": "`",
                     'А': 'F', 
                     'О': 'J', 
                     'В': 'D', 
                     'Л': 'K', 
                     'Ы': 'S', 
                     'Д': 'L', 
                     'Ф': 'A', 
                     'Ж': ';', 
                     'П': 'G', 
                     'Р': 'H', 
                     'К': 'R', 
                     'Г': 'U', 
                     'Е': 'T', 
                     'Н': 'Y', 
                     'М': 'V',
                     'Ь': 'M', 
                     'И': 'B', 
                     'Т': 'N', 
                     'У': 'E', 
                     'Ш': 'I', 
                     'Щ': 'O', 
                     'С': 'C', 
                     'Ц': 'W', 
                     'Ч': 'X', 
                     'Й': 'Q', 
                     'З': 'P', 
                     'Я': 'Z', 
                     'Б': ',', 
                     'Ю': '.', 
                     'Х': '{', 
                     'Э': "\"", 
                     'Ъ': '}',
                     "Ë": "~",
                     ' ': ' ',
                     ".": "/"}
        
        self.shift_to_lower_mapping = {
            "А": "а", 
            "О": "о",
            "В": "в",
            "Л": "л",
            "Ы": "ы",
            "Д": "д",
            "Ф": "ф",
            "Ж": "ж",
            "П": "п", 
            "Р": "р", 
            "К": "к", 
            "Г": "г", 
            "Е": "е", 
            "Н": "н", 
            "М": "м", 
            "Ь": "ь", 
            "И": "и", 
            "Т": "т", 
            "У": "у", 
            "Ш": "ш", 
            "С": "с", 
            "Ц": "ц", 
            "Щ": "щ", 
            "Ч": "ч", 
            "Й": "й", 
            "З": "з", 
            "Я": "я", 
            "Б": "б", 
            "Ю": "ю", 
            "Х": "х", 
            "Э": "э", 
            "Ъ": "ъ",
            "%": "5", 
            ":": "6", 
            ";": "4", 
            "?": "7", 
            "№": "3", 
            "*": "8", 
            "\"": "2", 
            "(": "9", 
            "!": "1", 
            ")": "0", 
            "Ë": "ё", 
            ",": ".", 
            "/": "\\", 
            "_": "-",
            "+": "="
        }

        self.shift_left = {'О', 'Л', 'Д', 'Ж', 'Р', 'Г', 'Н', 'Ь', 'Т', 'Ш', 'Щ', 'З', 'Б', 'Ю', 'Х', 'Э', 'Ъ', ':', '?', '*', '(', ')', ',', '/', '_', '+'}
        self.shift_right = {'А', 'В', 'Ы', 'Ф', 'П', 'К', 'Е', 'М', 'И', 'У', 'С', 'Ц', 'Ч', 'Й', 'Я', '%', ';', '№', '"', '!', 'Ë'}
        
        self.screen_x = 400
        self.screen_y = 225
        pyxel.init(self.screen_x, self.screen_y, title="Platformer")
        pyxel.load("assets/platformer.pyxres")
        self.game_state = "menu"
        with open("key_positions.json", "r") as f:
            self.key_positions = json.load(f)
        # self.score = 0
        self.ground_level = 72
        self.player_x = 16
        self.player_dx = 1
        self.player_y = self.ground_level
        self.player_dy = 0
        self.letter_order = [" ", 
                             "а", "о", "в", "л", "ы", "д", "ф", "ж", 
                             "п", "р", "к", "г", "е", "н", "м", "ь", 
                             "и", "т", "у", "ш", "с", "ц", "щ", "ч", 
                             "й", "з", "я", "б", "ю", "х", "э", "ъ", # TODO: make levels past ъ possible
                             "5", "6", "4", "7", "3", "8", "2", "9", 
                             "1", "0", "ё", ".", "\\", "-",

                             "=", ",",
                             "А", "О", "В", "Л", "Ы", "Д", "Ф", "Ж", 
                             "П", "Р", "К", "Г", "Е", "Н", "М", "Ь", 
                             "И", "Т", "У", "Ш", "С", "Ц", "Щ", "Ч", 
                             "Й", "З", "Я", "Б", "Ю", "Х", "Э", "Ъ",
                             "%", ":", ";", "?", "№", "*", "\"", "(",
                             "!", ")", "Ë", "+", "/", "_"]
        self.num_letters = (400 - 32) // 16
        self.level = 0
        self.level_delta = 0
        self.level_type = "showcase"
        self.letters = self.set_letters()
        self.last_button_pressed = " "
        self.finger_positions = ["ф", "ы", "в", "а", "о", "л", "д", "ж"]
        # self.is_alive = True
        # self.far_cloud = [(-10, 75), (40, 65), (90, 60)]
        # self.near_cloud = [(10, 25), (70, 35), (120, 15)]
        self.floor = [(i * 60, pyxel.rndi(8, 104), True) for i in range(4)]
        self.keyboard_fill = 0
        self.menu_choice = 0
        # self.fruit = [
        #     (i * 60, pyxel.rndi(0, 104), pyxel.rndi(0, 2), True) for i in range(4)
        # ]
        pyxel.playm(0, loop=True)
        pyxel.run(self.update, self.draw)

    
    def set_finger_positions(self):
        self.finger_positions = ["ф", "ы", "в", "а", "о", "л", "д", "ж", " "]
        if self.game_state == "game":
            if len(self.letters) > 0:
                cur_letter = self.letter_order[self.letters[-1]]
                cur_letter = self.shift_to_lower_mapping.get(cur_letter, cur_letter)
                if cur_letter not in self.finger_positions and cur_letter != " ":
                    if cur_letter in {"п", "е", "к", "и", "м", "4", "5"}:
                        idx_to_change = 3
                    elif cur_letter in {"у", "3", "с"}:
                        idx_to_change = 2
                    elif cur_letter in {"ц", "2", "ч"}:
                        idx_to_change = 1
                    elif cur_letter in {"й", "1", "я", "ё"}:
                        idx_to_change = 0
                    elif cur_letter in {"6", "7", "г", "н", "р", "т", "ь"}:
                        idx_to_change = 4
                    elif cur_letter in {"8", "ш", "б"}:
                        idx_to_change = 5
                    elif cur_letter in {"9", "щ", "ю"}:
                        idx_to_change = 6
                    elif cur_letter in {"0", "з", "х", "э", "ъ", "\\", "-", "=", "."}:
                        idx_to_change = 7
                    self.finger_positions[idx_to_change] = cur_letter

    
    def set_letters(self):
        if self.level_type == "all":
            choice_list = list(range(0, self.level*2 + 3))
        elif self.level_type == "showcase":
            letters = []
            for _ in range(5):
                letters.append(self.level*2+2)
                letters.append(self.level*2+1)
            # choice_list = list(range(self.level*2, self.level*2 + 2))
            # num_letters = 10
        elif self.level_type == "intro":
            choice_list = list(range(self.level*2+1, self.level*2+3)) + [0]
        if self.level_type != "showcase":
            letters = random.choices(choice_list, k=self.num_letters)
            # letters = [(pyxel.rndi(0, self.level*2 + 2), True) for _ in range(self.num_letters)] # TODO: make space less frequent

        return letters


    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

        if pyxel.btnp(pyxel.KEY_BACKSPACE):
            self.game_state = "menu"
            self.set_finger_positions()
            self.level = (self.level - self.level_delta) % ((len(self.letter_order)-1) // 2)
            self.level_delta = 0

        self.update_keyboard()
        if self.game_state == "game":
            self.update_game()
            self.update_player()
            self.set_finger_positions()
        elif self.game_state == "menu":
            self.update_menu()
        elif self.game_state == "choose_level":
            self.update_choose_level()
        elif self.game_state == "instructions":
            self.update_player()


    def update_game(self):
        if len(self.letters) == 0:
            if self.level_type == "showcase":
                self.level_type = "intro"
                self.set_level()
            else:
                self.player_change_level()


    def update_menu(self):
        if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            self.menu_choice = (self.menu_choice - 1) % 3
        if pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            self.menu_choice = (self.menu_choice + 1) % 3

        if pyxel.btnp(ord(" ")) or pyxel.btnp(pyxel.KEY_RETURN):
            if self.menu_choice == 0:
                self.game_state = "game"
                self.letters = self.set_letters() # TODO: make next level also possible with enter
                self.player_x = 0
                self.player_dx = 1
                self.player_y = self.ground_level
                self.player_dy = 0
            elif self.menu_choice == 1:
                self.game_state = "choose_level"
                self.player_x = 0
                self.player_dx = 1
                self.player_y = self.ground_level
                self.player_dy = 0
            elif self.menu_choice == 2:
                self.game_state = "instructions"


    def update_choose_level(self):
        repeat = 4
        if pyxel.btnp(pyxel.KEY_LEFT, repeat=repeat) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT, repeat=repeat):
            # if self.level > 0:
            self.level_delta -= 1
            self.level = (self.level - 1) % ((len(self.letter_order)-1) // 2)
                
        if pyxel.btnp(pyxel.KEY_RIGHT, repeat=repeat) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT, repeat=repeat):
            # if self.level < (len(self.letter_order)-1)//2:
            self.level_delta += 1
            self.level = (self.level + 1) % ((len(self.letter_order)-1) // 2)

        if pyxel.btnp(ord(" ")) or pyxel.btnp(pyxel.KEY_RETURN):
            self.game_state = "menu"
            self.level_delta = 0
            self.level_type = "showcase"
            self.letters = self.set_letters()


    def update_player(self):
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
        if self.game_state == "game":
            correct = False
            if len(self.letters) > 0:
                key = self.letter_order[self.letters[-1]]
            # self.last_button_pressed = self.letter_order[self.letters[-1]]
                if key in self.shift_to_lower_mapping:
                    key = self.shift_to_lower_mapping.get(key, key)
                    # if (pyxel.btnp(ord(key)) or pyxel.btnp(ord(self.mapping.get(key, key)))) and pyxel.btn(pyxel.KEY_SHIFT):
                    if (pyxel.btnp(ord(self.mapping.get(key, key)))) and pyxel.btn(pyxel.KEY_SHIFT):

                        correct = True
                # print(self.last_button_pressed)
                # print(pyxel.btnp(ord(self.mapping[key])))
                else:
                    # if (pyxel.btnp(ord(key)) or pyxel.btnp(ord(self.mapping.get(key, key)))):
                    if (pyxel.btnp(ord(self.mapping.get(key, key)))):

                        correct = True
                if correct:
                    self.letters = self.letters[:-1]
                    self.player_x = (32 + (self.num_letters - (len(self.letters)) - 1) * 16)
                    self.player_y = self.ground_level
                    self.player_dx = 1
                    self.player_dy = 0
            # self.last_button_pressed = 1072


    def update_keyboard(self):
        if pyxel.btnp(pyxel.KEY_TAB):
            self.keyboard_fill = (self.keyboard_fill + 1) % 3


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


    def draw_key_background(self, x, y, key_width=18, key_height=18, function="none", keyboard=True):
        if keyboard:
            x += (self.screen_x - 274) // 2 - 16
        if key_height == 18:
            sprite_x = 96
        else:
            sprite_x = 152
        sprite_y = 64
        # left part
        pyxel.blt(x, y,
                  0,
                  sprite_x, sprite_y,
                  2, key_height)
        # middle part
        for i in range(key_width-4):
            pyxel.blt(x+2+i, y,
                  0,
                  sprite_x+2, sprite_y,
                  1, key_height)
        # right part
        pyxel.blt(x+key_width-2, y,
                  0,
                  sprite_x+18-2, sprite_y,
                  2, key_height)
        
        if function == "position":
            sprite_y = 117 if key_height == 18 else 179
            for i in range(key_width-6):
                pyxel.blt(x+2+i+1, y,
                    0,
                    sprite_y, 64,
                    1, key_height,
                    0)
        elif function == "press":
            sprite_y = 135 if key_height == 18 else 195
            for i in range(key_width-6):
                pyxel.blt(x+2+i+1, y,
                    0,
                    sprite_y, 64,
                    1, key_height,
                    0)
                

    def draw_key(self, key_name, function="None", fill_keyboard=True, x=None, y=None):
        key = self.key_positions[key_name]
        if not (x and y):
            x, y = key["screen_pos"]
        sprite_x, sprite_y = key["sprite_pos"][function]
        sprite_width, sprite_height = key["size"]
        background_colour = key["background"]
        width = key["width"]
        height = sprite_height+sprite_height//8
        shift = key.get("shift", 0)
        self.draw_key_background(x, y, width, height, function)
        if fill_keyboard:
            x += (self.screen_x - 274) // 2 - 16
            pyxel.blt(x+1+shift, y+1,
                    0,
                    sprite_x, sprite_y,
                    sprite_width, sprite_height,
                    background_colour)
        

    def draw_sequence(self):
        for i, letter in enumerate(self.letters):
            img = 0
            key_name = self.letter_order[letter]
            if ord(key_name) not in list(range(1072, 1104)) + [1105] + list(range(1040, 1072)) + [203] and key_name != " ":
                key_name = f"{key_name}_sequence"
                img = 1
            if "sequence" not in key_name and ord(key_name) in list(range(1040, 1072)) + [203]:
                key_name = key_name.lower()
                img = 1
            key = self.key_positions[key_name]
            # offset = 13 * 16 if self.level_type == "showcase" else 0
            x = self.screen_x - 16 * (i+1)
            y = self.ground_level
            sprite_x, sprite_y = key["sprite_pos"]["None"]
            sprite_width, sprite_height = key["size"]
            background_colour = key["background"]
            pyxel.blt(x, y,
                        0,
                        0, 80,
                        16, 16)
            pyxel.blt(x, y,
                        img,
                        sprite_x, sprite_y,
                        16, 16,
                        0)
                
    def draw_keyboard(self):
        if self.keyboard_fill == 2:
            fill_keyboard = False
        else:
            fill_keyboard = True
        for key in self.key_positions:
            if "sequence" in key:
                continue
            self.draw_key(key, function="None", fill_keyboard=fill_keyboard)

        if self.keyboard_fill == 0:
            for key in self.finger_positions:
                key = self.shift_to_lower_mapping.get(key, key)
                self.draw_key(key, function="position")

            if len(self.letters) > 0 and self.game_state == "game":
                key = self.letter_order[self.letters[-1]]
                if key in self.shift_left:
                    self.draw_key("shift_left", function="press")
                elif key in self.shift_right:
                    self.draw_key("shift_right", function="press")
                key = self.shift_to_lower_mapping.get(key, key)
                self.draw_key(key, function="press")

    
    def draw_floor(self):
        for i in range(self.screen_x//16):
            pyxel.blt(i*16, 88, 0, 48, 0, 16, 8)
        for j in range(17):
            for i in range(self.screen_x//16):
                pyxel.blt(i*16, 88+(j+1)*8, 0, 48, 8, 16, 8)
            

    def draw_doors(self):
        x_pos = 313
        pyxel.text(x_pos, self.ground_level - 27, f"prev", 1)
        pyxel.text(x_pos - 1, self.ground_level - 20, f"level", 1)
        pyxel.blt(  # hitbox door 1: x = 302:326 (excl), y = self.ground_level-8:self.ground_level+18 (excl)
            x_pos + 1, self.ground_level - 8,
            1,
            0, 0,
            16, 16,
            0,
            scale=2
        )

        pyxel.text(x_pos + 31, self.ground_level - 27, f"same", 1)
        pyxel.text(x_pos - 1 + 31, self.ground_level - 20, f"level", 1)
        pyxel.blt( # hitbox door 2: x = 333:357 (excl), y = self.ground_level-8:self.ground_level+18 (excl)
            x_pos + 1 + 31, self.ground_level - 8,
            1,
            0, 0,
            16, 16,
            0,
            scale=2
        )

        pyxel.text(x_pos + 62, self.ground_level - 27, f"next", 1)
        pyxel.text(x_pos - 1 + 62, self.ground_level - 20, f"level", 1)
        pyxel.blt( # hitbox door 2: x = 364:388 (excl), y = self.ground_level-8:self.ground_level+18 (excl)
            x_pos + 1 + 62, self.ground_level - 8,
            1,
            0, 0,
            16, 16,
            0,
            scale=2
        )

        if self.player_x >= 313 - 8 and self.player_x < 337 - 8 and self.player_y >= self.ground_level-16 and self.player_y < self.ground_level + 18 - 8:
            self.draw_key(" ", function="press")

        elif self.player_x >= 344 - 8 and self.player_x < 368 - 8 and self.player_y >= self.ground_level-16 and self.player_y < self.ground_level + 18 - 8:
            self.draw_key(" ", function="press")

        elif self.player_x >= 375 - 8 and self.player_x < 399 - 8 and self.player_y >= self.ground_level-16 and self.player_y < self.ground_level + 18 - 8:
            self.draw_key(" ", function="press")


    def draw_player(self):
        if self.player_dy == 0:
            pic = (0, 16)
        elif self.player_dy > 0:
            pic = (0, 32)
        elif self.player_dy < 0:
            pic = (0, 48)
        else:
            raise Exception(f"I don't know how you got here. self.player.dy = {self.player_dy}")
        pyxel.blt(
            self.player_x, self.player_y,
            0,
            # 16 if self.player_dy > 0 else 0,
            pic[0], pic[1],
            16 * self.player_dx, 16,
            6,
        )


    def set_level(self):
        self.letters = self.set_letters()
        self.player_x = 16
        self.player_y = self.ground_level
        self.player_dx = 1
        self.player_dy = 0


    def player_change_level(self):
        # x_pos = 313 (= + 11)
        if self.player_x >= 313 - 8 and self.player_x < 337 - 8 and self.player_y >= self.ground_level-16 and self.player_y < self.ground_level + 18 - 8:
            if pyxel.btnp(ord(" ")) and self.level >= 1:
                self.level_type = "intro"
                self.level -= 1
                self.set_level()

        elif self.player_x >= 344 - 8 and self.player_x < 368 - 8 and self.player_y >= self.ground_level-16 and self.player_y < self.ground_level + 18 - 8:
            if pyxel.btnp(ord(" ")):
                self.set_level()  

        elif self.player_x >= 375 - 8 and self.player_x < 399 - 8 and self.player_y >= self.ground_level-16 and self.player_y < self.ground_level + 18 - 8:
            if pyxel.btnp(ord(" ")):
                if self.level_type == "intro":
                    self.level_type = "all"
                elif self.level_type == "all" and self.level < ((len(self.letter_order)-1) // 2) - 1:
                    self.level += 1
                    self.level_type = "showcase" # TODO: make first and last door do nothing for first and last level
                self.set_level()


    def draw_game(self):
        if len(self.letters) == 0 and self.level_type != "showcase":
            self.draw_doors()
        self.draw_sequence()
    
        pyxel.text(4, 4, f"level {self.level+1}", 7) # TODO: make recent letters more frequent
        pyxel.text(4, 12, f"{self.level_type}", 1)


    def draw_menu(self, choice):
        pyxel.blt(
            (400-128)//2, self.ground_level-48,
            1,
            # 16 if self.player_dy > 0 else 0,
            0, 16,
            128, 16,
            0,
        )
        pyxel.text((400-22*3)//2, self.ground_level-28, f"For my staartmees", 7)

        functions = ["None", "None", "None"]
        colours = [7, 7, 7]
        if choice == 0:
            functions[0] = "press"
            colours[0] = 8
        elif choice == 1:
            functions[1] = "press"
            colours[1] = 8
        elif choice == 2:
            functions[2] = "press"
            colours[2] = 8

        self.draw_key_background(119, self.ground_level+23, 47, 18, functions[0], keyboard=False)
        pyxel.text(123, self.ground_level+29, f"Start game", colours[0])

        self.draw_key_background(169, self.ground_level+23, 55, 18, functions[1], keyboard=False)
        pyxel.text(173, self.ground_level+29, f"Choose level", colours[1])

        self.draw_key_background(227, self.ground_level+23, 55, 18, functions[2], keyboard=False)
        pyxel.text(231, self.ground_level+29, f"Instructions", colours[2])

        self.draw_key(" ", function="press")
        self.draw_key("return", function="press")
        self.draw_key("left", function="press")
        self.draw_key("right", function="press")


    def draw_choose_level(self):
        # pyxel.text(16, self.ground_level+29, "a", 8)
        self.draw_key(" ", function="press")
        self.draw_key("return", function="press")
        self.draw_key("left", function="press")
        self.draw_key("right", function="press")
        for order_in_sequence, i in enumerate(range(1, 47, 2)):
            img = 0
            letter = key_name = self.letter_order[i]
            # key_name = self.letter_order[letter]
            if ord(key_name) not in list(range(1072, 1104)) + [1105] + list(range(1040, 1072)) + [203]:
                key_name = f"{key_name}_sequence"
                img = 1
            if "sequence" not in key_name and ord(key_name) in list(range(1040, 1072)) + [203]:
                key_name = key_name.lower()
                img = 1
            key = self.key_positions[key_name]
            # offset = 13 * 16 if self.level_type == "showcase" else 0
            x = 16 + 16 * order_in_sequence # self.screen_x - 16 * (i+1)
            y = self.ground_level - 16 - 32
            sprite_x, sprite_y = key["sprite_pos"]["None"]
            sprite_width, sprite_height = key["size"]
            background_colour = key["background"]
            if i < self.level * 2 + 3:
                pyxel.blt(x, y,
                            0,
                            152, 80,
                            16, 16)
            else:
                pyxel.blt(x, y,
                            0,
                            0, 80,
                            16, 16)
            pyxel.blt(x, y,
                        img,
                        sprite_x, sprite_y,
                        16, 16,
                        0)
        for order_in_sequence, i in enumerate(range(2, 47, 2)):
            img = 0
            letter = key_name = self.letter_order[i]
            # key_name = self.letter_order[letter]
            # print(key_name)
            if ord(key_name) not in list(range(1072, 1104)) + [1105] + list(range(1040, 1072)) + [203]:
                key_name = f"{key_name}_sequence"
                img = 1
            if "sequence" not in key_name and ord(key_name) in list(range(1040, 1072)) + [203]:
                key_name = key_name.lower()
                img = 1
            key = self.key_positions[key_name]
            # offset = 13 * 16 if self.level_type == "showcase" else 0
            x = 16 + 16 * order_in_sequence # self.screen_x - 16 * (i+1)
            y = self.ground_level - 32
            sprite_x, sprite_y = key["sprite_pos"]["None"]
            sprite_width, sprite_height = key["size"]
            background_colour = key["background"]
            if i < self.level * 2 + 3:
                pyxel.blt(x, y,
                            0,
                            152, 80,
                            16, 16)
            else:
                pyxel.blt(x, y,
                            0, # TODO: make letters in choose level smaller. Make capital letters possible
                            0, 80,
                            16, 16)
            pyxel.blt(x, y,
                        img,
                        sprite_x, sprite_y,
                        16, 16,
                        0)
            
        for order_in_sequence, i in enumerate(range(47, 95, 2)):
            img = 0
            letter = key_name = self.letter_order[i]
            # key_name = self.letter_order[letter]
            # print(key_name)
            if ord(key_name) not in list(range(1072, 1104)) + [1105] + list(range(1040, 1072)) + [203]:
                key_name = f"{key_name}_sequence"
                img = 1
            if "sequence" not in key_name and ord(key_name) in list(range(1040, 1072)) + [203]:
                key_name = key_name.lower()
                img = 1
            key = self.key_positions[key_name]
            # offset = 13 * 16 if self.level_type == "showcase" else 0
            x = 16 + 16 * order_in_sequence # self.screen_x - 16 * (i+1)
            y = self.ground_level - 16
            sprite_x, sprite_y = key["sprite_pos"]["None"]
            sprite_width, sprite_height = key["size"]
            background_colour = key["background"]
            if i < self.level * 2 + 3:
                pyxel.blt(x, y,
                            0,
                            152, 80,
                            16, 16)
            else:
                pyxel.blt(x, y,
                            0,
                            0, 80,
                            16, 16)
            pyxel.blt(x, y,
                        img,
                        sprite_x, sprite_y,
                        16, 16,
                        0)
        for order_in_sequence, i in enumerate(range(48, 95, 2)):
            img = 0
            letter = key_name = self.letter_order[i]
            # key_name = self.letter_order[letter]
            # print(key_name)
            if ord(key_name) not in list(range(1072, 1104)) + [1105] + list(range(1040, 1072)) + [203]:
                key_name = f"{key_name}_sequence"
                img = 1
            if "sequence" not in key_name and ord(key_name) in list(range(1040, 1072)) + [203]:
                key_name = key_name.lower()
                img = 1
            key = self.key_positions[key_name]
            # offset = 13 * 16 if self.level_type == "showcase" else 0
            x = 16 + 16 * order_in_sequence # self.screen_x - 16 * (i+1)
            y = self.ground_level
            sprite_x, sprite_y = key["sprite_pos"]["None"]
            sprite_width, sprite_height = key["size"]
            background_colour = key["background"]
            if i < self.level * 2 + 3:
                pyxel.blt(x, y,
                            0,
                            152, 80,
                            16, 16)
            else:
                pyxel.blt(x, y,
                            0, # TODO: make letters in choose level smaller. Make capital letters possible
                            0, 80,
                            16, 16)
            pyxel.blt(x, y,
                        img,
                        sprite_x, sprite_y,
                        16, 16,
                        0)
            
    
    def draw_instructions(self):
        pyxel.text(48, 4, f"Press the keys in the order that they appear on the screen.", 7)
        self.draw_key("del", function="None", x=38, y=12)
        pyxel.text(48, 18, f"Press the        key at any point to return to the menu or cancel choosing a level.", 7)
        self.draw_key("tab", function="None", x=38, y=32)
        pyxel.text(48, 38, f"Press the        key at any point to cycle through keyboard display hints.", 7)
        # self.draw_key("esc", function="None", x=38, y=52)
        pyxel.text(48, 58, f"Press the ESC key at any point to exit the game.", 7)
        pyxel.text(48, 72, f"In the game and in this menu, you can move the bird using the arrowkeys for fun :)", 7)
                

    def draw(self):
        pyxel.cls(6)
        self.draw_floor()
        self.draw_keyboard()
        if self.game_state == "game":
            self.draw_game()
        elif self.game_state == "menu":
            self.draw_menu(self.menu_choice)
            pyxel.text(4, 4, f"{self.game_state}", 7)
            pyxel.text(4, 12, f"level {self.level + 1}", 7)
        elif self.game_state == "choose_level":
            pyxel.text(4, 4, f"{self.game_state}", 7)
            pyxel.text(4, 12, f"level {self.level + 1}", 7)
            self.draw_choose_level()
        elif self.game_state == "instructions":
            self.draw_instructions()
            
        self.draw_player()

App()