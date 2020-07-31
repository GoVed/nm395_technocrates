from PIL import Image
import numpy as np
year=2000
idp=1
ids=192

imgrgb=[]
imgir=[]
for i in range(8):
        
    did=str(year)+"07"+str(idp)+"_"+str(ids)+"-"+str(year)+"01"+str(idp)+"_"+str(ids)
    diffrgb=np.array(Image.open("diffrgb/"+did+".png").convert('RGB'),np.int16)
    diffir=np.array(Image.open("diffir/"+did+".png").convert('RGB'),np.int16)
    
    imgrgb.append(diffrgb)
    imgir.append(diffir)
    
    year+=1


i=3
while i>0:
    crgb=[]
    cir=[]
    j=0
    while j<len(imgrgb):
        crgb.append(abs(imgrgb[j+1]-imgrgb[j]))
        cir.append(abs(imgir[j+1]-imgir[j]))
        j+=2
    imgrgb=crgb
    imgir=cir
    i-=1

Image.fromarray(np.array(imgrgb[0],dtype=np.uint8)).show()
