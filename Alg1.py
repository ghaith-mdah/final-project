import numpy as np
import math
import tensorflow as tf
from PIL import Image
import cv2
import os
import random
from keras.applications.vgg16 import VGG16, preprocess_input
from keras.preprocessing import image
from scipy.spatial.distance import cosine
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import ReLU
from keras.layers import BatchNormalization
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.optimizers.legacy import Adam
import matplotlib.pyplot as plt
#from extra_keras_datasets import emnist
from keras.utils import np_utils
from image_spliter import reduce_clarity
import image_spliter
from imutils import contours
from sklearn.neighbors import NearestNeighbors
checkpoint_path = "training_1/cp.ckpt"

# def Get_data():
#     (input_train, target_train), (input_test, target_test) = emnist.load_data(type='letters')
    

#     # reshape to be [samples][width][height][channels]
#     input_train = input_train.reshape((input_train.shape[0], 28, 28, 1)).astype('float32')
#     input_test = input_test.reshape((input_test.shape[0], 28, 28, 1)).astype('float32')



#     target_train = np_utils.to_categorical(target_train)
#     target_test = np_utils.to_categorical(target_test)


#     return input_train, target_train, input_test, target_test
   


def complex_model():
    model = Sequential()
    model.add(Conv2D(64, 7, activation=None, padding="same",input_shape=[28, 28, 1]))
    model.add(BatchNormalization(epsilon=1e-05, momentum=0.1))
    model.add(ReLU())
    model.add(MaxPooling2D(2))
    model.add(Conv2D(128, 3, activation=None, padding="same"))
    model.add(BatchNormalization(epsilon=1e-05, momentum=0.1))
    model.add(ReLU())
    model.add(Conv2D(128, 3, activation=None, padding="same"))
    model.add(BatchNormalization(epsilon=1e-05, momentum=0.1))
    model.add(ReLU())
    model.add(MaxPooling2D(2))
    model.add(Conv2D(256, 3, activation=None, padding="same"))
    model.add(BatchNormalization(epsilon=1e-05, momentum=0.1))
    model.add(ReLU())
    model.add(MaxPooling2D(2))
    model.add(Flatten())
    model.add(Dense(256, activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(128, activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(27, activation="softmax"))

    model.compile(loss='categorical_crossentropy', optimizer=Adam(learning_rate=1e-3), metrics=['accuracy'])
    return model




def Read_Letter(filename):
    model=complex_model()
    model.load_weights(checkpoint_path)

    img = cv2.imread(filename)
    if img is not None and len(img.shape) > 0:
        
        img = cv2.resize(img,dsize=(28,28))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #gray = img[:,:,0]
        pred = model.predict(gray.reshape(1,28,28,1))
        print(f"{100*np.max(pred[0])}%")
        return class_names[pred.argmax()-1],100*np.max(pred[0])
    else:
        return "error",-1
    
  
def train_model(NNmodel):
    model = NNmodel()
    model.summary()
    checkpoint_dir = os.path.dirname(checkpoint_path)

# Create a callback that saves the model's weights
    cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1)

# Fit the model
    callbacks_list = [cp_callback]
    history=model.fit(input_train, target_train, validation_data=(input_test, target_test), epochs=10, batch_size=32,callbacks=callbacks_list)
    scores = model.evaluate(input_test, target_test, verbose=0)
    print("CNN Error: %.2f%%" % (100-scores[1]*100))

    return model






def find_wrong_letters(array):
    model=complex_model()
    model.load_weights(checkpoint_path)
    i=0
    j=0
    for img in array:
        img = cv2.resize(img,dsize=(28,28))
        pred = model.predict(img.reshape(1,28,28,1))
        if 100*np.max(pred[0])<95: 
            cv2.imwrite('Wrong_Images/wrong_'+class_names[pred.argmax()-1]+str(int(100*np.max(pred[0])))+'_'+str(i)+'.png', img)
            i+=1
        else:
             cv2.imwrite('Correct_Images/correct_'+class_names[pred.argmax()-1]+str(int(100*np.max(pred[0])))+'_'+str(j)+'.png', img)
             j+=1
           

def ImageDiff(file1,file2):
    image1 = cv2.imread(file1)
    image2 = cv2.imread(file2)

    

    # Convert the images to grayscale
    gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # Flatten the grayscale images
    flattened_image1 = gray_image1.flatten().reshape(1, -1)
    flattened_image2 = gray_image2.flatten().reshape(1, -1)

    # Create a k-NN model
    knn = NearestNeighbors(n_neighbors=1)

    # Fit the model with the first image
    knn.fit(flattened_image1)

    # Find the k nearest neighbors of the second image
    distances, _ = knn.kneighbors(flattened_image2)

    # Calculate the similarity as the inverse of the average distance
    similarity = 1.0 / np.mean(distances)

    return np.mean(distances)

def ImageAVG(path,letter):
    sum=0
    for i in range(3):
        if letter.islower():
            compare_path="All_Letters/"+letter+"s/ROI_"+str(i)+".png"
        else:
            compare_path="All_Letters/"+letter+"/ROI_"+str(i)+".png"
    
        diff=ImageDiff(path,compare_path)
        print(diff)
        sum+=diff
    avg=sum/3
    print(avg)
    return avg    



def BinClassify(path,letter):
        if ImageAVG(path,letter)>=0.3:
            return True
        else:
            return False



def Img_split(filename):
    if filename!="Generated/.DS_Store":
        image = cv2.imread(filename)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray,0,255,cv2.THRESH_OTSU + cv2.THRESH_BINARY)[1]

        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        cnts, _ = contours.sort_contours(cnts, method="left-to-right")
        return len(cnts)

