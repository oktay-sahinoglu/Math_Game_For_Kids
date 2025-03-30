#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame, random

# Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)

class Game(object):
    def __init__(self, bg_image_id):
        # Create new font objects
        self.font = pygame.font.Font(None,80)
        self.question_font = pygame.font.Font("BergenMono-SemiBold.otf",100)
        self.answer_font = pygame.font.Font(None,100)
        # Create a dictionary with keys: num1, num2, result
        # These variables will be used for creating the
        # arithmetic problem
        self.problem = {"num1":0,"num2":0,"result":0}
        self.reset_problem = False
        # some limit definitions about operation
        self.multiplication_num2_space = list(range(2,20))
        self.multiplication_num2_space.pop(self.multiplication_num2_space.index(10))
        self.answer_max_digit = 5
        # layout positions
        self.horizontal_question_posY = 455 - (100 if bg_image_id == 2 else 0)
        self.vertical_question_posY = 375 - (100 if bg_image_id == 2 else 0)
        self.horizontal_answer_posY = 675 - (100 if bg_image_id == 2 else 0)
        self.vertical_answer_posY = 675 - (100 if bg_image_id == 2 else 0)
        self.info_posY = 305 - (100 if bg_image_id == 2 else 0)
        self.space_width = 20
        # load background image
        self.background_image = pygame.image.load("background1.jpg" if bg_image_id == 1 else "background2.png").convert()
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = self.background_image.get_size()
        # load splash images
        self.correct_splash = pygame.image.load("correct_splash.png").convert_alpha()
        self.wrong_splash = pygame.image.load("wrong_splash.png").convert_alpha()
        # load operation position images
        self.horizontal_pos_image = pygame.image.load("position1.png").convert_alpha()
        self.vertical_pos_image = pygame.image.load("position2.png").convert_alpha()
        # load sound images
        self.sound_on_image = pygame.image.load("sound_on.png").convert_alpha()
        self.sound_off_image = pygame.image.load("sound_off.png").convert_alpha()
        # position flag
        self.is_vertical = False
        # sound flag
        self.sound_on = True
        # load sounds effects
        self.correct_sounds = [
            pygame.mixer.Sound("success1.mp3"),
            pygame.mixer.Sound("success2.mp3"),
            pygame.mixer.Sound("success3.mp3")
        ]       
        self.wrong_sounds = [
            pygame.mixer.Sound("fail1.mp3"),
            pygame.mixer.Sound("fail2.mp3"),
            pygame.mixer.Sound("fail3.mp3")
        ]
        # load operator images
        self.operator_images = {
            "addition": pygame.image.load("addition.png").convert_alpha(),
            "subtraction": pygame.image.load("subtraction.png").convert_alpha(),
            "multiplication": pygame.image.load("multiplication.png").convert_alpha(),
            "division": pygame.image.load("division.png").convert_alpha(),
            "equal": pygame.image.load("equal.png").convert_alpha()
        }       
        # load scaled operator images
        self.small_operator_images = {
            "addition": pygame.transform.scale(pygame.image.load("addition.png").convert_alpha(), ((self.operator_images["addition"].get_width() //3)*2, (self.operator_images["addition"].get_height() //3)*2)),
            "subtraction": pygame.transform.scale(pygame.image.load("subtraction.png").convert_alpha(), ((self.operator_images["subtraction"].get_width() //3)*2, (self.operator_images["subtraction"].get_height() //3)*2)),
            "multiplication": pygame.transform.scale(pygame.image.load("multiplication.png").convert_alpha(), ((self.operator_images["multiplication"].get_width() //3)*2, (self.operator_images["multiplication"].get_height() //3)*2)),
            "division": pygame.transform.scale(pygame.image.load("division.png").convert_alpha(), ((self.operator_images["division"].get_width() //3)*2, (self.operator_images["division"].get_height() //3)*2)),
            "equal": pygame.transform.scale(pygame.image.load("equal.png").convert_alpha(), ((self.operator_images["equal"].get_width() //3)*2, (self.operator_images["equal"].get_height() //3)*2))
        }       
        # create operator strings
        self.operator_strings = {
            "addition": "+",
            "subtraction": "-",
            "multiplication": "x",
            "division": "/",
            "equal": "=",
        }       
        # problem type list
        self.problem_type_list = ["addition", "subtraction", "multiplication", "division"]
        # Create a variable that will hold the name of the operation
        self.operation = ""

        # prepare answer part
        self.answer_box = InputBox(10, 10) # position of answer is random 10,10 initially
        self.answer_label = self.answer_font.render("Answer:",True,BLACK)
        horizontal_answer_total_width = self.answer_label.get_width() + self.space_width + (self.answer_box.get_char_width() * self.answer_max_digit)
        self.horizontal_answer_label_posX = (self.SCREEN_WIDTH //2) - (horizontal_answer_total_width //2)
        self.vertical_answer_label_posX = (self.SCREEN_WIDTH // 2) - ((self.answer_box.char_width * self.answer_max_digit) //2) - self.answer_label.get_width() - (3 * self.space_width)

        self.answer_box.set_position(*self.get_answer_box_position())

        self.reset_statistics()
        self.show_correct_splash = False
        self.show_wrong_splash = False
        self.show_statistics = False
    
    def get_answer_box_position(self):
        if self.answer_box.is_vertical:
            return self.get_vertical_answer_box_position()
        else:
            return self.get_horizontal_answer_box_position()
    
    def get_horizontal_answer_box_position(self):
        horizontal_answer_box_posX = self.horizontal_answer_label_posX + self.answer_label.get_width() + self.space_width
        horizontal_answer_box_posY = self.horizontal_answer_posY + (self.answer_label.get_height() //2) - (self.answer_box.char_height //2)
        return (horizontal_answer_box_posX, horizontal_answer_box_posY)

    def get_vertical_answer_box_position(self):
        # we are sure that num1 is larger (and longer) than num2
        # so calculate position according to longer
        num1_str = str(self.problem["num1"])
        vertical_answer_box_posX = (self.SCREEN_WIDTH // 2) - ((self.answer_box.char_width * len(num1_str)) //2) + (self.answer_box.char_width * len(num1_str)) - (self.answer_box.char_width * len(self.answer_box.text))
        vertical_answer_box_posY = self.vertical_answer_posY + (self.answer_label.get_height() //2) - (self.answer_box.char_height //2)
        return (vertical_answer_box_posX, vertical_answer_box_posY)

    def draw_line_round_corners(self, surf, p1, p2, c, w):
        p1v = pygame.math.Vector2(p1)
        p2v = pygame.math.Vector2(p2)
        lv = (p2v - p1v).normalize()
        lnv = pygame.math.Vector2(-lv.y, lv.x) * w // 2
        pts = [p1v + lnv, p2v + lnv, p2v - lnv, p1v - lnv]
        pygame.draw.polygon(surf, c, pts)
        pygame.draw.circle(surf, c, p1, round(w / 2))
        pygame.draw.circle(surf, c, p2, round(w / 2))


    def reset_statistics(self):
        # create/reset the score counter
        self.score = 0
        # create/reset the number of problems
        self.count = 0
        self.set_problem()
        self.info_label1 = self.font.render(f"Question: {self.count+1}",True,BLACK)
        self.info_label2 = self.font.render(f"Score: {self.score}/{self.count}",True,BLACK)
        self.problem_history = []

    def addition(self):
        """ These will set num1,num2,result for addition """
        a = random.randint(100,900)
        b = random.randint(100,900)
        if a > b:
            self.problem["num1"] = a
            self.problem["num2"] = b
        else:
            self.problem["num1"] = b
            self.problem["num2"] = a
        self.problem["result"] = a + b
        self.operation = "addition"

    def subtraction(self):
        """ These will set num1,num2,result for subtraction """
        a = random.randint(100,900)
        b = random.randint(100,900)
        if a > b:
            self.problem["num1"] = a
            self.problem["num2"] = b
            self.problem["result"] = a - b
        else:
            self.problem["num1"] = b
            self.problem["num2"] = a
            self.problem["result"] = b - a
        self.operation = "subtraction"
            

    def multiplication(self):
        """ These will set num1,num2,result for multiplication """
        a = random.randint(2,100)
        b = random.choice(self.multiplication_num2_space)
        if a > b:
            self.problem["num1"] = a
            self.problem["num2"] = b
        else:
            self.problem["num1"] = b
            self.problem["num2"] = a
        self.problem["result"] = a * b
        self.operation = "multiplication"

    def division(self):
        """ These will set num1,num2,result for division """
        divisor = random.randint(2,12)
        dividend = divisor * random.randint(2,12)
        quotient = dividend // divisor
        self.problem["num1"] = dividend
        self.problem["num2"] = divisor
        self.problem["result"] = quotient
        self.operation = "division"

    def check_result(self):
        """ Check the result """
        if self.answer_box.get_text() == str(self.problem["result"]):
            # increase score
            self.score += 1
            self.show_correct_splash = True
            self.problem_history.append(" ".join([str(self.problem["num1"]), self.operator_strings[self.operation], str(self.problem["num2"]), self.operator_strings["equal"], self.answer_box.get_text()]) + "\t\t[Correct]")
            if self.sound_on:
                # Play sound effect
                random.choice(self.correct_sounds).play()
        else:
            self.show_wrong_splash = True
            self.problem_history.append(" ".join([str(self.problem["num1"]), self.operator_strings[self.operation], str(self.problem["num2"]), self.operator_strings["equal"], self.answer_box.get_text()]) + "\t\t[Wrong ]")
            if self.sound_on:       
                # play sound effect
                random.choice(self.wrong_sounds).play()
        # Set reset_problem True so it can go to the
        # next problem
        # we'll use reset_problem in display_frame to wait
        # a second
        self.answer_box.clear_text()
        self.reset_problem = True

    def set_problem(self):
        """ do another problem again """ 
        self.operation = random.choice(self.problem_type_list)
        if self.operation == "addition":
            self.addition()
        elif self.operation == "subtraction":
            self.subtraction()
        elif self.operation == "multiplication":
            self.multiplication()
        elif self.operation == "division":
            self.division()
        self.answer_box.set_position(*self.get_answer_box_position())
        
        

    def process_events(self):
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT: # If user clicked close
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("")
                    print("")
                    print("")
                    if self.count > 0:
                        for p_item in self.problem_history:
                            print(p_item)
                        print("")
                        print(f"Average Score: %{(self.score/self.count)*100}  {self.score}/{self.count}")
                    else:
                        print("No question was answered.")
                    print("")
                    print("")
                    print("")
                    self.reset_statistics()
                elif event.key == pygame.K_RETURN:
                    self.check_result()
                elif event.key == pygame.K_BACKSPACE or event.unicode.isdigit():
                    self.answer_box.handle_event(event)
                elif event.key == pygame.K_s:
                    if pygame.key.get_mods() & pygame.KMOD_CTRL:
                        self.sound_on ^= True
                elif event.key == pygame.K_p:
                    if pygame.key.get_mods() & pygame.KMOD_CTRL:
                        self.is_vertical ^= True
                        self.answer_box.set_is_vertical(self.is_vertical)
                        self.answer_box.set_position(*self.get_answer_box_position())

        return False

    def display_frame(self,screen):
        # Draw the background image
        screen.blit(self.background_image,(0,0))
        if self.sound_on:
            screen.blit(self.sound_on_image,(10,10))
        else:
            screen.blit(self.sound_off_image,(10,10))
            
        # True: call pygame.time.wait()
        time_wait = False

        if not self.is_vertical:
            screen.blit(self.horizontal_pos_image, (self.SCREEN_WIDTH-132, 20))
            # Create labels for the each number
            label_1 = self.question_font.render(str(self.problem["num1"]),True,BLACK)
            label_2 = self.question_font.render(str(self.problem["num2"]),True,BLACK)
            label_3 = self.question_font.render("?",True,BLACK)
            # t_w: total width
            t_w = label_1.get_width() + label_2.get_width() + label_3.get_width() + self.operator_images[self.operation].get_width() + self.operator_images["equal"].get_width() + (4*self.space_width)
            posX = (self.SCREEN_WIDTH // 2) - (t_w // 2)
            screen.blit(label_1,(posX, self.horizontal_question_posY))
            # print the operand into the screen
            posX += label_1.get_width() + self.space_width
            posY = self.horizontal_question_posY + (label_1.get_height() //2) - (self.operator_images[self.operation].get_height() //2)
            screen.blit(self.operator_images[self.operation],(posX,posY))

            posX += self.operator_images[self.operation].get_width() + self.space_width
            screen.blit(label_2,(posX, self.horizontal_question_posY))

            posX += label_2.get_width() + self.space_width
            posY = self.horizontal_question_posY + (label_2.get_height() //2) - (self.operator_images["equal"].get_height() //2)
            screen.blit(self.operator_images["equal"],(posX,posY))

            posX += self.operator_images["equal"].get_width() + self.space_width
            screen.blit(label_3,(posX, self.horizontal_question_posY))

            # display answer part
            screen.blit(self.answer_label,(self.horizontal_answer_label_posX, self.horizontal_answer_posY))
            self.answer_box.draw(screen)
        else:
            screen.blit(self.vertical_pos_image, (self.SCREEN_WIDTH-71, 20))
            # Create labels for the each number
            num1_str = str(self.problem["num1"])
            num2_str = str(self.problem["num2"])
            label_1 = self.question_font.render(num1_str,True,BLACK)
            label_2 = self.question_font.render(num2_str,True,BLACK)
            if self.operation == "division":
                vertical_line_width = 15
                horizontal_line_width = 15
                total_division_width = label_1.get_width() + self.space_width + vertical_line_width + self.space_width + label_2.get_width()
                posX = (self.SCREEN_WIDTH //2) - (total_division_width //2)
                screen.blit(label_1, (posX, self.vertical_question_posY))
                posX += label_1.get_width() + self.space_width
                self.draw_line_round_corners(screen, (posX, self.vertical_question_posY - 10), (posX, self.vertical_question_posY + (2 * label_1.get_height()) + self.space_width), BLACK, vertical_line_width)
                posX += vertical_line_width + (self.space_width //2)
                screen.blit(label_2, (posX, self.vertical_question_posY))
                posX -= vertical_line_width + (self.space_width //2)
                posY = self.vertical_question_posY + label_1.get_height() + self.space_width
                self.draw_line_round_corners(screen, (posX, posY), (posX + vertical_line_width + self.space_width + label_2.get_width() + 10, posY), BLACK, horizontal_line_width)
            else:
                operand_posX = (self.SCREEN_WIDTH // 2) - (label_1.get_width() //2) - self.small_operator_images[self.operation].get_width() - (3 * self.space_width)
                operand_posY = self.vertical_question_posY + label_1.get_height() + label_2.get_height() - self.small_operator_images[self.operation].get_height()
                screen.blit(label_1, ((self.SCREEN_WIDTH // 2) - (label_1.get_width() //2), self.vertical_question_posY))
                screen.blit(label_2, ((self.SCREEN_WIDTH // 2) + (label_1.get_width() //2) - label_2.get_width(), self.vertical_question_posY + label_1.get_height()))
                screen.blit(self.small_operator_images[self.operation], (operand_posX, operand_posY))
                line_posY = operand_posY + self.small_operator_images[self.operation].get_height() + self.space_width
                self.draw_line_round_corners(screen, (operand_posX, line_posY), (self.answer_box.x + (self.answer_box.char_width * len(self.answer_box.text)), line_posY), BLACK, 15)
            # display answer part
            screen.blit(self.answer_label,(self.vertical_answer_label_posX, self.vertical_answer_posY))
            self.answer_box.draw(screen)


        # display the score
        info_total_width = self.info_label1.get_width() + self.info_label2.get_width() + (10 * self.space_width)
        info_posX = (self.SCREEN_WIDTH // 2) - (info_total_width // 2)
        screen.blit(self.info_label1,(info_posX, self.info_posY))
        info_posX += self.info_label1.get_width() + (10 * self.space_width)
        screen.blit(self.info_label2,(info_posX, self.info_posY))

        if self.show_correct_splash:
            screen.blit(self.correct_splash,((self.SCREEN_WIDTH //2) - (self.correct_splash.get_width() //2), (self.SCREEN_HEIGHT //2) - (self.correct_splash.get_height() //2)))
            self.show_correct_splash = False
        if self.show_wrong_splash:
            screen.blit(self.wrong_splash,((self.SCREEN_WIDTH //2) - (self.wrong_splash.get_width() //2), (self.SCREEN_HEIGHT //2) - (self.wrong_splash.get_height() //2)))
            self.show_wrong_splash = False

        # --- Go ahead and update the screen with what we've drawn
        pygame.display.flip()
        # --- This is for the game to wait a few seconds to be able to show
        # --- what we have drawn before it change to another frame
        if self.reset_problem:
            # wait 1.5 second
            pygame.time.wait(1500)
            self.set_problem()
            # Increase count by 1
            self.count += 1
            self.info_label1 = self.font.render(f"Question: {self.count+1}",True,BLACK)
            self.info_label2 = self.font.render(f"Score: {self.score}/{self.count}",True,BLACK)
            self.reset_problem = False
        elif time_wait:
            # wait three seconds
            pygame.time.wait(3000)


class InputBox(object):
    def __init__(self, x, y, text=''):
        self.color = pygame.Color('dodgerblue2')
        self.text = text
        self.font = pygame.font.Font("BergenMono-SemiBold.otf", 100)
        self.txt_surface = self.font.render(text, True, self.color)
        self.x = x
        self.y = y
        self.char_width = self.font.render("0", True, self.color).get_width()
        self.char_height = self.font.render("0", True, self.color).get_height()
        self.is_vertical = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.unicode.isdigit():
                self.text += event.unicode
                if self.is_vertical:
                    self.x -= self.char_width
            elif event.key == pygame.K_BACKSPACE:
                if len(self.text) > 0:
                    self.text = self.text[:-1]
                    if self.is_vertical:
                        self.x += self.char_width
            # Re-render the text.
            self.txt_surface = self.font.render(self.text, True, self.color)

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.x, self.y))

    def get_text(self):
        return self.text
    
    def get_char_width(self):
        return self.char_width
    
    def get_char_height(self):
        return self.char_height
    
    def clear_text(self):
        if self.is_vertical:
            self.x += self.char_width * len(self.text)
        self.text = ''
        self.txt_surface = self.font.render(self.text, True, self.color)

    def set_position(self, x, y):
        self.x = x
        self.y = y
    
    def set_is_vertical(self, value):
        self.is_vertical = value
