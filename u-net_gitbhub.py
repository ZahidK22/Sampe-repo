import tensorflow as tf
import os
import numpy as np
import sys
import random 

from tqdm import tqdm 

from skimage.io import imread, imshow
from skimage.transform import resize
import matplotlib.pyplot as plt

# Define a random seed - makes sure to get the same results consistently
seed = 42
np.random.seed = seed
IMG_WIDTH = 128
IMG_HEIGHT = 128
IMG_CHANNELS = 3

TRAIN_PATH = 'C:/Users/ecen/Desktop/python_trial/youtube_learning/data-science-bowl-2018/stage1_train/'
TEST_PATH = 'C:/Users/ecen/Desktop/python_trial/youtube_learning/data-science-bowl-2018/stage1_test/'

#next - returns the next item of the iterator (os.walk), where walk 
# want the list of the subfolders so we start from [1] not [0]
train_ids = next(os.walk(TRAIN_PATH))[1]    
test_ids = next(os.walk(TEST_PATH))[1] 
# https://androidkt.com/tensorflow-keras-unet-for-image-image-segmentation/ 

# Read all images and resize
# create an array of same dimension as input images - with all zeros and update with new numbers
X_train = np.zeros((len(train_ids),IMG_HEIGHT,IMG_WIDTH,IMG_CHANNELS), dtype = np.uint8) #uint8 has range till 255 
Y_train = np.zeros((len(train_ids), IMG_HEIGHT, IMG_WIDTH, 1),dtype = np.bool)  #boolean either yes or no that classifies each pixel


print('Resizing training images and masks')
# tqdm shows the progress bar as you loop 
for n,id_ in tqdm(enumerate(train_ids),total = len(train_ids)):
#for n,id_ in enumerate(train_ids):
    path = TRAIN_PATH + id_
    img = imread(path + '/images/' + id_ + '.png')[:,:,:IMG_CHANNELS] # to get (128,128,3)
    img = resize(img, (IMG_HEIGHT,IMG_WIDTH), mode = 'constant', preserve_range = True) #preserves the range of pixel values
    X_train[n] = img #fill empty X_train with values from img

    # Iterating through each image in the mask folder and taking the maximum value at a given pixel (which is the annotated labels)
        # 0 = black, 255 = white
    mask = np.zeros((IMG_HEIGHT,IMG_WIDTH,1), dtype=np.bool)
    for mask_file in next(os.walk(path + '/masks'))[2]: #goes through each image
        eventual_path = path + '/masks/' + mask_file
        mask_ = imread(eventual_path)
        mask_ = np.expand_dims(resize(mask_, (IMG_HEIGHT,IMG_WIDTH),mode = 'constant', 
                    preserve_range = True), axis = -1)
        mask = np.maximum(mask, mask_) #takes the max values where the labels would be higher values
    # Creates a training image where each pixel is either 0 or 1
    Y_train[n] = mask

##################################
# For test images
X_test = np.zeros((len(test_ids), IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS), dtype = np.uint8)
sizes_test = []
print('Resizing test images')
for n,id_ in tqdm(enumerate(test_ids),total=len(test_ids)):
    path = TEST_PATH + id_
    img = imread(path + '/images/'+ id_ + '.png')[:,:,:IMG_CHANNELS]
    sizes_test.append([img.shape[0],img.shape[1]])
    img = resize(img, (IMG_HEIGHT,IMG_WIDTH), mode = 'constant', preserve_range = True)
    X_test[n] = img

print('Done!')

image_x = random.randint(0,len(train_ids))
imshow(X_train[image_x])
plt.show()
imshow(np.squeeze(Y_train[image_x]))
plt.show()



  
# Build U-Net model
#
# Starting weights using kernel initializer - defines initial values 
# he_normal - trincated normal distribution 

# Have to convert the input values to floating values cuz the conv layers
# only take floating points as inputs 
# Input values, at every pixel [0,255] so we divide by 255 to convert to floating point 
# Lambda is the same as regulare python

inputs = tf.keras.layers.Input((IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS))
s = tf.keras.layers.Lambda(lambda x: x / 255)(inputs)
 
c1 = tf.keras.layers.Conv2D(16, (3, 3), activation='relu', kernel_initializer='he_normal',
                            padding='same')(s)
c1 = tf.keras.layers.Dropout(0.1)(c1)
c1 = tf.keras.layers.Conv2D(16, (3, 3), activation='relu', kernel_initializer='he_normal',
                            padding='same')(c1)
p1 = tf.keras.layers.MaxPooling2D((2, 2))(c1)
 
c2 = tf.keras.layers.Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_normal',
                            padding='same')(p1)
c2 = tf.keras.layers.Dropout(0.1)(c2)
c2 = tf.keras.layers.Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_normal',
                            padding='same')(c2)
p2 = tf.keras.layers.MaxPooling2D((2, 2))(c2)
 
c3 = tf.keras.layers.Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_normal',
                            padding='same')(p2)
c3 = tf.keras.layers.Dropout(0.2)(c3)
c3 = tf.keras.layers.Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_normal',
                            padding='same')(c3)
