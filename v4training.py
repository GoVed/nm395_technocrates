import numpy as np
from tensorflow import keras
import random



def get_batch():
    year=random.randint(2000,2006)
    if year >= 2003:
        year+=1
    file=random.randint(1,2)
    openpath=str(year)+"071_"
    b=np.load("v4data/"+openpath+"b"+str(file)+".npy")
    d=np.load("v4data/"+openpath+"d"+str(file)+".npy")
    y=np.load("v4data/"+openpath+"o"+str(file)+".npy")
    
    return np.dstack((d.flatten(),b.flatten()))[0,:,:],np.reshape(y,(len(y)*len(y[0]),5))

def get_test_batch():
    year=2003
    file=random.randint(1,2)
    openpath=str(year)+"071_"
    b=np.load("v4data/"+openpath+"b"+str(file)+".npy")
    d=np.load("v4data/"+openpath+"d"+str(file)+".npy")
    y=np.load("v4data/"+openpath+"o"+str(file)+".npy")
    
    return np.dstack((d.flatten(),b.flatten()))[0,:,:],np.reshape(y,(len(y)*len(y[0]),5))

model = keras.models.Sequential()
model.add(keras.layers.Dense(10,input_shape=(2,),activation='relu'))
model.add(keras.layers.Dense(50,activation='relu'))
model.add(keras.layers.Dense(50,activation='relu'))
model.add(keras.layers.Dense(10,activation='relu'))
model.add(keras.layers.Dense(5,activation='sigmoid'))

model.compile(optimizer=keras.optimizers.Adagrad(lr=0.0005),loss=keras.losses.BinaryCrossentropy())

for i in range(5):
    x,y=get_batch()
    model.fit(x,y,epochs=(i*100)+100,shuffle=True,batch_size=50000,initial_epoch=i*100)

# model.save("model0.h5")
print("Saved model to disk")



