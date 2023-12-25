# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 10:16:44 2023

@author: opolezh
"""

import pygame
import os
# import pathlib
import pandas as pd
import numpy as np
import functions
import pre_test
import random
'''
@@@@@@@@@@@@@@@@@@
GLOBAL VARIABLES
@@@@@@@@@@@@@@@@@@
'''
'''
Type of trials organization pause every 50 trials
 1 -  rdw iid rdw iid rdw iid rdw iid
 2 -  iid rdw iid rdw iid rdw iid rdw
 3 - rdw rdw iid iid rdw rdw iid iid
 4 - iid iid rdw rdw iid iid rdw rdw
 5 - rdw rdw rdw rdw  iid iid iid iid
 6 - iid iid iid iid rdw rdw rdw rdw
 7 - rdw iid rdw iid iid rdw iid rdw
 8 - iid rdw iid rdw rdw iid rdw iid
 9 - rdw rdw iid iid rdw iid rdw iid
10 - iid iid rdw rdw iid rdw iid rdw
11 - rdw iid rdw iid rdw rdw iid iid
12 - iid rdw iid rdw rdw iid rdw iid
'''

pre_test_phase = True # If you want to run a pre-test of 10 random trials. If non = False
block_organisation_type = random.randint(1, 13)
print(f'block_organisation_type: {block_organisation_type}')

# path = "C:/Users/opolezh/Desktop/Paris Saclay/Thèse/2_SCRIPT/exp_1"
# stim_csv =  sorted(str(p) for p in pathlib.Path(path).glob("*.csv"))
iid_csv= pd.read_csv('iid_ind.csv', header=None).to_numpy()
rdw_csv = pd.read_csv('rdw_ind.csv', header=None).to_numpy()

dot_radius = 0.27 # Radius of each dot in deg
time_intertrial = 1000 # in msec

display_dist = 35 # distance from the human eye to the stimulus, measured in in cm
frames_per_second = 60 # my monotor
display_width = 34 #cm horizontal size of my screen (labo HP = 54cm and pc = 34 cm)
N = 150 # nomnre of dots total

stim_array = functions.trials_organisarion(iid_csv,rdw_csv, block_organisation_type)
n_trials = stim_array.shape[1]

'''
SET UP CANVAS, APERTURE
'''
cwd = os.getcwd()

pygame.init()
monitor = pygame.display.Info() # Set task display to be full screen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('RDM Task')

x_screen_center = pygame.Rect((0,0),(monitor.current_w, monitor.current_h)).centerx
y_screen_center = pygame.Rect((0,0),(monitor.current_w, monitor.current_h)).centery
pygame.mouse.set_visible(False)

display_resolution = monitor.current_w
dot_radius = functions.visual_degrees_to_pix(display_width, display_resolution, dot_radius, display_dist)
# Set our color constants
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)

'''
CLASS DEFINITIONS
'''
class dot(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.x = pygame.Rect((0,0),(monitor.current_w, monitor.current_h)).centerx     #x coordinate
        self.y = 0                   #y coordinate
        # self.y =  round(0.01 * monitor.current_h )                    #y coordinate
        self.image = pygame.Surface([dot_radius * 2, dot_radius * 2]).convert_alpha()
        self.image.fill(GRAY) # Set the dot to be transparent
        pygame.draw.circle(self.image, WHITE, (dot_radius, dot_radius), dot_radius)
        self.rect = self.image.get_rect(center=(pygame.Rect((0,0),
                    (monitor.current_w, monitor.current_h)).centerx,0)) # Rect determines
    def update(self,r,count_dot):
        self.latest_y_move = round((monitor.current_h-(0.07 * monitor.current_h))/N,5)
        self.x = functions.visual_degrees_to_pix(display_width, display_resolution, r, display_dist)+x_screen_center
        self.y += self.latest_y_move
        self.rect.x = self.x
        self.rect.y = self.y

class resulaj(dot):
    def __init__(self):
        self.directory_name = ""
        self.make_data_dir()
        self.clock = None
        self.start_time = 0
        self.stimulus_start_time = 0
        # trial-specific parameters
        self.intertrial_period_over = False
        self.stimulus_over = False
        self.answer_over = False
        self.stimulus_over_event = pygame.USEREVENT + 1
    def make_data_dir(self):
        experiment_num = 0
        # create parent "data" directory, if needed
        if not os.path.exists(cwd + "/data"):
            os.mkdir(cwd + "/data")
        while os.path.exists(cwd + "/data/experiment_" + str(experiment_num)):
            experiment_num += 1
        self.directory_name = cwd + "/data/experiment_" + str(experiment_num)
        os.mkdir(self.directory_name)
    # run however many resulaj_trials we want
    def run(self):
        # data collection parameters
        self.filename = "exp"+".csv"
        self.trial_dict = {}

        self.num_trial = []
        self.path_trial =[]
        self.index_traj =[]
        self.mean_side_trial = []

        self.f_trial = []
        self.mean_val = []
        self.sd_trial = []
        self.to_be_pred_side = []
        self.to_be_pred_abs_d = []
        self.response = []
        self.dot_mvt_start_time = []
        self.fix_start_time_trial =[]
        self.last_dot_time_trial = []
        self.button_pressed_time_trial =[]
        self.rt = []
        self.end_trial_time_trial = []
        self.start_exp_total = []
        self.end_exp_total = []
        self.line_time = []
        self.early_response_trial = []
        self.rest_time_trial =[]
        self.last_visivl_time_trial = []

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
            self.num_trial.append(k)
            self.index_traj.append(int(stim_array[0,k]))
            if stim_array[1,k] == 1 :
                self.path_trial.append('rdw')
            else:
                self.path_trial.append('iid')
            if np.mean(stim_array[3:,k]) <=0 :
                self.mean_side_trial.append('left')
            else:
                self.mean_side_trial.append('right')

            self.r = stim_array[3:,k]
            self.f = functions.search_f(stim_array[:,k])

            if stim_array[-self.f,k] <= 0:
                self.to_be_pred_side.append('left')
            else:
                self.to_be_pred_side.append('right')
            self.f_trial.append(self.f)
            self.mean_val.append(round(np.mean(stim_array[3:-self.f,k]),3))
            self.sd_trial.append(round(np.std(stim_array[3:-self.f, k]),3))
            self.to_be_pred_abs_d.append(round(stim_array[-(self.f),k],3))

            self.end_exp =  pygame.time.get_ticks()
            self.end_exp_total.append(self.end_exp/1000)

            if k == 0 :
                self.start_exp_total.append(self.start_exp)
            else :
                self.start_exp_total.append(np.nan)

            self.resulaj_trial(k)

    def resulaj_trial(self, trial_num):
        self.stop =False
        print (f'trial num: {trial_num}')
        print(f'f= {self.f}')
        if (trial_num > 0 and trial_num % 50 == 0 ):
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
        self.target_selected = 0
        self.target = 0
        # prepare variables for the trial`
        self.initialize_member_variables()
        self.sprite_group = pygame.sprite.Group()
        new_dot = dot()
        self.sprite_group.add(new_dot)
       # start of the trial demonstration of the fixation cross
        self.fix_start_time = self.current_time()
        self.fix_start_time_trial.append(self.fix_start_time)
        self.only_fix_phase()

        self.stimulus_start_time = self.current_time()
        self.dot_mvt_start_time.append(self.stimulus_start_time)
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
                self.last_dot_time = self.current_time() # time last dots
                self.last_dot_time_trial.append(self.last_dot_time)
                self.start_answer =  pygame.time.get_ticks()
                self.sprite_group.update(self.r[self.count_dot],self.count_dot)
                self.sprite_group.draw(screen)
                self.count_dot = self.count_dot + 1

            elif self.count_dot == (len(self.r)-(self.f)+1) :
                pygame.display.update()
                self.answer_over = True
                self.rest_time = round((N/frames_per_second - (N-(self.f))/frames_per_second)*1000)
                self.rest_time_trial.append(self.rest_time)

                pygame.time.set_timer(self.stimulus_over_event, self.rest_time)
                while self.answer_over == True :
                    pygame.display.update()
                    for event in pygame.event.get():
                        if event.type ==  self.stimulus_over_event:
                            self.line_transparent = True
                            self.ligne_cache_time = self.current_time()
                            # print( f'line_time {self.ligne_cache_time}')
                            pygame.time.set_timer(self.stimulus_over_event, 0, True)
                            self.draw_targets_transparent()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_LEFT:
                                self.button_pressed_time = self.current_time()
                                self.button_pressed_time_trial.append(self.button_pressed_time)

                                self.answer_end_time = pygame.time.get_ticks()-self.start_answer
                                self.rt.append(self.answer_end_time)
                                self.answer_over = False
                                self.target_selected =-1
                                self.response.append(self.target_selected)

                                self.intertrial_period()
                                self.end_trial_time = self.current_time()
                                self.end_trial_time_trial.append(self.end_trial_time)
                                self.intertrial_period_over = True

                            elif event.key == pygame.K_RIGHT:
                                self.button_pressed_time = self.current_time()
                                self.button_pressed_time_trial.append(self.button_pressed_time)

                                self.answer_end_time = pygame.time.get_ticks()-self.start_answer
                                self.rt.append(self.answer_end_time)
                                self.answer_over = False
                                self.target_selected =1
                                self.response.append(self.target_selected)

                                self.intertrial_period()
                                self.end_trial_time = self.current_time()
                                self.end_trial_time_trial.append(self.end_trial_time)
                                self.intertrial_period_over = True

                if self.line_transparent == False:
                    self.line_time.append(self.last_dot_time + self.rest_time) #time to cross the point
                    # print(f'line2 : {self.last_dot_time + self.rest_time}')
                    # print(f'line3 : {self.ligne_cache_time}')
                    self.early_response_trial.append(1) # yes
                if self.line_transparent == True:
                    self.early_response_trial.append(0) # no
                    self.line_time.append(int(self.ligne_cache_time))
                    # print(f'line2 : {self.last_dot_time + self.rest_time}')
                    # print(f'line3 : {self.ligne_cache_time}')
            pygame.display.update()

        self.trial_dict['trial'] = self.num_trial
        self.trial_dict['index_traj']=self.index_traj
        self.trial_dict['path'] = self.path_trial
        # trajectory parametres
        self.trial_dict['mean_side'] = self.mean_side_trial
        self.trial_dict['mean_val']=self.mean_val
        self.trial_dict['sd']=self.sd_trial
        self.trial_dict['last_visibl_side']=self.to_be_pred_side
        self.trial_dict['f_missing_pos']=self.f_trial
        self.trial_dict['last_visibl_center_dist[deg]']=self.to_be_pred_abs_d
        self.trial_dict['response']= self.response
        self.trial_dict['RT'] = self.rt
        # time parametres
        self.trial_dict['fix_start_time']=self.fix_start_time_trial
        self.trial_dict['dot_mvt_start_time']=self.dot_mvt_start_time
        self.trial_dict['last_dot_time']=self.last_dot_time_trial
        self.trial_dict['button_pressed_time']=self.button_pressed_time_trial

        self.trial_dict['line_cross_time'] =self.line_time
        self.trial_dict['early_response (t/f)']=self.early_response_trial
        self.trial_dict['rest_time'] =self.rest_time_trial

        self.trial_dict['end_time']=self.end_trial_time_trial
        self.trial_dict['start_exp_time']= self.start_exp_total
        self.trial_dict['time_from_start [ces]']= self.end_exp_total

        self.export_csv(self.trial_dict,self.filename)

    def export_csv(self, result_dict, filename):
        pd.DataFrame(self.trial_dict).to_csv(self.directory_name+ "/"+self.filename, index= False)

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

    def pause(self):
        text = """Break., 300, white
        Press the SPACEBAR to continue the experiment., 400, white"""
        screen.fill(GRAY)
        # self.blit_text(screen, text, (place), font)
        self.render_multiline(text)
        pygame.display.update()

    def intro(self):
        TEXT1 = """After the dot disappears determine as quickly as possible,  100, white
        from which side the point will cross the blask line relative to its middle., 150, white
        Every 50 trials you will be offered a pause., 250, white
        Press the LEFT arrow if the target will cross the LEFT side., 350, white
        Press the RIGHT arrow if the target will cross the RIGHT side., 400, white
        Press the SPACEBAR to start the experiment., 550, white
        To exit the experiment press ESCAPE., 600, white"""
        screen.fill(GRAY)
        self.render_multiline(TEXT1)
        pygame.display.update()

    def draw_fix(self):
          fix_color = WHITE
          fix_1 = pygame.Rect(0, 0, 5, 40)
          fix_2 = pygame.Rect(0, 0, 40, 5)
          fix_2.center = (x_screen_center, y_screen_center )
          fix_1.center = fix_2.center
          pygame.draw.rect(screen, fix_color, fix_2)
          pygame.draw.rect(screen, fix_color, fix_1)

    def draw_targets_transparent(self):
        screen.fill(GRAY)
        rect_1 = pygame.Rect(0, 0, 5, 10)
        rect_2 = pygame.Rect(0, 0, monitor.current_w, 5)
        rect_2.center = (x_screen_center,  round((monitor.current_h-(0.04 * monitor.current_h )),3))
        rect_1.center = rect_2.center
        pygame.draw.rect(screen, BLACK, rect_2, 1)
        pygame.draw.rect(screen, BLACK, rect_1, 1)

    def draw_targets(self):
        rect_1 = pygame.Rect(0, 0, 5, 10)
        rect_2 = pygame.Rect(0, 0, monitor.current_w, 5)
        rect_2.center = (x_screen_center,  round((monitor.current_h-(0.04 * monitor.current_h)),3))
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
MAIN IMPLEMENTATION
'''
def main():
    if pre_test_phase == True:
        pre = pre_test.resulaj()
        pre.run()
    test_driver = resulaj()
    test_driver.run()
    pygame.quit()

if __name__=='__main__':
    main()
