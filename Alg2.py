from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from tensorflow.keras.optimizers.legacy import Adam
import numpy as np
import cv2
import os
import random
from tensorflow import keras

checkpoint_path="training_4/cp.ckpt"
classes=["Slant","Incompatable","Incomplete"]






def makeDataSet():
    paths=[]
    paths.append("Sheared") 
    paths.append("Incompatable")
    paths.append("Incomplete")
    image_size = (28, 28) 
    images = []
    labels = []
    i=0
    for path in paths:
        for filename in os.listdir(path):
            if filename.endswith('.png') and filename!=".DS_Store":
                classname, index = filename.split('_')
                image_path = os.path.join(path, filename)
                img=cv2.imread(image_path)
                img = img[:,:,0]
                img = cv2.resize(img,dsize=image_size)
                images.append(np.array(img.reshape(28,28,1)))  # Convert image to numpy array before appending
                labels.append(i) 
        i+=1
    combined_data = list(zip(images, labels))
    random.shuffle(combined_data)
    images[:], labels[:] = zip(*combined_data)

    train_ratio = 0.8
    num_train = int(len(images) * train_ratio)

    train_images = np.array(images[:num_train])
    train_labels = np.array(labels[:num_train])
    test_images = np.array(images[num_train:])
    test_labels = np.array(labels[num_train:])


    print(str(len(train_images))+"   "+str(len(test_images)))

    return train_images,train_labels,test_images,test_labels



def AlgModel():
    

    model = Sequential([
        Conv2D(64, (5, 5), input_shape=(28, 28, 1), activation="relu"), 
        MaxPooling2D(pool_size=(2, 2)),
        Dropout(0.25), 
        Conv2D(32, (5, 5), input_shape=(28, 28, 1), activation="relu"),
        MaxPooling2D(pool_size=(2, 2)), 
        Dropout(0.25),
        Flatten(),
        Dense(64, activation='relu'),
        Dropout(0.4),
        Dense(3, activation='softmax'),
    ])

    model.compile(
        optimizer=keras.optimizers.legacy.Adam(learning_rate=0.001),
        loss=keras.losses.SparseCategoricalCrossentropy(),
        metrics=['accuracy']
    )
    return model



def train_model(NNmodel):
    model = NNmodel()
    model.summary()
    checkpoint_dir = os.path.dirname(checkpoint_path)

# Create a callback that saves the model's weights
    cp_callback = keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1)

# Fit the model
    callbacks_list = [cp_callback]
    history=model.fit(train_images, train_labels, validation_data=(test_images, test_labels), epochs=6, batch_size=32,callbacks=callbacks_list)
    scores = model.evaluate(test_images, test_labels, verbose=0)
    print("CNN Error: %.2f%%" % (100-scores[1]*100))

    return model



def Classify_Mistake(filename):
    model=AlgModel()
    model.load_weights(checkpoint_path)

    img = cv2.imread(filename)
    img = cv2.resize(img,dsize=(28,28))
    grey_img = img[:,:,0]
    pred = model.predict(grey_img.reshape(1,28,28,1))
    print(f"{100*np.max(pred[0])}%")
    return classes[pred.argmax()]





# train_images,train_labels,test_images,test_labels=makeDataSet()
# model=train_model(AlgModel)









