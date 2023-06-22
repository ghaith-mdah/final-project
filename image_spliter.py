import cv2
from imutils import contours
import numpy as np
import os
from PIL import Image


def shear_image(img, shear_factor,x):
    # Open the image

    rows, cols, dim = img.shape
    # transformation matrix for Shearing
    # shearing applied to x-axis
    M = np.float32([[1, shear_factor, shear_factor*x ],
                    [0, 1  , 0],
                    [0, 0  , 1]])
    # apply a perspective transformation to the image                
    sheared_img = cv2.warpPerspective(img,M,(int(cols*1.7),int(rows*1.2)))
    return sheared_img
    # disable x & y axis


def compare_images(image1_path, image2_path):
    # Load images
    image1 = cv2.imread(image1_path, cv2.IMREAD_GRAYSCALE)
    image2 = cv2.imread(image2_path, cv2.IMREAD_GRAYSCALE)
    # Initialize SIFT detector
    sift = cv2.SIFT_create()

    # Find keypoints and descriptors for both images
    keypoints1, descriptors1 = sift.detectAndCompute(image1, None)
    keypoints2, descriptors2 = sift.detectAndCompute(image2, None)

    # Create a brute-force matcher
    matcher = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)

    # Match descriptors
    matches = matcher.match(descriptors1, descriptors2)

    # Sort matches by distance
    matches = sorted(matches, key=lambda x: x.distance)

    # Draw top matches (optional)
    # num_matches = 70  # Number of matches to display
    # match_img = cv2.drawMatches(
    #     image1, keypoints1, image2, keypoints2, matches[:num_matches], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
    # )

    # Calculate similarity score
    similarity = len(matches) / min(len(descriptors1), len(descriptors2))

    # Display results
    # match_img=cv2.resize(match_img,dsize=(600,600))
    # cv2.imshow("Matches", match_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return similarity


def Img_split(filename):
    if filename!=".DS_Store":
        image = cv2.imread(filename)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray,0,255,cv2.THRESH_OTSU + cv2.THRESH_BINARY)[1]


        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        #cnts, _ = contours.sort_contours(cnts, method="left-to-right")
        return len(cnts)


def reduce_clarity(image, blur_amount):
    # Apply the blurring filter
    return cv2.blur(image,(blur_amount,blur_amount))

def union(a,b):
    x = min(a[0], b[0])
    y = min(a[1], b[1])
    w = max(a[0]+a[2], b[0]+b[2]) - x
    h = max(a[1]+a[3], b[1]+b[3]) - y
    return (x, y, w, h)


def Image_splite(filename):
    image = cv2.imread(filename)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray=reduce_clarity(gray,5)
    thresh = cv2.threshold(gray,0,255,cv2.THRESH_OTSU + cv2.THRESH_BINARY)[1]

    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    flag=False
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    j=cnts[0]
    cnts, _ = contours.sort_contours(cnts, method="left-to-right")
    ROI_number = 0
    for c in cnts:
        
        area = cv2.contourArea(c)
        if area > 3000 :
            x,y,w,h = cv2.boundingRect(c)
              
            ROI = image[y:y+h, x:x+w]
            ROI = cv2.copyMakeBorder(ROI, 60, 60, 60, 60, cv2.BORDER_CONSTANT)
            #ROI=reduce_clarity(ROI,20)
            ROI = cv2.resize(ROI,dsize=(28,28))
            
            cv2.imwrite('Letters/ROI_{}.png'.format(ROI_number), ROI)
            ROI_number += 1
            j=c
            flag=True
        else:
            x,y,w,h = cv2.boundingRect(c)

            x1,y1,w1,h1=cv2.boundingRect(j)

            x,y,w,h =union([x,y,w,h],[x1,y1,w1,h1])
            ROI = image[y:y+h, x:x+w]
            ROI = cv2.copyMakeBorder(ROI, 60, 60, 60, 60, cv2.BORDER_CONSTANT)
           # ROI=reduce_clarity(ROI,20)
            ROI = cv2.resize(ROI,dsize=(28,28))
            if ROI_number>0:
                cv2.imwrite('Letters/ROI_{}.png'.format(ROI_number-1), ROI)
            else:
                cv2.imwrite('Letters/ROI_{}.png'.format(ROI_number), ROI)
            flag=True



