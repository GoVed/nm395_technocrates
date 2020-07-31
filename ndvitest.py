from osgeo import gdal
import numpy as np
import math
from PIL import Image

# # this allows GDAL to throw Python Exceptions
gdal.UseExceptions()

year=2000
while year<2020:
    month=1
    while month<12:
        file=1
        while file<4:
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
            
            
            
            print('Getting band 3 for water')
            w2=ds.GetRasterBand(2).ReadAsArray()
            
            print('Getting band 3')
            r=ds.GetRasterBand(3).ReadAsArray()
            
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

            
            
            print('Splitting images')
            M=100
            N=100
            sdiff = np.full((math.ceil(diff.shape[0]/M)*math.ceil(diff.shape[1]/N),M,N),0,np.uint8)
            
            i=0
            for x in range(0,diff.shape[0],M):
                for y in range(0,diff.shape[1],N):
                    s = diff[x:x+M,y:y+N]
                    sdiff[i,0:s.shape[0], 0:s.shape[1]]=s
                    
                    i+=1
            
            diff=""
            
            print('Saving images')
            for i in range(len(sdiff)-1):
                rname = 'v3diff/'+savepath+'_'+str(i)+'.png'
                   
                rgbdiff=Image.fromarray(sdiff[i])
                rgbdiff.save(rname)
                
            file+=1
        
        month+=6
    
    year+=1
    
    
    
#DO green/nir for water , water > 1
# year=2001

# month=1

# file=1
# openpath="data/"+str(year)+"01"+str(file)+".tif"
# savepath=str(year)+"01"+str(file)      
   
# print('Opening',openpath)
# print('Savepath = ',savepath)
# ds = gdal.Open(openpath)
# print(ds)

# print('Getting band 3 for water')
# w1=ds.GetRasterBand(2).ReadAsArray()

# print('Getting band 3 for vegetation')
# r=ds.GetRasterBand(3).ReadAsArray()

# print('Getting band 4 (IR)')
# ir=ds.GetRasterBand(4).ReadAsArray()

# print('searching area with water')
# w1=w1/ir

# print('Generating ndvi')
# r[r==0]=0.1
# ir[ir==0]=0.1
# diff1=ir/r

# diff1/=(diff1+1)
# # diff1*=2
# # diff1=diff1**3
# # diff1/=8
# diff1*=255

# openpath="data/"+str(year)+"07"+str(file)+".tif"
# savepath=str(year)+"07"+str(file)      
   
# print('Opening',openpath)
# print('Savepath = ',savepath)
# ds = gdal.Open(openpath)
# print(ds)



# print('Getting band 3 for water')
# w2=ds.GetRasterBand(2).ReadAsArray()

# print('Getting band 3')
# r=ds.GetRasterBand(3).ReadAsArray()

# print('Getting band 4 (IR)')
# iro=ir
# ir=ds.GetRasterBand(4).ReadAsArray()

# print('searching area with water')
# w2=w2/ir

# print('Generating ndvi')
# r[r==0]=0.1
# ir[ir==0]=0.1
# diff2=ir/r

# diff2/=(diff2+1)
# # diff2*=2
# # diff2=diff2**3
# # diff2/=8
# diff2*=255

# mean1=np.nanmean(diff1)
# mean2=np.nanmean(diff2)

# diff1*=((mean2+mean1)/2)/mean1
# diff2*=((mean2+mean1)/2)/mean2

# diff1[diff1>255]=255
# diff1[diff1<0]=0
# diff2[diff2>255]=255
# diff2[diff2<0]=0

# diff=abs(diff2-diff1)
# diffo=diff
# for i in range(len(iro)):
#     for j in range(len(iro[0])):
#         if iro[i][j]<5 or ir [i][j]<5 or w1[i][j]>0.8 or w2[i][j]>0.8:
#             diff[i][j]=0
# diff = np.array(diff, dtype=np.uint8)
# diffo = np.array(diffo, dtype=np.uint8)
# Image.fromarray(diff).show()
