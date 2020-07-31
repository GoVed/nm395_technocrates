from PIL import Image
import numpy as np


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
            openpath=str(year)+"07"+str(idp)+"_"+str(ids) 
            img=np.array(Image.open("v3diff/"+openpath+".png"),np.uint8)
            img=np.array(abs(np.array(img,dtype=np.float64)-img.mean()),np.uint8)            
            rname = 'v3var/'+openpath+'.png'            
            rgbdiff=Image.fromarray(img)
            rgbdiff.save(rname)
                
            ids+=1
        
        idp+=1
    
    year+=1