def make_incompatable():

    source_path = "Generated"
    target_path = "Incompatable"
    dirsize=len(os.listdir(target_path))-1
    i=dirsize
    model=complex_model()
    model.load_weights(checkpoint_path)
    for filename in os.listdir(source_path):
         if filename!=".DS_Store" and i<100000 and Img_split(source_path+"/"+filename)==1:
            img=cv2.imread(source_path+"/"+filename)
            img = img[:,:,0]
            img = cv2.resize(img,dsize=(28,28))
            pred = model.predict(img.reshape(1,28,28,1))
            if 100*np.max(pred[0])>50 and 100*np.max(pred[0])<70:
                cv2.imwrite(f"Incompatable/incompatable_{i}.png",img)
                i+=1






#input_train, target_train, input_test, target_test=Get_data()
        
# num_classes = target_test.shape[1]
# print(target_test.shape)    
class_names = np.empty(27, dtype=object) 
for i in range(len(class_names)):#num_classes
    class_names[i]=chr(ord('A')+i)

# # print('Train: X=%s, y=%s' % (input_train.shape, target_train.shape))
# # print('Test: X=%s, y=%s' % (input_test.shape, target_test.shape))





# img=cv2.imread("image.png")
# plt.imshow(rotateImage(img,50))
# plt.show()
# find_wrong_letters(input_train)
#findLR(complex_model)
# for i in range(6):
#     s=Read_Letter("Letters/ROI_"+str(i)+".png")
#     print(s)
#     if ImageAVG("Letters/ROI_0.png",s)>0.5:
#         print(True)
#     else:
#         print(False)
#print(ImageAVG("Letters/ROI_0.png",'A'))
# model=train_model(complex_model)
# result=Read_Letter('Letters/ROI_2.png')
# print(result)



# source_path="Incompatable"
# for filename in os.listdir(source_path):
#     if filename!=".DS_Store":
#         if Img_split(source_path+"/"+filename)>1:
#             os.remove(source_path+"/"+filename)




# makeDataSet()
# i=65000
# for filename in os.listdir("Incompatable"):
#     if i<100000:
#         os.remove(f"Incompatable/incompatable_{i}.png")
#         i+=1
#make_incompatable()



















