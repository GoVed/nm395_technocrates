import numpy as np

from tensorflow import keras

from PIL import Image
import random
import pandas as pd

#id2 is 07 and id1 is 01
def getImg(aid):
    return np.array(Image.open("v3var/"+str(aid)+".png"))

def get_batch(size,withsc):
    allX=np.load("v3varX.npy")
    allY=np.load("v3varY.npy")

    
    y=np.zeros(size)
    features=np.full((size,100,100,1),0,dtype=np.uint8)
    
    randomimg=np.random.choice(range(len(allX)),withsc)
    i=0
    print('Getting batch')
    for each in randomimg:        
        features[i,:,:,0]=getImg(allX[each])
        y[i]=allY[each]
        i+=1
        
    while i<size:
        year=random.randint(2000,2019)
        idp=random.randint(1,3)
        ids=0
        if idp==1 or idp==2:
            ids=random.randint(0,3310)
        else:
            ids=random.randint(0,273)
        
        aid=str(year)+"07"+str(idp)+"_"+str(ids)
        if aid not in allX:
            features[i,:,:,0]=getImg(aid)
            i+=1
        
    
    
    
    return features,y

model = keras.models.Sequential()
model.add(keras.layers.Conv2D(8, (3,3), input_shape=(100,100,1),padding='same'))
model.add(keras.layers.MaxPool2D((2,2),padding='same'))
model.add(keras.layers.Conv2D(5, (3,3),padding='same'))
model.add(keras.layers.MaxPool2D((2,2),padding='same'))

model.add(keras.layers.Flatten())
model.add(keras.layers.Dense(64, activation='relu'))
model.add(keras.layers.Dropout(0.3))
model.add(keras.layers.Dense(1,activation='relu'))

model.compile(optimizer=keras.optimizers.Adagrad(lr=0.0005),loss=keras.losses.mean_squared_error)

for i in range(50):
    x,y=get_batch(500,250)
    model.fit(x,y,epochs=(i*100)+100,shuffle=True,batch_size=5,initial_epoch=i*100)

# model.save("model0.h5")
print("Saved model to disk")



