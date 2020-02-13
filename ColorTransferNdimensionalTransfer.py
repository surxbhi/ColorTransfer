# Task 2 : Reduce the n-dimensional problem to a 1-dimensional problem
# 
#   @Surabhi Malani
#
# References
# link 1 : https://github.com/ptallada/colour_transfer/blob/master/colour_transfer.py
# link 2:  https://github.com/ptallada/colour_transfer/blob/master/colour_transfer.py

import numpy as np
import cv2
import os
import scipy.stats 
import scipy.linalg
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
    source_image = source_image.astype(np.float32)
    target_image = cv2.imread('/Users/sur/OneDrive/OneDrive - Nanyang Technological University/COLLEGE/Y3/Y3S2/FYP/Task 1 : Implement Transfer of Color Statistics/Target/'+target_image_name+'.jpg')
    target_image = target_image.astype(np.float32)
    
    return source_image, target_image


#def pdf_transfer(s, t, bins, n_rot, Rotations, relaxation): #{if defining Rotations}
def pdf_transfer(s, t, bins, n_rot, relaxation):
    n_dimensional = s.shape[1] #height, width, channel Extract width of image
    print(s.shape)
    #Transpose the array
    d0 = s.T
    d1 = t.T
    for i in range(n_rot):
        print("Rotation " + str(i))
        rotation_matrix = scipy.stats.special_ortho_group.rvs(n_dimensional).astype(np.float32)
        #Rotate the samples
        d0_rotated = np.dot(rotation_matrix,d0)
        d1_rotated = np.dot(rotation_matrix,d1)
        d_r = np.empty_like(d0) # purpose ?
        
        # np.empty_like()
        #   > return a new array with same shape and type as given array

        
        # Get the marginals,match the marginals and apply transformation
        for j in range(n_dimensional):
            
            # Get the data range
            low = min(d0_rotated[j].min(), d1_rotated[j].min())
            high = max(d0_rotated[j].max(), d1_rotated[j].max())

            # Get the projections onto the new axes which gives the marginals
            # np.histogram parameters:
            #       if bins is an int == defines number of equal-width bins in given range
            # np.histogram returns: 
            #       1. hist: array
            #               > values of histogram
            #       2. bin_edges: array [return the bin edges]
            #               > e.g [1,2,3,4]: first bin is [1,2) second bin is [2,3) third bin is [3,4]   
             
            proj0_rotated, edges = np.histogram(d0_rotated[j], bins=bins, range=[low, high])
            proj1_rotated, _     = np.histogram(d1_rotated[j], bins=bins, range=[low, high])

            # pdf transfer1D
            # Calculate CDF of rotated projections
            cumulative_proj0_rotated = proj0_rotated.cumsum().astype(np.float32) # ensure format of data type is in np.float32 for consistency
            cumulative_proj1_rotated = proj1_rotated.cumsum().astype(np.float32) # ensure format of data type is in np.float32 for consistency

            # Normalize to sum (cdf) Divide my the maximum value (which is at the end of the array)
            cumulative_proj0_rotated /= cumulative_proj0_rotated[-1]
            cumulative_proj1_rotated /= cumulative_proj1_rotated[-1]

            # Get the 1D transformation
            # numpy.interp
            #   > one dimensional linear interpolation
            #   > cumulative_proj0_rotated : x coordinates at which to evaluate the interpolated values
            #   > cumulative_proj1_rotated : x coordinates of data points that must be increasing
            #   > edges[1:]                : y coordinates of data points. Get from the 1st index onwards which tells the length of the previous bin.
            linearF = np.interp(cumulative_proj0_rotated, cumulative_proj1_rotated, edges[1:])

            # Remap the samples , according to the 1D transformation
            d_r[j] = np.interp(d0_rotated[j], edges[1:], linearF, left = 0, right = bins)
            # numpy.interp
            #   > one dimensional linear interpolation
            #   > d0_rotated[j] : x coordinates at which to evaluate the interpolated values
            #   > edges[1:]     : x coordinates of data points that must be increasing
            #   > f             : y coordinates of data points.
            #   > left = 0      : return f[0]
            #   > right = bins  : return f[300] = f[-1] #last index 

        # Rotate back the samples
        d0 = relaxation * np.linalg.solve(rotation_matrix, (d_r - d0_rotated)) + d0
        
        # np.linalg.solve
        #   > solve a linear matrix equation.
    print("Completed pdf transfer ")
  
    return d0.T
    
def main():
    source_list, target_list = go_through_file_list()
    
    for i in range(len(source_list)):
        print("Reading image " + source_list[i])
        source_gray, target_gray = read_image_file(source_list[i],target_list[i])
        height, width, channel = source_gray.shape
        print(channel)
        df_orig = np.reshape(source_gray, (-1, channel))
        df_target = np.reshape(target_gray, (-1, channel))

        a_orig = df_orig
        a_target = df_target
        print(a_orig.shape)
        a_result = pdf_transfer(a_orig, a_target, bins=300, n_rot=20, relaxation=1)
        im_result = np.reshape(a_result, source_gray.shape)
        # Convert image back to color
        #new_source = cv2.cvtColor(im_result,cv2.COLOR_LAB2BGR)
        # Saving image
        print('saving image ' + str(i))
        cv2.imwrite('/Users/sur/OneDrive/OneDrive - Nanyang Technological University/COLLEGE/Y3/Y3S2/FYP/Task 1 : Implement Transfer of Color Statistics/Result2/'+'Result'+str(i)+'.jpg',im_result)
        print('completed saving image ' + str(i))


main()