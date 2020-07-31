import tensorflow as tf
import numpy as np
from PIL import Image
from osgeo import gdal

model=tf.keras.models.load_model('tf2model4.h5')

year = 2003
file = 2

savepath=str(year)+str(file) 

openpath="data/"
openpath=openpath+str(year)+"01"
openpath=openpath+str(file)
openpath=openpath+".tif"

  
       
print('Opening',openpath)
print('Savepath = ',savepath)

ds = gdal.Open(openpath)
print(ds)
print('Getting band 3')
r=ds.GetRasterBand(3).ReadAsArray()
print('Getting band 2')
g=ds.GetRasterBand(2).ReadAsArray()
print('Getting band 1')
b=ds.GetRasterBand(1).ReadAsArray()

print('generating one image from r,g,b')
img1=np.dstack((r,g,b))
r=""
g=""
b=""
img1 = img1/11.71875
img1 = np.array(img1, dtype=np.uint8)
img1 = np.array(img1, dtype=np.int16)


print('Getting band 7 (IR)')
r=ds.GetRasterBand(7).ReadAsArray()
print('Getting band 5 (IR)')
g=ds.GetRasterBand(5).ReadAsArray()
print('Getting band 4 (IR)')
b=ds.GetRasterBand(4).ReadAsArray()

print('Generating fake coloured image from 3 bands of ir')
ir1=np.dstack((r,g,b))
r=""
g=""
b=""
ir1 = ir1/11.71875
ir1 = np.array(ir1, dtype=np.uint8)
ir1 = np.array(ir1, dtype=np.int16)

openpath="data/"
openpath=openpath+str(year)+"07"
openpath=openpath+str(file)
openpath=openpath+".tif"

  
       
print('Opening',openpath)
print('Savepath = ',savepath)

ds = gdal.Open(openpath)
print(ds)
print('Getting band 3')
r=ds.GetRasterBand(3).ReadAsArray()
print('Getting band 2')
g=ds.GetRasterBand(2).ReadAsArray()
print('Getting band 1')
b=ds.GetRasterBand(1).ReadAsArray()

print('generating one image from r,g,b')
img2=np.dstack((r,g,b))
r=""
g=""
b=""
img2 = img2/11.71875
img2 = np.array(img2, dtype=np.uint8)
img2 = np.array(img2, dtype=np.int16)


print('Getting band 7 (IR)')
r=ds.GetRasterBand(7).ReadAsArray()
print('Getting band 5 (IR)')
g=ds.GetRasterBand(5).ReadAsArray()
print('Getting band 4 (IR)')
b=ds.GetRasterBand(4).ReadAsArray()

print('Generating fake coloured image from 3 bands of ir')
ir2=np.dstack((r,g,b))
r=""
g=""
b=""
ir2 = ir2/11.71875
ir2 = np.array(ir2, dtype=np.uint8)
ir2 = np.array(ir2, dtype=np.int16)


diffrgb=abs(img2-img1)
diffir=abs(ir2-ir1)


i=0
while i < len(diffrgb):
    j=0
    print(i,'/',len(diffrgb))
    while j< len(diffrgb[0]):
        predX=np.zeros((1,100,100,3,2))
        sec=diffrgb[i:i+100,j:j+100]
        predX[0,0:len(sec),0:len(sec[0]),:,0]=sec
        predX[0,0:len(sec),0:len(sec[0]),:,1]=diffir[i:i+100,j:j+100]
        if model.predict(predX)[0][0]>50:
            uptoi=0
            uptoj=0
            if i+100>=len(img1):
                uptoi=len(img1)-1
            else:
                uptoi=i+100
            if j+100>=len(img1[0]):
                uptoj=len(img1[0])-1
            else:
                uptoj=j+100  
            img1[i:uptoi,j]=[255,0,0]
            img1[i:uptoi,uptoj]=[255,0,0]
            img1[i,j:uptoj]=[255,0,0]
            img1[uptoi,j:uptoj]=[255,0,0]
        j+=100
    i+=100
    
rname = 'vistest32.png'    
visImg=Image.fromarray(np.array(img1,np.uint8))
visImg.save(rname)
