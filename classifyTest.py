#ir 111,115,11
#rgb 30,7,5


#ir 146,227,224
#nir 112,200,254


#rgb 94,60,50  ir 155,108,15

from PIL import Image
import numpy as np


output=np.full((137940,3),'0',dtype='|S12')
count=0
year=2000
while year<2020:
    idp=1
    print('Year',year)
    while idp<4:
        limit=0
        if idp==1 or idp==2:
            limit = 3311
        else:
            limit=275
        ids=0
        print('----------',idp,'---------')
        while ids<limit:
            if ids%500==0:
                print(ids)
            
            aid=str(year)+"01"+str(idp)+"_"+str(ids)
            bid=str(year)+"07"+str(idp)+"_"+str(ids)
            did=str(year)+"07"+str(idp)+"_"+str(ids)+"-"+str(year)+"01"+str(idp)+"_"+str(ids)
            
            diffrgb=np.array(Image.open("diffrgb/"+did+".png").convert('RGB'),np.uint8)
            diffir=np.array(Image.open("diffir/"+did+".png").convert('RGB'),np.uint8)
            
            
            
            validRGB=[94,60,50]
            validIR=[155,108,15]
            
            ignorance=30 #how much the color could differ?
            chunkReq=4 #MxM square required
            
            
            containsN = [ abs(diffir[x][y]-validIR).max()<ignorance and abs(diffrgb[x][y]-validRGB).max()<ignorance for x in range(100) for y in range(100)]
            containsN=np.reshape(containsN,(100,100))
            contains=False
            area=[0,0]
            conchk=np.full((chunkReq,chunkReq),True)
            for x in range(100-chunkReq):
                for y in range(100-chunkReq):  
                    
                    if (containsN[x:x+chunkReq,y:y+chunkReq] == conchk).all():
                        contains=True
                        area=[x,y]
                        break
            if contains:                
                output[count][0]=str(aid)
                output[count][1]=str(bid)
                output[count][2]=str(1)
            
            ids+=1
            count+=1
        idp+=1
    year+=1


