# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 15:35:05 2023

@author: opolezh
"""
import pathlib
import pandas as pd
import numpy as np
import random

def trials_organisarion (iid_csv,rdw_csv, trial_type):
    iid_shufl = iid_csv[:, np.random.RandomState(seed=42).permutation(iid_csv.shape[1])]
    rdw_shufl = rdw_csv[:, np.random.RandomState(seed=42).permutation(rdw_csv.shape[1])]
    rdw = [rdw_shufl[:,0:50], rdw_shufl[:,50:100],rdw_shufl[:,100:150],rdw_shufl[:,150:200]]
    iid= [iid_shufl[:,0:50], iid_shufl[:,50:100],iid_shufl[:,100:150],iid_shufl[:,150:200]]
    
    if  trial_type ==1:
        stim_array_1 =  np.hstack([rdw[0],iid[0],rdw[1],iid[1],rdw[2],iid[2],rdw[3],iid[3],])
        return stim_array_1
    elif trial_type == 2 :
        stim_array_2 =  np.hstack([iid[0], rdw[0], iid[1], rdw[1], iid[2], rdw[2], iid[3], rdw[3],])
        return stim_array_2    
    elif trial_type == 3 :
        stim_array_3 =  np.hstack([rdw[0], rdw[0], iid[1], iid[1], rdw[2], rdw[2], iid[3], iid[3],])
        return stim_array_3        
    elif trial_type == 4 :
        stim_array_4 =  np.hstack([iid[0], iid[0], rdw[1], rdw[1], iid[2], iid[2], rdw[3], rdw[3],])
        return stim_array_4 
    elif trial_type == 5 :
        stim_array_5 =  np.hstack([rdw[0], rdw[0], rdw[1], rdw[1],  iid[2], iid[2], iid[3], iid[3],])
        return stim_array_5
    elif trial_type == 6 :
        stim_array_6 =  np.hstack([iid[0], iid[0], iid[1], iid[1], rdw[2], rdw[2], rdw[3], rdw[3],])
        return stim_array_6
    elif trial_type == 7 :
        stim_array_7 =  np.hstack([rdw[0], iid[0], rdw[1], iid[1], iid[2], rdw[2], iid[3], rdw[3],])
        return stim_array_7
    elif trial_type == 8 :
        stim_array_8 =  np.hstack([iid[0], rdw[0], iid[1], rdw[1], rdw[2], iid[2], rdw[3], iid[3],])
        return stim_array_8
    elif trial_type == 9 :
        stim_array_9 =  np.hstack([rdw[0],  rdw[0],  iid[1],  iid[1],  rdw[2],  iid[2],  rdw[3],  iid[3], ])
        return stim_array_9    
    elif trial_type == 10 :
        stim_array_10 =  np.hstack([iid[0], iid[0], rdw[1], rdw[1], iid[2], rdw[2], iid[3], rdw[3],  ])
        return stim_array_10    
    elif trial_type == 11 :
        stim_array_11 =  np.hstack([rdw[0], iid[0], rdw[1], iid[1], rdw[2], rdw[2], iid[3],iid[3],])
        return stim_array_11
    elif trial_type == 12 :
        stim_array_12 =  np.hstack([iid[0], rdw[0], iid[1], rdw[1], rdw[2], iid[2], rdw[3], iid[3],])
        return stim_array_12  
    
def unique_permutations(iterable):
    def permutations(iterable):
        if len(iterable) == 1:
            yield (iterable[0], )
        else:
            for perm in permutations(iterable[1:]):
                for i in range(len(iterable)):
                    yield perm[:i] + (iterable[0], ) + perm[i:]
    return list(set(permutations(iterable)))

# stim_array = pd.read_csv(stim_csv, header=None).to_numpy()

def trials_random_organisation (iid_csv,rdw_csv,): 
    combination_list  = list(map(list, unique_permutations(["rdw","rdw","rdw","rdw","iid","iid","iid","iid",])))
    trial_org = combination_list[np.random.choice(range(len(combination_list)))]
    iid_shufl = iid_csv[:, np.random.RandomState(seed=42).permutation(iid_csv.shape[1])]
    rdw_shufl = rdw_csv[:, np.random.RandomState(seed=42).permutation(rdw_csv.shape[1])]
    rdw_list = [rdw_shufl[:,0:50], rdw_shufl[:,50:100],rdw_shufl[:,100:150],rdw_shufl[:,150:200]]
    iid_list = [iid_shufl[:,0:50], iid_shufl[:,50:100],iid_shufl[:,100:150],iid_shufl[:,150:200]]
    
    stim_list = []
    rdw_count = 0
    iid_count = 0
    for i in range(len(trial_org)): 
        if trial_org[i] == 'rdw':
            stim_list.append(rdw_list[rdw_count])
            rdw_count += 1  
        if trial_org[i] == 'iid':
            stim_list.append(iid_list[iid_count]) 
            iid_count += 1
    stim_array =  np.hstack([stim_list[0],stim_list[1],stim_list[2], stim_list[3],
                             stim_list[4],stim_list[5],stim_list[6],stim_list[7]])
    return stim_array,trial_org

def pixel_to_visual_degrees(display_width, display_resolution, pix, dist_of_eye_to_screen_cm):
    #converts monitor pixels into degrees of visual angle.
    #display_dist (distance from screen (cm))
    #display_width (width of screen (cm))
    #display_resolution (number of pixels of display in horizontal direction)
    #ang (visual angle)
    #Calculate pixel size
    display_dist = dist_of_eye_to_screen_cm
    pixSize = display_width/display_resolution   #cm/pix
    sz = pix*pixSize  # cm (duh)
#     ang = 2*180*math.atan(sz/(2*display_dist))/np.pi
    return np.degrees(2*np.arctan(sz/(2*display_dist)))

def visual_degrees_to_pix(display_width, display_resolution,ang, display_dist):
    #Calculate pixel size        
    pixSize = display_width/display_resolution;   #cm/pix
    sz = 2*display_dist*np.tan(np.pi*ang/(2*180))  #cm
    return round(sz/pixSize,4) 
# def angles_per_second_to_pixels_per_second(SD,display_width, display_resolution, display_dist):
#     return round((SD /frames_per_second) * (visual_degrees_to_pix(display_width, display_resolution,SD, display_dist)/SD),3)
# search the number of visible points
def search_f(path):
    f= int(path[2])
    return f