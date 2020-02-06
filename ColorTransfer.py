# Task 1 : Transfering color statistics from one image to another
# 
#   @Surabhi Malani
#
# References
# link 1 : https://github.com/chia56028/Color-Transfer-between-Images/blob/master/color_transfer.py
# link 2: https://www.cnblogs.com/likethanlove/p/6003677.html

import numpy as np
import cv2
import os

number_of_images = 4
# Go through the image file list
def go_through_file_list():
    #initialize array
    source_image_list = []
    target_image_list = []
    for i in range(1,number_of_images):
        src_image_name = "src_clip" + str(i)
        source_image_list.append(src_image_name)
        tgt_image_name = "target_clip" + str(i)
        target_image_list.append(tgt_image_name)
    source_image_list = np.array(source_image_list)
    target_image_list = np.array(target_image_list)
    #return list of image names
    return source_image_list, target_image_list

# Read image file and convert to grayscale
def read_image_file(source_image_name, target_image_name):
    # Need to convert the colors to grayscale in order to calculate pixel intensity
    # Ignore color space
    source_image = cv2.imread('/Users/sur/OneDrive/OneDrive - Nanyang Technological University/COLLEGE/Y3/Y3S2/FYP/Task 1 : Implement Transfer of Color Statistics/Source/'+source_image_name+'.jpg')
    #cv2.imshow('image', source_image)
    source_image = cv2.cvtColor(source_image,cv2.COLOR_BGR2LAB) #convert to grayscale 
    target_image = cv2.imread('/Users/sur/OneDrive/OneDrive - Nanyang Technological University/COLLEGE/Y3/Y3S2/FYP/Task 1 : Implement Transfer of Color Statistics/Target/'+target_image_name+'.jpg')
    target_image = cv2.cvtColor(target_image,cv2.COLOR_BGR2LAB) #convert to grayscale
    
    return source_image, target_image

# Calculate mean and standard deviation specific to the channels (R, G, B)
def calculate_mean_std(img, channel):
    img_mean_list = []
    img_std_list = []
    for i in range(channel) :
        ghist = cv2.calcHist(img, [i], None, [256], [0,256]) # histogram
        # First Way
        img_mean = np.mean(img[:,:,i])
        img_mean_list.append(img_mean)
        img_std = np.std(img[:,:,i])
        img_std_list.append(img_std)
        # print("1st way: mean " + str(img_mean) + " std: " + str(img_std))
        #---
        # Second Way
        # x_mean, x_std = cv2.meanStdDev(img)
        # x_mean = np.hstack(np.around(x_mean,2))
        # x_std = np.hstack(np.around(x_std,2))
        # print("2nd way: mean " + str(x_mean) + " std: " + str(x_std))
    img_mean_list = np.array(img_mean_list)
    img_std_list = np.array(img_std_list)

    return img_mean_list, img_std_list

def color_transfer():
    source_list, target_list = go_through_file_list()
    for i in range(len(source_list)):
        print("Reading image " + source_list[i])
        source_gray, target_gray = read_image_file(source_list[i],target_list[i])
        height, width, channel = source_gray.shape

        src_mean, src_sd = calculate_mean_std(source_gray, channel)
        tgt_mean, tgt_sd = calculate_mean_std(target_gray, channel)

        for row in range(height):
            for col in range(width):
                for k in range(0,channel):
                    # Extract pixel information
                    src_point = source_gray[row,col,k]
                    # Subtract mean from data points on the source image
                    src_point = src_point - src_mean[k]
                    # Scale data points by respective standard deviation
                    src_point = src_point * (tgt_sd[k]/src_sd[k])
                    # Add average computed for target image
                    src_point += tgt_mean[k]

                    # necessary rounding
                    src_point = np.round(src_point)
                    # boundary check
                    if src_point<0:
                        src_point = 0
                        
                    if src_point>255:
                        src_point = 255
                    source_gray[row,col,k] = src_point

        # overt image back to color
        new_source = cv2.cvtColor(source_gray,cv2.COLOR_LAB2BGR)
        # Saving image
        print('saving image ' + str(i))
        cv2.imwrite('/Users/sur/OneDrive/OneDrive - Nanyang Technological University/COLLEGE/Y3/Y3S2/FYP/Task 1 : Implement Transfer of Color Statistics/Result/'+'Resule'+str(i)+'.jpg',new_source)
        print('completed saving image ' + str(i))
color_transfer()