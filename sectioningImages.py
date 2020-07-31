from osgeo import gdal
import numpy as np
import math
from PIL import Image

# this allows GDAL to throw Python Exceptions
gdal.UseExceptions()

year=2000
while year<2020:
    month=1
    while month<12:
        file=1
        while file<4:
            openpath="data/"
            openpath=openpath+str(year)
            openpath=openpath+"0"+str(month)
            openpath=openpath+str(file)
            openpath=openpath+".tif"
            savepath=str(year)
            savepath=savepath+"0"+str(month)
            savepath=savepath+str(file)            
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
            img=np.dstack((r,g,b))
            r=""
            g=""
            b=""
            img = img/11.71875
            img = np.array(img, dtype=np.uint8)
            
            
            print('Getting band 7 (IR)')
            r=ds.GetRasterBand(7).ReadAsArray()
            print('Getting band 5 (IR)')
            g=ds.GetRasterBand(5).ReadAsArray()
            print('Getting band 4 (IR)')
            b=ds.GetRasterBand(4).ReadAsArray()
            
            print('Generating fake coloured image from 3 bands of ir')
            ir=np.dstack((r,g,b))
            r=""
            g=""
            b=""
            ir = ir/11.71875
            ir = np.array(ir, dtype=np.uint8)
            
            
            
            
            print('Splitting images')
            M=100
            N=100
            simg = np.full((math.ceil(img.shape[0]/M)*math.ceil(img.shape[1]/N),M,N,3),255,np.uint8)
            sir = np.full((math.ceil(ir.shape[0]/M)*math.ceil(ir.shape[1]/N),M,N,3),255,np.uint8)
            i=0
            for x in range(0,img.shape[0],M):
                for y in range(0,img.shape[1],N):
                    s = img[x:x+M,y:y+N]
                    simg[i,0:s.shape[0], 0:s.shape[1]]=s
                    s = ir[x:x+M,y:y+N]
                    sir[i,0:s.shape[0], 0:s.shape[1]]=s
                    i+=1
            
            img=""
            ir=""
            print('Saving images')
            for i in range(len(simg)-1):
                rname = 'rgb/'+savepath+'_'+str(i)+'.png'
                iname = 'ir/'+savepath+'_'+str(i)+'.png'    
                rgbImg=Image.fromarray(simg[i])
                rgbImg.save(rname)
                irImg = Image.fromarray(sir[i])
                irImg.save(iname)
            file+=1
        
        month+=6
    
    year+=1
