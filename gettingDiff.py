from PIL import Image
import numpy as np

year=2000
while year<2020:
    idp=1
    while idp<4:
        limit=0
        if idp==1 or idp==2:
            limit = 3311
        else:
            limit=275
        ids=0
        print(year,idp,'-----------------')
        while ids<limit:
            if ids%500==0:
                print(ids)
            fromid=str(year)+"07"+str(idp)+"_"+str(ids)
            toid=str(year)+"01"+str(idp)+"_"+str(ids)
            cimg0 = np.array(Image.open("rgb/"+toid+".png").convert('RGB'),np.int16)
            cimg1 = np.array(Image.open("rgb/"+fromid+".png").convert('RGB'),np.int16)
            iimg0 = np.array(Image.open("ir/"+toid+".png").convert('RGB'),np.int16)
            iimg1 = np.array(Image.open("ir/"+fromid+".png").convert('RGB'),np.int16)
            
            
            cimgd=np.array(abs(cimg1-cimg0),np.uint8)
            iimgd=np.array(abs(iimg1-iimg0),np.uint8)
            
            cImg=Image.fromarray(cimgd)
            cImg.save("diffrgb/"+fromid+"-"+toid+".png")
            cImg=Image.fromarray(iimgd)
            cImg.save("diffir/"+fromid+"-"+toid+".png")
            ids+=1
        idp+=1
    year+=1