def incomplete(image):
    height, width = image.shape[:2]

    # Create four regions
    region1 = [(0, 0), (width//2, height//2)]               # Top-left region
    region2 = [(width//2, 0), (width, height//2)]           # Top-right region
    region3 = [(0, height//2), (width//2, height)]           # Bottom-left region
    region4 = [(width//2, height//2), (width, height)]       # Bottom-right region
    region5 = [(0, 0), (width, height//2)]   
    region6 = [(0, height//2), (width, height//2)]   
    # Create masks for each region
    mask1 = np.zeros_like(image)
    mask1=255-mask1
    cv2.rectangle(mask1, region1[0], region1[1], (0, 0, 0), -1)

    mask2 = np.zeros_like(image)
    mask2=255-mask2
    cv2.rectangle(mask2, region2[0], region2[1], (0, 0, 0), -1)

    mask3 = np.zeros_like(image)
    mask3=255-mask3
    cv2.rectangle(mask3, region3[0], region3[1], (0, 0, 0), -1)

    mask4 = np.zeros_like(image)
    mask4=255-mask4
    cv2.rectangle(mask4, region4[0], region4[1],(0, 0, 0), -1)


    mask5 = np.zeros_like(image)
    mask5=255-mask5
    cv2.rectangle(mask5, region5[0], region5[1],(0, 0, 0), -1)


    mask6=255-mask5
    



    # Bitwise AND the image with each mask


    result1 = cv2.bitwise_and(image, mask1)
    result2 = cv2.bitwise_and(image, mask2)
    result3 = cv2.bitwise_and(image, mask3)
    result4 = cv2.bitwise_and(image, mask4)
    result5 = cv2.bitwise_and(image, mask5)
    result6 = cv2.bitwise_and(image, mask6)

    return result1,result2,result3,result4,result5,result6

def ImageAVG(path,letter):
    sum=0
    for i in range(3):
        diff=compare_images(path,"All_Letters/"+letter+"/ROI_"+str(i)+".png")
        #print(diff)
        sum+=diff
    avg=sum/3
    print(avg)
    return avg   




def new_Read_Letter(filename):
    arr=[0]*26
    for i in range(6):
        arr[i]=ImageAVG(filename,chr(ord('A')+i))
    return chr(ord('A')+np.argmax(arr)) 

#print(compare_images("Letters/ROI_0.png","Letters/ROI_1.png"))
#print(ImageAVG("Correct_Images/correct_A99_64.png","A"))

# Example usage
# img=shear_image("All_Letters/A/ROI_0.png",0.5)
# cv2.imwrite('output_image.png', img)
def compareimg(image1,image2):

    if image1 is None or image2 is None:
        return False

    image1_gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    image2_gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
        
    diff_image=cv2.subtract(image1_gray, image2_gray)    
    
    num_differing_pixels = cv2.countNonZero(diff_image)

    

    if num_differing_pixels>50:
        return True
    return False    


folder_path = "Correct_Images"

# i=0
# j=0
# # Iterate over all files in the folder
# for filename in os.listdir(folder_path):
#     if(i>100000):
#         break
#     else:    
#         img=cv2.imread(folder_path+"/"+filename)
#         if filename!=".DS_Store":
#             r1,r2,r3,r4,r5,r6=incomplete(img)

#             if compareimg(img,r1):
#                 cv2.imwrite(f'Incomplete/incomplete_{i}.png', r1)
#                 i+=1
#             else: 
#                 j+=1
#                 print(filename)
#             if compareimg(img,r2):   
#                 cv2.imwrite(f'Incomplete/incomplete_{i}.png', r2)
#                 i+=1
#             else: 
#                 j+=1  
#                 print(filename)
#             if compareimg(img,r3):
#                 cv2.imwrite(f'Incomplete/incomplete_{i}.png', r3)
#                 i+=1
#             else: 
#                 j+=1
#                 print(filename)   
#             if compareimg(img,r4):
#                 cv2.imwrite(f'Incomplete/incomplete_{i}.png', r4)
#                 i+=1
#             else:
#                 j+=1
#                 print(filename)   
#             if compareimg(img,r5):
#                 cv2.imwrite(f'Incomplete/incomplete_{i}.png', r5)
#                 i+=1
#             else: 
#                 j+=1
#                 print(filename)   
#             if compareimg(img,r6):
#                 cv2.imwrite(f'Incomplete/incomplete_{i}.png', r6)
#                 i+=1
#             else:
#                 j+=1
#                 print(filename)  


# print(j)


# i=181108
# for filename in os.listdir(folder_path):
#      if filename!=".DS_Store":
#         img=cv2.imread(folder_path+"/"+filename)
#         img1=shear_image(img,0.75,-7)
#         img2=shear_image(img,-0.75,-30)
#         cv2.imwrite(f'Sheared/sheared_{i}.png', img1)
#         i+=1
#         cv2.imwrite(f'Sheared/sheared_{i}.png', img2)
#         i+=1




# print(new_Read_Letter("Letters/ROI_4.png"))