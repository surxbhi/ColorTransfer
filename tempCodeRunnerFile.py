
# number_of_images = 4
# # Go through the image file list
# def go_through_file_list():
#     #initialize array
#     source_image_list = []
#     target_image_list = []
#     for i in range(1,number_of_images):
#         src_image_name = "src_clip" + str(i)
#         source_image_list.append(src_image_name)
#         tgt_image_name = "target_clip" + str(i)
#         target_image_list.append(tgt_image_name)
#     source_image_list = np.array(source_image_list)
#     target_image_list = np.array(target_image_list)
#     #return list of image names
#     return source_image_list, target_image_list


# # Read image file and convert to grayscale
# def read_image_file(source_image_name, target_image_name):
#     # Need to convert the colors to grayscale in order to calculate pixel intensity
#     # Ignore color space
#     source_image = cv2.imread('/Users/sur/OneDrive/OneDrive - Nanyang Technological University/COLLEGE/Y3/Y3S2/FYP/Task 1 : Implement Transfer of Color Statistics/Source/'+source_image_name+'.jpg')
#     #cv2.imshow('image', source_image)
#     source_image = cv2.cvtColor(source_image,cv2.COLOR_BGR2LAB) #convert to grayscale 
#     target_image = cv2.imread('/Users/sur/OneDrive/OneDrive - Nanyang Technological University/COLLEGE/Y3/Y3S2/FYP/Task 1 : Implement Transfer of Color Statistics/Target/'+target_image_name+'.jpg')
#     target_image = cv2.cvtColor(target_image,cv2.COLOR_BGR2LAB) #convert to grayscale
    
#     return source_image, target_image

# def color_transfer_idt(s, t, bins = 300, n_rot = 10, relaxation = 1):
#     n_dimensional = t.shape[1] #height, width, channel Extract width of image

#     #Transpose the array
#     d0 = s.T
#     d1 = t.T

#     for i in range(n_rot):
#         rotation_matrix = sp.stats.special_ortho_group.rvs(n_dimensional).astype(np.float32)

#         #Rotate the samples
#         d0_rotated = np.dot(rotation_matrix,d0)
#         d1_rotated = np.dot(rotation_matrix,d1)
#         d_r = np.empty_like(d0) #purpose

#         #get the marginals,match the marginals and apply transformation
#         for j in range(n_dimensional):
#             #Get the data range
#             low = min(d0_rotated[j].min(), d1_rotated[j].min())
#             high = max(d0_rotated[j].max(), d1_rotated[j].max())

#             #Get the projections onto the new axews which gives the marginals

#             proj0_rotated, edges = np.histogram(d0_rotated[j], bins=bins, range=[low, high])
#             proj1_rotated, _     = np.histogram(d1_rotated[j], bins=bins, range=[low, high])

# def main():
#     source_list, target_list = go_through_file_list()
#     for i in range(len(source_list)):
#         print("Reading image " + source_list[i])
#         source_gray, target_gray = read_image_file(source_list[i],target_list[i])
#         color_transfer_idt(source_gray, target_gray, bins = 300, n_rot = 10, relaxation = 1):

