import numpy as np
from tensorflow.python.keras import models,layers,losses

from PIL import Image
import random
import pandas as pd

#id2 is 07 and id1 is 01
def getImg(id1="",id2=""):
    img=np.zeros((100,100,3,2),np.uint8)
    
    diffrgb=Image.open("diffrgb/"+str(id2)+"-"+str(id1)+".png").convert('RGB')
    diffir=Image.open("diffir/"+str(id2)+"-"+str(id1)+".png").convert('RGB')
    
    
    img[0:100, 0:100, 0:3 , 0]=diffrgb
    img[0:100, 0:100, 0:3 , 1]=diffir
    return img

def get_batch(size,withsc):
    lables=pd.read_csv("x2.csv")
    lables=lables.to_numpy()
    
    features=np.full((size,100,100,3,2),0,dtype=np.uint8)
    
    randomimg=np.random.choice(range(len(lables)),withsc)
    i=0
    print('Getting batch')
    for each in randomimg:        
        features[i]=getImg(lables[each][0],lables[each][1])
        i+=1
    
    while i<size:
        year=random.randint(2000,2019)
        idp=random.randint(1,3)
        ids=0
        if idp==1 or idp==2:
            ids=random.randint(0,3310)
        else:
            ids=random.randint(0,273)
        aid=str(year)+"01"+str(idp)+"_"+str(ids)
        bid=str(year)+"07"+str(idp)+"_"+str(ids)
        if aid not in features[:,0]:
            features[i]=getImg(aid,bid)
            i+=1
        
    y=np.zeros(size)
    y[:withsc]=np.random.randint(85,100,withsc)
    y[withsc:]=np.random.randint(0,10,size-withsc)
    return features,y

model = models.Sequential()
model.add(layers.Conv3D(8, (3,3,3), input_shape=(100,100,3,2),padding='same'))
model.add(layers.MaxPool3D((4,4,4),padding='same'))
model.add(layers.Conv3D(2, (3,3,3),padding='same'))
model.add(layers.MaxPool3D((2,2,2),padding='same'))
model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dropout(0.3))
model.add(layers.Dense(1,activation='relu'))

model.compile(optimizer="adam",loss=losses.mean_absolute_error)

for i in range(100):
    x,y=get_batch(300,150)
    model.fit(x,y,epochs=(i*100)+100,shuffle=True,batch_size=5,initial_epoch=i*100)

# model.save("model0.h5")
print("Saved model to disk")