p3 = tf.keras.layers.MaxPooling2D((2, 2))(c3)
 
c4 = tf.keras.layers.Conv2D(128, (3, 3), activation='relu', kernel_initializer='he_normal',
                            padding='same')(p3)
c4 = tf.keras.layers.Dropout(0.2)(c4)
c4 = tf.keras.layers.Conv2D(128, (3, 3), activation='relu', kernel_initializer='he_normal',
                            padding='same')(c4)
p4 = tf.keras.layers.MaxPooling2D(pool_size=(2, 2))(c4)
 
c5 = tf.keras.layers.Conv2D(256, (3, 3), activation='relu', kernel_initializer='he_normal',
                            padding='same')(p4)
c5 = tf.keras.layers.Dropout(0.3)(c5)
c5 = tf.keras.layers.Conv2D(256, (3, 3), activation='relu', kernel_initializer='he_normal',
                            padding='same')(c5)
 
u6 = tf.keras.layers.Conv2DTranspose(128, (2, 2), strides=(2, 2), padding='same')(c5)
u6 = tf.keras.layers.concatenate([u6, c4])
c6 = tf.keras.layers.Conv2D(128, (3, 3), activation='relu', kernel_initializer='he_normal',
                            padding='same')(u6)
c6 = tf.keras.layers.Dropout(0.2)(c6)
c6 = tf.keras.layers.Conv2D(128, (3, 3), activation='relu', kernel_initializer='he_normal',
                            padding='same')(c6)
 
u7 = tf.keras.layers.Conv2DTranspose(64, (2, 2), strides=(2, 2), padding='same')(c6)
u7 = tf.keras.layers.concatenate([u7, c3])
c7 = tf.keras.layers.Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_normal',
                            padding='same')(u7)
c7 = tf.keras.layers.Dropout(0.2)(c7)
c7 = tf.keras.layers.Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_normal',
                            padding='same')(c7)
 
u8 = tf.keras.layers.Conv2DTranspose(32, (2, 2), strides=(2, 2), padding='same')(c7)
u8 = tf.keras.layers.concatenate([u8, c2])
c8 = tf.keras.layers.Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_normal',
                            padding='same')(u8)
c8 = tf.keras.layers.Dropout(0.1)(c8)
c8 = tf.keras.layers.Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_normal',
                            padding='same')(c8)
 
u9 = tf.keras.layers.Conv2DTranspose(16, (2, 2), strides=(2, 2), padding='same')(c8)
u9 = tf.keras.layers.concatenate([u9, c1], axis=3)
c9 = tf.keras.layers.Conv2D(16, (3, 3), activation='relu', kernel_initializer='he_normal',
                            padding='same')(u9)
c9 = tf.keras.layers.Dropout(0.1)(c9)
c9 = tf.keras.layers.Conv2D(16, (3, 3), activation=tf.keras.activations.elu, kernel_initializer='he_normal',
                            padding='same')(c9)
 
outputs = tf.keras.layers.Conv2D(1, (1, 1), activation='sigmoid')(c9)
 
model = tf.keras.Model(inputs=[inputs], outputs=[outputs])
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.summary()

#################################################
#Model Checkpoint - save your model when something happens 
checkpointer = tf.keras.callbacks.ModelCheckpoint('model_for_nuclei.h5',
                                                verbose =1, save_best_only = True)

#Early stopping to check best model, patience will do two more epochs to verify the model 
#TensorBoard is a visualiation tool, log_dir creates a new directory called logs
# In this look at validation loss as a function of epochs
callbacks = [
    tf.keras.callbacks.EarlyStopping(patience =2, monitor = 'val_loss'),
    tf.keras.callbacks.TensorBoard(log_dir = 'logs')
]

results = model.fit(X_train,Y_train,validation_split = 0.1, batch_size = 16, epochs = 25, callbacks=callbacks)

###################
# Every pixel has a probabilistic value

idx = random.randint(0, len(X_train))
    
preds_train = model.predict(X_train[:int(X_train.shape[0]*0.9)],verbose =1)
preds_val = model.predict(X_train[int(X_train.shape[0]*0.9):],verbose =1)
preds_test = model.predict(X_test,verbose=1)

# Making every pixel to be binary 
preds_train_t = (preds_train>0.5).astype(np.uint8)
preds_val_t = (preds_val>0.5).astype(np.uint8)
preds_test_t = (preds_test>0.5).astype(np.uint8)

# Perform a sanity check on some random training samples 
ix = random.randint(0,len(preds_train_t))
imshow(X_train[ix])
plt.show()
imshow(np.squeeze(Y_train[ix]))
plt.show()
imshow(np.squeeze(preds_train_t[ix]))
plt.show()

# Perform a sanity check on some random validation samples
ix = random.randint(0,len(preds_val_t))
imshow(X_train[int(X_train.shape[0]*0.9):][ix])
plt.show()
imshow(np.squeeze(Y_train[int(Y_train.shape[0]*0.9):][ix]))
plt.show()
imshow(np.squeeze(preds_val_t[ix]))
plt.show()
