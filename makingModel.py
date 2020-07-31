import pandas as pd
import random
from PIL import Image
import numpy as np


#id2 is 07 and id1 is 01
def getImg(id1="",id2=""):
    img=np.zeros((100,100,3,6),np.uint8)
    rgb1=Image.open("rgb/"+id1+".png").convert('RGB')
    ir1=Image.open("ir/"+id1+".png").convert('RGB')
    rgb2=Image.open("rgb/"+id2+".png").convert('RGB')
    ir2=Image.open("ir/"+id2+".png").convert('RGB')
    diffrgb=Image.open("diffrgb/"+id2+"-"+id1+".png").convert('RGB')
    diffir=Image.open("diffir/"+id2+"-"+id1+".png").convert('RGB')
    
    img[0:100, 0:100, 0:3 , 0]=rgb1
    img[0:100, 0:100, 0:3 , 1]=ir1
    img[0:100, 0:100, 0:3 , 2]=rgb2
    img[0:100, 0:100, 0:3 , 3]=ir2
    img[0:100, 0:100, 0:3 , 4]=diffrgb
    img[0:100, 0:100, 0:3 , 5]=diffir
    return img



lables=pd.read_csv("lables.csv")
lables=lables.to_numpy()

features=np.full((2000,100,100,3,6),0,dtype=np.uint8)

randomimg=np.random.choice(range(len(lables)),400)
i=0
for each in randomimg:
    print(i)
    features[i]=getImg(lables[each][0],lables[each][1])
    i+=1

while i<2000:
    print(i)
    year=random.randint(2000,2019)
    idp=random.randint(1,3)
    ids=0
    if idp==1 or idp==2:
        ids=random.randint(0,3310)
    else:
        ids=random.randint(0,273)
    aid=str(year)+"01"+str(idp)+"_"+str(ids)
    bid=str(year)+"07"+str(idp)+"_"+str(ids)
    features[i]=getImg(aid,bid)
    i+=1
    
    
#get 400 images with sifting cultivation and 1600 without it
#generate (2000,100,100,18) numpy