#print('Helloworld');

# Hey Surabhi
# It's the 6th of February 2020

# Just go over the report again and finish up the first task !

# link: https://github.com/chia56028/Color-Transfer-between-Images/blob/master/color_transfer.py

import numpy as np
import cv2
import os



def go_through_file_list():
    source_image_list = []
    target_image_list = []
    for i in range(1,4):
        src_image_name = "src_clip" + str(i)
        source_image_list.append(src_image_name)
        tgt_image_name = "target_clip" + str(i)
        target_image_list.append(tgt_image_name)
    source_image_list = np.array(source_image_list)
    target_image_list = np.array(target_image_list)
    return source_image_list, target_image_list

def read_image_file(source_image_name, target_image_name):
    # Need to convert the colors to grayscale in order to calculate pixel intensity
    # Ignore color space
    source_image = cv2.imread(source_image_name)
    source_image = cv2.cvtColor(source_image,cv2.COLOR_BGR2LAB) #convert to grayscale
    target_image = cv2.imread(target_image_name)
    target_image = cv2.cvtColor(target_image,cv2.COLOR_BGR2LAB) #convert to grayscale

    ghist = cv2.calcHist([source_image], [0], None, [256], [0,256])
    print(np.mean(ghist))

def calculate_mean_std(img):
    ghist = cv2.calcHist([img], [0], None, [256], [0,256])
    print(np.mean(ghist))

def color_transfer():
    source_list, target_list = go_through_file_list()
    for i in range(len(source_list)):
        read_image_file(source_list[i],target_list[i])
        
color_transfer()