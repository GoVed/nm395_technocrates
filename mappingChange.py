import numpy as np
import math
from PIL import Image
from osgeo import gdal

change=np.load("change.npy")

var=[]
i=0
while i<len(change):
    j=0
    a=[]
    while j<len(change[0]):
        m=change[i,j,:].mean()
        x=0
        for k in range(8):
            x+=abs(change[i,j,k]-m)

        a.append(math.sqrt(x/8))
        j+=1
    var.append(a)
    i+=1
var=np.array(var)
var=abs(var-var.mean())
var*=0.5/var.max()



year = 2000
file = 1

openpath="data/"+str(year)+"01"+str(file)+".tif"
ds = gdal.Open(openpath)
print('Getting band 1')
b=ds.GetRasterBand(1).ReadAsArray()

print('Getting band 2')
g=ds.GetRasterBand(2).ReadAsArray()

print('Getting band 3')
r=ds.GetRasterBand(3).ReadAsArray()

img=np.dstack((r/11.71875,g/11.71875,b/11.71875))

del r,g,b

for i in range(len(var)):
    for j in range(len(var[0])):
        opacity = var[i,j]
        if (i*100)+100>=len(img):
            uptoi=len(img)-1
        else:
            uptoi=(i*100)+100
        if (j*100)+100>=len(img[0]):
            uptoj=len(img[0])-1
        else:
            uptoj=(j*100)+100
        img[i*100:uptoi,j*100:uptoj,0] = [[ img[x,y,0]*(1-opacity)+(255*opacity) for y in range(j*100,uptoj)]for x in range(i*100,uptoi) ]
Image.fromarray(np.array(img,dtype=np.uint8)).save("testTS.png")