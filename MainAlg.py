import Alg1
import Alg2
import image_spliter
import random
import os
import cv2


Levels={"Beginner":0,"Intermediate":40,"Advancd":60}

def Empty_Letters():
    for filename in os.listdir("Letters"):
        os.remove("Letters/"+filename)

def extract_sift_features(image,threshold):
    # Create SIFT object
    image = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
    sift = cv2.SIFT_create()

    # Detect keypoints and compute descriptors
    keypoints, descriptors = sift.detectAndCompute(image, None)

    num_keypoints = len(keypoints)
    return num_keypoints>=threshold



min_percentage=[4,3,4,7,4,2,4,4,2,3,4,3,3,2,3,3,6,6,6,4,3,3,3,3,5,3]
def correct_mistake(mistake):
    corrections = {
        'Slant': [
            "Please ensure the letters are properly aligned before shearing.",
            "Try adjusting the shearing angle for better letter preservation.",
            "Make sure the letters are evenly positioned before shearing."
        ],
        'Incomplete': [
            "Check if all the required letter fields have been filled.",
            "Make sure you haven't missed any steps in letter completion.",
            "Try completing the letter again from the beginning."
        ],
        'Incompatable': [
            "Ensure that the letter parts are compatible with each other.",
            "Check if the letter sizes and styles meet the requirements."
        ]
    }
    correction_list = corrections[mistake]
    correction = random.choice(correction_list)
    return correction


# Example usage

def Classify_Algorithm(filname,word,level):
    image_spliter.Image_splite("image.png")
   

    num_letters=len(os.listdir("Letters"))
    response=[]
    if(len(word)>num_letters):
        response.append(f"Please write the full word {num_letters} out of {len(word)}!")
        return response
    for i in range(len(word)):
        ch=''
        path="Letters/ROI_"+str(i)+".png"
        if word[i].islower():
            ch='a'
            letter_from_image,per=Alg1.Read_Letter(path)
            letter_from_image=letter_from_image.lower()
        else:
            ch='A'
            letter_from_image,per=Alg1.Read_Letter(path)

        
        print(letter_from_image)
        print(word[i])
        
        if letter_from_image!=word[i]:
            if word[i]=='e'and (letter_from_image=='C'):
                response.append("try making the circle of the letter e bigger")
            if (word[i]=='m' or word[i]=='M')and letter_from_image=='N':
                response.append("try adjusting the gap size of letter m it seems like you wrote n")
            if (word[i]=='t')and letter_from_image=='L':
                response.append("try making the ascender stroke in letter t bigger")
            if (word[i]=='G')and letter_from_image=='O':
                response.append("try making the gap of the letter G bigger")  
            if (word[i]=='b' or word[i]=='d')and letter_from_image=='O':
                response.append("make the stick bigger")
            if (word[i]=='D')and letter_from_image=='O':
                response.append("try making the letter less round")
            if (word[i]=='V' or word[i]=='v')and letter_from_image=='U':
                response.append("try making the letter more pointy")
            if (word[i]=='K' or word[i]=='k')and letter_from_image=='X':
                response.append("try preventing the lines of the K to not pass the vertical line so it does not look like X")
            if (word[i]=='i')and letter_from_image=='L':
                response.append("Try to make the point further from the line")
            if (word[i]=='q')and letter_from_image=='G':
                response.append("Try to make the stroke at the end of the letter q go more to the right") 
            if (word[i]=='h')and letter_from_image=='N':
                response.append("make the stick bigger") 
            if (word[i]=='R')and letter_from_image=='P':
                response.append("Try to make the stroke at the end of the letter R go more to the right") 
            if (word[i]=='E')and (letter_from_image=='F' or letter_from_image=='T' ):
                response.append("Try to make the three strokes of the letter bigger") 
            if (word[i]=='W' or word[i]=='w')and letter_from_image=='V':
                response.append("try adjusting the gap size of letter W it seems like you wrote V")                 
            if word[i]=='Q'and (letter_from_image=='A'or letter_from_image=='O'):
                if extract_sift_features(path,min_percentage[ord(word[i])-ord(ch)]) and per>Levels[level]:
                    response.append("Good job! No letter mistakes found.")
                
                else:
                    response.append(correct_mistake(Alg2.Classify_Mistake(path)))
            else:
                response.append("you wrote a wrong letter")

        else:
            if extract_sift_features(path,min_percentage[ord(word[i])-ord(ch)]) and per>Levels[level]:
                response.append("Good job! No letter mistakes found.")
                
            else:
                 response.append(correct_mistake(Alg2.Classify_Mistake(path)))
        


           
    return response		 	

#print(correct_mistake(Alg2.Classify_Mistake("Letters/ROI_0.png")))





