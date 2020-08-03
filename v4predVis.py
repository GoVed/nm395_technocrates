import tensorflow as tf
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

doPlot=False

year=2000
output=[]
while year<2008:
    month=1
    while month<12:
        idp=1
        ids=1404
        model=tf.keras.models.load_model("v4model0.h5")
        openpath=str(year)+"0"+str(month)+str(idp)+"_"+str(ids)+".png"
        rgb=np.array(Image.open("rgb/"+openpath).convert('RGB'),np.uint8)
        ir=np.array(Image.open("ir/"+openpath).convert('RGB'),np.uint8)
        
        r=rgb[:,:,0]
        ir2=ir[:,:,2]
        swirl2=ir[:,:,0]
        
        print('Replacing nan values with mean')
        r[np.isnan(r)]=np.nanmean(r)
        ir2[np.isnan(ir2)]=np.nanmean(ir2)
        swirl2[np.isnan(swirl2)]=np.nanmean(swirl2)
        
        print('searching burned area')
        b2=(ir2-swirl2)/(ir2+swirl2)
        
        print('Generating ndvi')
        r[r==0]=0.01
        ir2[ir2==0]=0.01
        diff2=(ir2-r)/(ir2+r)
        diff2*=255
        
        print('Getting land from ndvi')
        diff2[diff2>255]=255
        diff2[diff2<0]=0
        
        print('Getting burnt area from burn index')
        b2*=-1
        b2-=0.25
        b2*=340
        b2[b2<0]=0
        b2[b2>255]=255
        
        
        x=np.dstack((diff2.flatten(),b2.flatten()))[0,:,:]
        pred=model.predict(x)
        output.append(np.reshape(pred,(100,100,5)))
        month+=6
    year+=1
  
    
output=np.array(output)
barren=[]
crop=[]
forest=[]
burnt=[]
other=[]
for i in range(len(output)):
    a.append(output[i,:,:,0].mean())
    b.append(output[i,:,:,1].mean())
    c.append(output[i,:,:,2].mean())
    d.append(output[i,:,:,3].mean())
    e.append(output[i,:,:,4].mean())
#Making plot
if doPlot==True  
    plt.plot(a,"red") #barren
    plt.plot(b,"blue") #crop
    plt.plot(c,"green") #forest
    plt.plot(d,"cyan") #burnt
    plt.plot(e,"yellow") #other

#Run single
# month="01"
# idp=1
# ids=0
# model=tf.keras.models.load_model("v4model0.h5")
# openpath=str(year)+str(month)+str(idp)+"_"+str(ids)+".png"
# rgb=np.array(Image.open("rgb/"+openpath).convert('RGB'),np.uint8)
# ir=np.array(Image.open("ir/"+openpath).convert('RGB'),np.uint8)

# r=rgb[:,:,0]
# ir2=ir[:,:,2]
# swirl2=ir[:,:,0]

# print('Replacing nan values with mean')
# r[np.isnan(r)]=np.nanmean(r)
# ir2[np.isnan(ir2)]=np.nanmean(ir2)
# swirl2[np.isnan(swirl2)]=np.nanmean(swirl2)

# print('searching burned area')
# b2=(ir2-swirl2)/(ir2+swirl2)

# print('Generating ndvi')
# r[r==0]=0.01
# ir2[ir2==0]=0.01
# diff2=(ir2-r)/(ir2+r)
# diff2*=255

# print('Getting land from ndvi')
# diff2[diff2>255]=255
# diff2[diff2<0]=0

# print('Getting burnt area from burn index')
# b2*=-1
# b2-=0.25
# b2*=340
# b2[b2<0]=0
# b2[b2>255]=255

# output=np.zeros((100,100,5))
# x=np.dstack((diff2.flatten(),b2.flatten()))[0,:,:]
# pred=model.predict(x)
# output=np.reshape(pred,(100,100,5))
# for i in range(len(b2)):
#     for j in range(len(b2[0])):
#         output[i][j]=model.predict(np.array([[diff2[i][j],b2[i][j]]]))[0]
# Image.fromarray(output[:,:,0]).show()
# Image.fromarray(output[:,:,1]).show()
# Image.fromarray(output[:,:,2]).show()
# Image.fromarray(output[:,:,3]).show()
# Image.fromarray(output[:,:,4]).show()