# -*- coding: utf-8 -*-


import pygame
import os
import pathlib
import pandas as pd
import numpy as np
import functions
import random
# import pre_test

'''
@@@@@@@@@@@@@@@@@@
GLOBAL VARIABLES
@@@@@@@@@@@@@@@@@@
'''
sigma_values = [1.5,3,4.5,6]  # List of sigma values to test



unique_seed_1 = [380127118, 438462352, 570875540, 79695259, 357337627, 339048478, 3897512, 152833960, 386198835, 426752948, 279855541, 295334325, 188144440, 393153215, 639661761, 854310224, 969697365, 573494491, 206088160, 427832034]
unique_seed_2= [564542017, 708828609, 348283459, 267566244, 16647301, 182719943, 663561545, 736200266, 939097707, 347338382, 714756784, 550250207, 893629044, 994409911, 935484024, 798330489, 928864415, 347338382, 409060100, 658159113, ]
unique_seed_5= [678891659, 101637981, 347338382, 538339265, 731673578, 447369645, 164302326, 610624057, 973130780, 570542700, 956002509, 575387501, 675929460, 953722694, 242808426, 893241675, 764797806, 164302326, 851986172, 851986172,]
unique_seed_6= [372553040, 733117513, 575387501, 16647301,610624057, 731673578, 538339265, 638354634, 956002509, 728976698, 372553040, 733117513, 575387501, 16647301, 610624057, 731673578, 538339265, 638354634, 956002509, 728976698]



unique_seed_1 = [x for x in unique_seed_1 for _ in range(2)]
unique_seed_2 = [x for x in unique_seed_2 for _ in range(2)]
unique_seed_5 = [x for x in unique_seed_5 for _ in range(2)]
unique_seed_6 = [x for x in unique_seed_6 for _ in range(2)]



seed = [unique_seed_1,unique_seed_2,unique_seed_5,unique_seed_6]
dot_radius = 0.30          # Radius of each dot in deg
time_intertrial = 1000 # in msec
display_dist = 60 # distance from the human eye to the stimulus, measured in in cm
frames_per_second = 60 # my monotor
display_width = 54 #cm horizontal size of my ecran (labo HP = 54cm and pc = 32cm)

'''
@@@@@@@@@@@@@@@@@@@@@@@@@
SET UP CANVAS, APERTURE @
@@@@@@@@@@@@@@@@@@@@@@@@@
'''
cwd = os.getcwd()

pygame.init()
monitor = pygame.display.Info() # Set task display to be full screen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('Exp_pf')

x_screen_center = pygame.Rect((0,0),(monitor.current_w, monitor.current_h)).centerx
y_screen_center = pygame.Rect((0,0),(monitor.current_w, monitor.current_h)).centery
pygame.mouse.set_visible(False)

display_resolution = monitor.current_w
# time_stimulus_max = int((((monitor.current_h-(0.04 * monitor.current_h ))/((monitor.current_h-(0.04 * monitor.current_h ))/N))
#                           /frames_per_second)*1000)
dot_radius = functions.visual_degrees_to_pix(display_width, display_resolution, dot_radius, display_dist)
# Set our color constants
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)

n_trials = 5


prop_visibl = 0.70
N = 100
N_visibl = int(N*prop_visibl)

# Define your generate_inclined_line function here
def generate_inclined_line(num_points, start_interval,):
    trajectories = []
    for elem in start_interval:
        start_point = elem
        a = 0
        b = start_point
        x_coordinates = [a * frame + b for frame in range(num_points)]
        trajectories.append(np.array(x_coordinates))
    return np.array(x_coordinates)

def add_noise_to_line(line, sigma, seed):
    seed = seed
    np.random.seed(seed)
    noise = np.random.normal(0, sigma, len(line[:N_visibl]))
    noise = np.hstack([noise, np.ones(N-N_visibl)*0])
    noise[0] = 0
    noise[-1] = 0
    # noise[-1] = 0
    line_noise = line + noise

    # line_noise[0] = line[0]
    line_noise[N_visibl:] = line[N_visibl:]
    return line_noise
