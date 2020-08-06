# create a data generator
import keras
import tensorflow as tf
import numpy as np
import pandas as pd
from tensorflow.keras.layers import Conv2D
from keras.preprocessing.image import ImageDataGenerator
from PIL import Image
from PIL import Image
import numpy as np
from skimage import transform
import os
import shutil
from pathlib import Path
from keras.applications.vgg16 import VGG16
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D,GlobalAveragePooling2D, InputLayer
from keras.models import Model
from keras import models
from keras.optimizers import Adam

MODEL_FILE_NAME = 'passport_classification.model'

class Network():
    def __init__(self):
        model = VGG16()
        
        inputs = model.get_layer('block1_conv1').input 
        outputs = model.get_layer('fc2').output
        
        model  = Model(outputs = outputs)
        
        self.model = models.Sequential()
        self.model.add(model)

        self.model.add(Dense(7, activation = 'softmax'))
        
        
def train_test(model, train_generator, validation_generator):
    opt = Adam(lr=0.001)
    model.compile(optimizer=opt, loss=keras.losses.categorical_crossentropy, metrics=['accuracy'])
    early_stopping_callback = EarlyStopping(monitor='val_loss', patience=5)
    checkpoint_callback = ModelCheckpoint("modelNew"+'.h5', monitor='val_loss', verbose=1, save_best_only=True,mode='min')
    model.fit_generator(train_generator, steps_per_epoch=32, epochs = 200, validation_data=validation_generator, validation_steps=8, callbacks=[early_stopping_callback, checkpoint_callback])
    model.save('modelNew.h5')
    
    
def main():
    # prepare an iterators for each dataset
    datagen = ImageDataGenerator()
    train_datagen = ImageDataGenerator(rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        validation_split=0.2) # set validation split

    train_generator = train_datagen.flow_from_directory(
        "train/",
        target_size=(224, 224),
        batch_size=64,
        class_mode='categorical',
        subset='training') # set as training data

    validation_generator = train_datagen.flow_from_directory(
        "train/", # same directory as training data
        target_size=(224, 224),
        batch_size=64,
        class_mode='categorical',
        subset='validation') # set as validation data
    
    
    model = Network()
    train_test(model.model, train_generator, validation_generator)
    
    
    
if __name__ == '__main__':
    main()
    
    
    
    