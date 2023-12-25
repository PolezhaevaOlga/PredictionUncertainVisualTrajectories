# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 15:25:50 2023

@author: opolezh
"""
import pygame

# import pathlib
import pandas as pd
import numpy as np
import functions
import random
####################### write the path where the files are located ###########################
# path = ""

# path = "C:/Users/opolezh/Desktop/Paris Saclay/Thèse/2_SCRIPT/experiment_150pts"

# stim_csv =  sorted(str(p) for p in pathlib.Path(path).glob("*.csv"))
iid_csv = pd.read_csv('iid_ind.csv', header=None).to_numpy()
rdw_csv = pd.read_csv('rdw_ind.csv', header=None).to_numpy()

# iid_csv= pd.read_csv(stim_csv[0], header=None).to_numpy()
# rdw_csv = pd.read_csv(stim_csv[1], header=None).to_numpy()

stim_array = np.hstack([rdw_csv[:, np.random.RandomState(seed=40).permutation(rdw_csv.shape[1])][:,0:5],
                        iid_csv[:, np.random.RandomState(seed=40).permutation(iid_csv.shape[1])][:,0:5]])

'''
@@@@@@@@@@@@@@@@@@
GLOBAL VARIABLES
@@@@@@@@@@@@@@@@@@
'''
n_trials = stim_array.shape[1]

dot_radius = 0.30             # Radius of each dot in deg
time_intertrial = 1000 # in msec
display_dist = 34 # distance from the human eye to the stimulus, measured in in cm
frames_per_second = 60 # my monotor
display_width = 34 #cm horizontal size of my ecran (labo HP = 54cm and pc = 32cm)

N = 150 # nomnre of dots total
'''
@@@@@@@@@@@@@@@@@@@@@@@@@
SET UP CANVAS, APERTURE @
@@@@@@@@@@@@@@@@@@@@@@@@@
'''
pygame.init()
monitor = pygame.display.Info() # Set task display to be full screen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('RDM Task')

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
        # self.y =  round(0.01 * monitor.current_h )                    #y coordinate
        self.image = pygame.Surface([dot_radius * 2, dot_radius * 2]).convert_alpha()
        self.image.fill((128, 128, 128)) # Set the dot to be transparent
        pygame.draw.circle(self.image, (255, 255, 255), (dot_radius, dot_radius), dot_radius)
        self.rect = self.image.get_rect(center=(pygame.Rect((0,0),(monitor.current_w, monitor.current_h)).centerx,
                                                0)) # Rect determines position the dot is drawn
    def update(self,r,count_dot):
        self.latest_y_move = round((monitor.current_h-(0.07 * monitor.current_h))/N,5)
        self.x = functions.visual_degrees_to_pix(display_width, display_resolution, r, display_dist)+x_screen_center
        self.y += self.latest_y_move
        self.rect.x = self.x
        self.rect.y = self.y

class resulaj(dot):
    def __init__(self):

        self.clock = None
        self.start_time = 0
        self.stimulus_start_time = 0
        # trial-specific parameters
        self.intertrial_period_over = False
        self.stimulus_over = False
        self.answer_over = False
        self.stimulus_over_event = pygame.USEREVENT + 1

    # run however many resulaj_trials we want
    def run(self):
        start = True
        self.start_exp = pygame.time.get_ticks()
        # print(f'start_exp {self.start_exp} ')
        while start == True:
            self.intro()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        start = False

        for k in range(n_trials):
            self.r = stim_array[3:,k]
            self.f = functions.search_f(stim_array[:,k])
            self.resulaj_trial(k)
            if k == n_trials-1:
            # if  == 50 or trial_num == 100 or trial_num == 150 or trial_num == 200 or trial_num == 250 or trial_num == 300 or trial_num == 350 :
                self.stop = True
            while self.stop == True:
                self.end()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            # self.stop = False
                            pygame.quit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                self.stop = False
    def resulaj_trial(self, trial_num):
        self.stop =False
        print (f'trial num: {trial_num}')
        print(f'f= {self.f}')

        self.target_selected = 0
        self.target = 0
        # prepare variables for the trial`
        self.initialize_member_variables()

        self.sprite_group = pygame.sprite.Group()
        new_dot = dot()
        self.sprite_group.add(new_dot)
        # start of the trial demonstration of the fixation cross
        self.only_fix_phase()

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
                self.target  = self.draw_targets()

            if self.count_dot < len(self.r)-(self.f) and not self.stimulus_over:
                self.sprite_group.update(self.r[self.count_dot],self.count_dot)
                self.sprite_group.draw(screen)
                self.count_dot = self.count_dot + 1
            elif self.count_dot == len(self.r)-(self.f): # last visible dot parametres
                self.start_answer =  pygame.time.get_ticks()
                self.sprite_group.update(self.r[self.count_dot],self.count_dot)
                self.sprite_group.draw(screen)

                self.count_dot = self.count_dot + 1

            elif self.count_dot == (len(self.r)-(self.f)+1) :
                pygame.display.update()
                self.answer_over = True
                self.rest_time = round((N/frames_per_second - (N-(self.f))/frames_per_second)*1000)

                pygame.time.set_timer(self.stimulus_over_event, self.rest_time)
                while self.answer_over == True :
                    pygame.display.update()
                    for event in pygame.event.get():
                        if event.type ==  self.stimulus_over_event:
                            self.line_transparent = True
                            self.ligne_cache_time = self.current_time()
                            # print( f'line_time {self.line_time}')
                            pygame.time.set_timer(self.stimulus_over_event, 0, True)
                            self.draw_targets_transparent()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_LEFT:
                                self.answer_over = False
                                self.target_selected =-1
                                self.intertrial_period()
                                self.intertrial_period_over = True

                            elif event.key == pygame.K_RIGHT:
                                self.answer_over = False
                                self.target_selected =1

                                self.intertrial_period()
                                self.intertrial_period_over = True

            pygame.display.update()
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

    def end(self):
        text = """End of the pre-test phase., 300, white
        Press the ESPACEBAR to start the full experiment., 400, white"""
        screen.fill((128, 128, 128))
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

    def draw_fix(self):
          fix_color = (255, 255, 255)
          fix_1 = pygame.Rect(0, 0, 5, 20)
          fix_2 = pygame.Rect(0, 0, 20, 5)
          fix_2.center = (x_screen_center, y_screen_center )
          fix_1.center = fix_2.center
          pygame.draw.rect(screen, fix_color, fix_2)
          pygame.draw.rect(screen, fix_color, fix_1)

    def draw_targets_transparent(self):
        screen.fill(GRAY)
        rect_1 = pygame.Rect(0, 0, 5, 10)
        rect_2 = pygame.Rect(0, 0, monitor.current_w, 5)
        rect_2.center = (x_screen_center,  round((monitor.current_h-(0.04 * monitor.current_h )),3)) #1341+4
        rect_1.center = rect_2.center
        pygame.draw.rect(screen, BLACK, rect_2, 1)
        pygame.draw.rect(screen, BLACK, rect_1, 1)

    def draw_targets(self):
        rect_1 = pygame.Rect(0, 0, 5, 10)
        rect_2 = pygame.Rect(0, 0, monitor.current_w, 5)
        rect_2.center = (x_screen_center,  round((monitor.current_h-(0.04 * monitor.current_h)),3)) #1341+4
        rect_1.center = rect_2.center
        pygame.draw.rect(screen, BLACK, rect_2)
        pygame.draw.rect(screen, BLACK, rect_1)

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
#     test_driver.run()
#     pygame.quit()

# if __name__=='__main__':
#     main()