'''
@@@@@@@@@@@@@@@@@@@
CLASS DEFINITIONS @
@@@@@@@@@@@@@@@@@@@
'''
class dot(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = pygame.Rect((0,0),(monitor.current_w, monitor.current_h)).centerx     #x coordinate
        self.y = 0                   #y coordinate
        self.y = 0+round((monitor.current_h-(0.07 * monitor.current_h))/N,5)
        # self.y =  round(0.01 * monitor.current_h )                    #y coordinate
        self.dot_radius = dot_radius
        self.image = pygame.Surface([self.dot_radius * 2, self.dot_radius * 2]).convert_alpha()
        self.image.fill(GRAY) # Set the dot to be transparent
        pygame.draw.circle(self.image, WHITE, (self.dot_radius, self.dot_radius), self.dot_radius)
        self.rect = self.image.get_rect(center=(pygame.Rect((0,0),
                                                            (monitor.current_w, monitor.current_h)).centerx,0)) # Rect determines position the dot is drawn
    def update(self,r):
        self.latest_y_move = round((monitor.current_h-(0.02 * monitor.current_h))/N,5)
        self.x = functions.visual_degrees_to_pix(display_width, display_resolution, r, display_dist)+x_screen_center-self.dot_radius
        # print(self.x)
        self.y += self.latest_y_move
        self.rect.x = self.x
        self.rect.y = self.y

class resulaj:
    def __init__(self):

        self.clock = None
        self.start_time = 0
        self.stimulus_start_time = 0
        # trial-specific parameters
        self.intertrial_period_over = False
        self.stimulus_over = False
        self.answer_over = False
        self.stimulus_over_event = pygame.USEREVENT + 1

        # self.direction_changed = False
        self.change_direction = False  # Флаг для изменения направления
        # Initialize variables for the experiment

    # run however many resulaj_trials we want
    def init_slop_param(self):
        self.current_slope = 6  # Define the N value for the 1-up-2-down rule
        self.correct_responses_count = 0
        self.N_down = 2

        self.first_error = True

    def run(self, sigma_values,seed):
        self.target_selected = 0
        self.target = 0


        start = True
        self.start_exp = pygame.time.get_ticks()
        # print(f'start_exp {self.start_exp} ')
        self.intro()
        while start == True:
            self.intro()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        start = False
        self.init_slop_param()
        # for sigma in sigma_values:
        for s in range(len(sigma_values)):
            sigma = sigma_values[s]
            self.seed = seed[s]

            self.init_slop_param()
            self.stop =False
            if (s > 0 ):
                self.stop = True
            while self.stop == True:
                self.pause()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.stop = False
            for k in range(n_trials):
                self.k = k
                # self.current_slope = 10 # Initial slope in visual degrees
                print(f'===============trial {k}========================')

                if k == n_trials//2 :
                    self.init_slop_param()
                    self.current_slope = (self.current_slope)*(-1)
                    self.first_error = True

                self.r_st = generate_inclined_line(num_points=N,start_interval=[self.current_slope])
                # print(f'init {self.r_st}')
                self.r =  add_noise_to_line(self.r_st, sigma=sigma, seed=self.seed[k])
                print(f'noise {sigma}')
                self.end_exp =  pygame.time.get_ticks()
            
            # prepare variables for the trial`
                self.initialize_member_variables()
                self.sprite_group = pygame.sprite.Group()
                new_dot = dot()
                self.sprite_group.add(new_dot)

            # start of the trial demonstration of the fixation cross
                self.fix_start_time = self.current_time()
                
                self.only_fix_phase()

                self.stimulus_start_time = self.current_time()
              
            # print(f'stimulus_start_time :{self.stimulus_start_time} ')
                self.line_transparent = False

                self.count_dot = 0
                while not self.intertrial_period_over:
                    # keep apropriate loop speed
                    self.clock.tick(frames_per_second)    # ms
                    # check for early program termination or if the stimulus should stop due to time limits)
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                pygame.quit()

                    screen.fill(GRAY)  # Update
                    if (not self.intertrial_period_over):
                        # self.info_text(self.current_slope, k)
                        self.target  = self.draw_targets()
                        # self.draw_basket_center(self.current_slope)

                    if self.count_dot < len(self.r)*prop_visibl and not self.stimulus_over:
                        # print(self.count_dot)
                        # self.draw_fix()
                        self.sprite_group.update(self.r[self.count_dot], )
                        self.sprite_group.draw(screen)
                        self.count_dot = self.count_dot + 1
                    elif self.count_dot == int(len(self.r)*prop_visibl): # last visible dot parametres

                        self.last_dot_time = self.current_time() # time last dots
                       

                        self.start_answer =  pygame.time.get_ticks()
                        self.sprite_group.update(self.r[self.count_dot], )
                        # print(self.r[self.count_dot])
                        self.sprite_group.draw(screen)

                        self.count_dot = self.count_dot +1
                        # pygame.time.wait(500)# wait for this period to end
                    elif self.count_dot == int(len(self.r)*prop_visibl)+1 :
                        pygame.display.update()
                        self.answer_over = True
                        self.rest_time = round((N/frames_per_second - (N-(N-int(N*prop_visibl)))/frames_per_second)*1000)
                        # print(f'rest t {self.rest_time}')
                        # self.sprite_group.draw(screen)
                        

                        pygame.time.set_timer(self.stimulus_over_event, self.rest_time)
                        while self.answer_over == True :
                            pygame.display.update()
                            for event in pygame.event.get():
                                if event.type ==  self.stimulus_over_event:
                                    # print( f'line_time {self.ligne_cache_time}')
                                    pygame.time.set_timer(self.stimulus_over_event, 0, True)
                                    self.draw_targets_transparent()
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_LEFT:
                                        self.button_pressed_time = self.current_time()
                                      
                                        self.answer_end_time = pygame.time.get_ticks()-self.start_answer
                                        
                                        self.answer_over = False
                                        self.target_selected =-1                                    
                                        self.intertrial_period()
                                        self.end_trial_time = self.current_time()
                                        
                                        self.intertrial_period_over = True

                                    elif event.key == pygame.K_RIGHT:
                                        self.button_pressed_time = self.current_time()

                                        self.answer_end_time = pygame.time.get_ticks()-self.start_answer
                                        
                                        self.answer_over = False
                                        self.target_selected =1
                                        
                                        self.intertrial_period()
                                        self.end_trial_time = self.current_time()
                                       
                                        self.intertrial_period_over = True
                    pygame.display.update()

                #path info
                print(f"Slope: {self.current_slope}, Response: {self.target_selected}" )
                self.make_step()

    def make_step (self):
        if np.sign(self.target_selected) == np.sign(self.r[-1]) and self.first_error==True: # before first error ok
            if self.current_slope > 0:
                print(f'last {round(self.r[-1],2)}')
                self.current_slope -= 2
            if self.current_slope < 0:
                print(f'last {round(self.r[-1],2)}')
                self.current_slope += 2

        if np.sign(self.target_selected) != np.sign(self.r[-1]) and np.sign(self.r[-1]) != 0: # not ok + first error
            print(f'last {round(self.r[-1],2)}')
            if self.current_slope > 0:
                self.first_error = False
                self.current_slope += 0.5
                self.correct_responses_count = 0
            if self.current_slope < 0:
                self.first_error = False
                self.current_slope -= 0.5
                self.correct_responses_count = 0

        if  np.sign(self.r[-1]) == 0 : # stright line conditions
        # randon choice go to other side or no (0 - no; 1-yes)
            # random.seed(self.k)
            self.go_other_side = random.choice([0,1])
            if self.go_other_side == 0:
                self.first_error = False
                self.current_slope += 1 # stay in current side

                print(f'last {round(self.r[-1],2)} ,{self.go_other_side}')
            elif self.go_other_side ==1:
                # self.direction_changed == True
                self.first_error = False
                self.current_slope -= 1
                print(f'last {round(self.r[-1],2)} , {self.go_other_side}')

        if np.sign(self.target_selected) == np.sign(self.r[-1]) and self.first_error== False:

            self.correct_responses_count += 1
                    # self.current_slope -= 0.5
        if self.correct_responses_count >= self.N_down:

            if self.current_slope > 0:
                print(f'last {round(self.r[-1],2)}')
                self.current_slope -= 0.5
                self.correct_responses_count = 0
            if self.current_slope < 0:
                print(f'last {round(self.r[-1],2)}')
                self.current_slope += 0.5
                self.correct_responses_count = 0

    def render_multiline(self, data):
            tc = []
            for line in data.split("\n"):
                if line != "":
                    text, size, color = line.split(",")
                    size = int(size)
                    tc.append([text, size, color])
            # 2. Each list of the list above is send to write to render text
            for t, s, c in tc:
                for i in t.split("\n"):
                    self.write(i, 200, s, color=c)
                    s += 30
    def write(self, text, x, y, color="Coral"):
        """Returns a surface with a text in the center of the screen, at y coord."""
        Font = pygame.font.SysFont
        font1 = Font("Arial", 40)
        surface_text = font1.render(text, 1, pygame.Color(color))
        text_rect = surface_text.get_rect(center=(x_screen_center, y))
        screen.blit(surface_text, text_rect)
        return surface_text

    def info_text(self, slope,  n_trials):
        text = f'trial {n_trials}; slope {slope} '
        Font = pygame.font.SysFont
        font1 = Font("Arial", 35)
        surface_text = font1.render(text, 1, pygame.Color("Coral"))

        screen.blit(surface_text, dest=(0,0))

    def pause(self):
        text = """Break., 300, white
        Press the SPACEBAR to continue the experiment., 400, white"""
        screen.fill(GRAY)
        # self.blit_text(screen, text, (place), font)
        self.render_multiline(text)
        pygame.display.update()

    def intro(self):         
        TEXT1 = """Welcome to experiment.,  100, white
        You are now in the pre-test phase., 150, white
        After the dot disappears determine as quickly as possible, 250, white  
        from which side the point will cross the blask line relative to its middle., 300, white
        Press the LEFT arrow if the target will cross the LEFT side., 400, white
        Press the RIGHT arrow if the target will cross the RIGHT side., 450, white
        Press the SPACEBAR to start., 550, white
        To exit the experiment press ESCAPE., 600, white"""  
        screen.fill(GRAY) 
        self.render_multiline(TEXT1)
        pygame.display.update()
        
    def draw_basket_center(self, basket_pos, ):
        pos = (functions.visual_degrees_to_pix(display_width, display_resolution, basket_pos, display_dist)+x_screen_center)
        rect_1 = pygame.Rect(0, 0, 5, monitor.current_w)
        rect_1.center = (pos,  y_screen_center)
        pygame.draw.rect(screen,WHITE, rect_1)

    def draw_fix(self):
          fix_color = WHITE
          fix_1 = pygame.Rect(0, 0, 5, 30)
          fix_2 = pygame.Rect(0, 0, 30, 5)
          fix_2.center = (x_screen_center, y_screen_center )
          fix_1.center = fix_2.center
          pygame.draw.rect(screen, fix_color, fix_2)
          pygame.draw.rect(screen, fix_color, fix_1)

    def draw_targets_transparent(self):
        screen.fill(GRAY)
        rect_1 = pygame.Rect(0, 0, 5, 30)
        rect_2 = pygame.Rect(0, 0, monitor.current_w, 5)
        rect_2.center = (x_screen_center,  round((monitor.current_h-(0.02 * monitor.current_h )),3)) #1341+4
        rect_1.center = rect_2.center
        pygame.draw.rect(screen, BLACK, rect_2, 1)
        pygame.draw.rect(screen, BLACK, rect_1, 1)

    def draw_targets(self):
        rect_1 = pygame.Rect(0, 0, 5, 30)
        rect_2 = pygame.Rect(0, 0, monitor.current_w, 5)
        rect_2.center = (x_screen_center,  round((monitor.current_h-(0.02 * monitor.current_h)),3)) #1341+4
        rect_1.center = rect_2.center
        rect_vert = pygame.Rect(0, 0, monitor.current_h, 5)
        rect_vert.center =(x_screen_center,  y_screen_center)

        pygame.draw.rect(screen, BLACK, rect_2)
        pygame.draw.rect(screen, BLACK, rect_1)

    def draw_targets_2(self):
        rect_1 = pygame.Rect(0, 0, 5, 10)
        rect_2 = pygame.Rect(0, 0, monitor.current_h, 5)
        rect_2.center = (x_screen_center,  y_screen_center) #1341+4
        rect_1.center = rect_2.center
        rect_vert = pygame.Rect(0, 0, monitor.current_h, 5)
        rect_vert.center =(x_screen_center,  y_screen_center)
    def only_fix_phase(self):
          screen.fill(GRAY)
          self.draw_fix()
          pygame.display.update()
          pygame.time.wait(300)# wait for this period to end

    def intertrial_period(self):
        screen.fill(GRAY)
        pygame.display.update()
        pygame.time.wait(time_intertrial)

    def cancel_scheduled_events(self):
        pygame.time.set_timer(self.stimulus_over_event, 0)

    def initialize_member_variables(self):
        self.clock = pygame.time.Clock()

        self.stimulus_over = False
        self.answer_over = False
        self.intertrial_period_over = False

        self.stimulus_start_time = 0
        self.stimulus_end_time = 0
        self.answer_end_time = 0
        self.cancel_scheduled_events()# clear the event queue to prepare for the trial
        pygame.event.clear()
        self.start_time = pygame.time.get_ticks() # set the start time in milliseconds

    def current_time(self):
        return pygame.time.get_ticks()-self.start_time
'''
@@@@@@@@@@@@@@@@@@@@@
MAIN IMPLEMENTATION @
@@@@@@@@@@@@@@@@@@@@@
'''
# def main():


#     test_driver = resulaj()
#     test_driver.run(sigma_values,seed)
#     pygame.quit()

# if __name__=='__main__':
#     main()
