import tensorflow as tf
import numpy as np
from PIL import Image
from osgeo import gdal

model=tf.keras.models.load_model('v3varModel0.h5')

year = 2000
file = 1

openpath="data/"+str(year)+"01"+str(file)+".tif"
savepath=str(year)+"01"+str(file)      
   
print('Opening',openpath)
print('Savepath = ',savepath)
ds = gdal.Open(openpath)
print(ds)

print('Getting band 3 for water')
w1=ds.GetRasterBand(2).ReadAsArray()

print('Getting band 3 for vegetation')
r=ds.GetRasterBand(3).ReadAsArray()

print('Getting band 4 (IR)')
ir=ds.GetRasterBand(4).ReadAsArray()

print('searching area with water')
w1=w1/ir

print('Generating ndvi')
r[r==0]=0.1
ir[ir==0]=0.1
diff1=ir/r

diff1/=(diff1+1)
# diff1*=2
# diff1=diff1**3
# diff1/=8
diff1*=255

openpath="data/"+str(year)+"07"+str(file)+".tif"
savepath=str(year)+"07"+str(file)      
   
print('Opening',openpath)
print('Savepath = ',savepath)
ds = gdal.Open(openpath)
print(ds)

print('Getting band 1 as blue')
b=ds.GetRasterBand(1).ReadAsArray()

print('Getting band 2 for water')
w2=ds.GetRasterBand(2).ReadAsArray()

print('Getting band 3')
r=ds.GetRasterBand(3).ReadAsArray()

img1=np.dstack((r/11.71875,w2/11.71875,b/11.71875))

print('Getting band 4 (IR)')
iro=ir
ir=ds.GetRasterBand(4).ReadAsArray()

print('searching area with water')
w2=w2/ir

print('Generating ndvi')
r[r==0]=0.1
ir[ir==0]=0.1
diff2=ir/r

diff2/=(diff2+1)
# diff2*=2
# diff2=diff2**3
# diff2/=8
diff2*=255

mean1=np.nanmean(diff1)
mean2=np.nanmean(diff2)

diff1*=((mean2+mean1)/2)/mean1
diff2*=((mean2+mean1)/2)/mean2

diff1[diff1>255]=255
diff1[diff1<0]=0
diff2[diff2>255]=255
diff2[diff2<0]=0

diff=abs(diff2-diff1)

for i in range(len(iro)):
    for j in range(len(iro[0])):
        if iro[i][j]<5 or ir [i][j]<5 or w1[i][j]>0.8 or w2[i][j]>0.8:
            diff[i][j]=0
diff = np.array(diff, dtype=np.uint8)


i=0
while i < len(diff):
    j=0
    print(i,'/',len(diff))
    while j< len(diff[0]):
        predX=np.zeros((1,100,100,1))
        sec=diff[i:i+100,j:j+100]
        predX[0,0:len(sec),0:len(sec[0]),0]=sec
        predX=abs(np.array(predX,dtype=np.float64)-predX.mean())
        predicted=model.predict(predX)[:,0]
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
            
        opacity = (0.43*(predicted**2.3))/(7.6**(0.27*(predicted**2)))
        img1[i:uptoi,j:uptoj,0] = [[ img1[x,y,0]*(1-opacity)+(255*opacity) for y in range(j,uptoj)]for x in range(i,uptoi) ]
        
         
            
        j+=100
    i+=100
    
rname = 'v3varVis001.png'    
visImg=Image.fromarray(np.array(img1,np.uint8))
visImg.save(rname)
