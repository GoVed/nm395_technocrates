from osgeo import gdal
import numpy as np
import math
from PIL import Image

# # this allows GDAL to throw Python Exceptions
gdal.UseExceptions()

year=2000
while year<2020:
    file=1
    while file<4:
        openpath="data/"+str(year)+"01"+str(file)+".tif"
        savepath=str(year)+str(file)      
           
        print('Opening',openpath)
        print('Savepath = ',savepath)
        ds = gdal.Open(openpath)
        print(ds)
        
        print('Getting band 2 for water')
        w1=ds.GetRasterBand(2).ReadAsArray()
        
        print('Getting band 3 for vegetation')
        r=ds.GetRasterBand(3).ReadAsArray()
        
        print('Getting band 4 (IR)')
        ir1=ds.GetRasterBand(4).ReadAsArray()
        
        
        print('searching area with water')
        w1=w1/ir1
        
        print('searching burned area')
        b1=1/((0.1-r)**2+(0.06-ir1)**2)
        b1[np.isnan(b1)]=0
        b1=b1*255/b1.max()
        
        print('Generating ndvi')
        r[r==0]=0.1
        ir1[ir1==0]=0.1
        diff1=ir1/r
        
        diff1/=(diff1+1)
        diff1*=255
        
        openpath="data/"+str(year)+"07"+str(file)+".tif"     
           
        print('Opening',openpath)

        ds = gdal.Open(openpath)
        print(ds)
        
        
        
        print('Getting band 2 for water')
        w2=ds.GetRasterBand(2).ReadAsArray()
        
        print('Getting band 3')
        r=ds.GetRasterBand(3).ReadAsArray()
        
        print('Getting band 4 (IR)')
        ir2=ds.GetRasterBand(4).ReadAsArray()
        
        
        print('searching area with water')
        w2=w2/ir2
        
        print('searching burned area')
        b2=1/((0.1-r)**2+(0.06-ir2)**2)
        b2[np.isnan(b2)]=0
        b2=b2*255/b2.max()
        
        print('Generating ndvi')
        r[r==0]=0.1
        ir2[ir2==0]=0.1
        diff2=ir2/r
        
        diff2/=(diff2+1)
        diff2*=255
        
        
        print('Calculating difference')
        mean1=np.nanmean(diff1)
        mean2=np.nanmean(diff2)
        
        diff1*=((mean2+mean1)/2)/mean1
        diff2*=((mean2+mean1)/2)/mean2
        
        diff1[np.isnan(diff1)]=0
        diff2[np.isnan(diff2)]=0
        diff1[diff1>255]=255
        diff1[diff1<0]=0
        diff2[diff2>255]=255
        diff2[diff2<0]=0
        
        diff=abs(diff2-diff1)
        
        print('Generating image from ndvi difference, water index')
        for i in range(len(ir1)):
            for j in range(len(ir1[0])):
                if ir2[i][j]<5 or ir1[i][j]<5 or w1[i][j]>0.8 or w2[i][j]>0.8:
                    diff[i][j]=0
                    
        print('Adding burn Index')
        diff+=b1
        diff+=b2
        diff[np.isnan(diff)]=0
        diff[diff>255]=255
        diff[diff<0]=0
        
        diff = np.array(diff, dtype=np.uint8)
        del b1,b2,diff1,diff2,ir1,ir2,r,w1,w2

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
            rname = 'v4img/'+savepath+'_'+str(i)+'.png'
               
            rgbdiff=Image.fromarray(sdiff[i])
            rgbdiff.save(rname)
            
        file+=1
        

    
    year+=1
    
    
    

# year=2017

# file=2
# openpath="data/"+str(year)+"01"+str(file)+".tif"
# savepath=str(year)+"01"+str(file)      
   
# print('Opening',openpath)
# print('Savepath = ',savepath)
# ds = gdal.Open(openpath)
# print(ds)

# print('Getting band 2 for water')
# w1=ds.GetRasterBand(2).ReadAsArray()

# print('Getting band 3 for vegetation')
# r=ds.GetRasterBand(3).ReadAsArray()

# print('Getting band 4 (IR)')
# ir1=ds.GetRasterBand(4).ReadAsArray()


# print('searching area with water')
# w1=w1/ir1

# print('searching burned area')
# b1=1/((0.1-r)**2+(0.06-ir1)**2)
# b1[np.isnan(b1)]=0
# b1=b1*255/b1.max()

# print('Generating ndvi')
# r[r==0]=0.1
# ir1[ir1==0]=0.1
# diff1=ir1/r

# diff1/=(diff1+1)
# diff1*=255

# openpath="data/"+str(year)+"07"+str(file)+".tif"
# savepath=str(year)+"07"+str(file)      
   
# print('Opening',openpath)
# print('Savepath = ',savepath)
# ds = gdal.Open(openpath)
# print(ds)



# print('Getting band 2 for water')
# w2=ds.GetRasterBand(2).ReadAsArray()

# print('Getting band 3')
# r=ds.GetRasterBand(3).ReadAsArray()

# print('Getting band 4 (IR)')
# ir2=ds.GetRasterBand(4).ReadAsArray()


# print('searching area with water')
# w2=w2/ir2

# print('searching burned area')
# b2=1/((0.1-r)**2+(0.06-ir2)**2)
# b2[np.isnan(b2)]=0
# b2=b2*255/b2.max()

# print('Generating ndvi')
# r[r==0]=0.1
# ir2[ir2==0]=0.1
# diff2=ir2/r

# diff2/=(diff2+1)
# diff2*=255


# print('Calculating difference')
# mean1=np.nanmean(diff1)
# mean2=np.nanmean(diff2)

# diff1*=((mean2+mean1)/2)/mean1
# diff2*=((mean2+mean1)/2)/mean2

# diff1[np.isnan(diff1)]=0
# diff2[np.isnan(diff2)]=0
# diff1[diff1>255]=255
# diff1[diff1<0]=0
# diff2[diff2>255]=255
# diff2[diff2<0]=0

# diff=abs(diff2-diff1)

# print('Generating image from ndvi difference, water index')
# for i in range(len(ir1)):
#     for j in range(len(ir1[0])):
#         if ir2[i][j]<5 or ir1[i][j]<5 or w1[i][j]>0.8 or w2[i][j]>0.8:
#             diff[i][j]=0
            
# print('Adding burn Index')
# diff+=b1
# diff+=b2
# diff[np.isnan(diff)]=0
# diff[diff>255]=255
# diff[diff<0]=0

# diff = np.array(diff, dtype=np.uint8)
# del b1,b2,diff1,diff2,ir1,ir2,r,w1,w2
# Image.fromarray(diff).show()
