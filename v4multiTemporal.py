# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 23:33:51 2020

@author: vedhs
"""

import numpy as np
from PIL import Image



tyear=4
syear=5
upto=syear+tyear
img=[]
while syear<upto:
    year=2000+syear
    idp=1
    ids=0
    aid=str(year)+str(idp)+"_"+str(ids)
    
    img.append(np.array(Image.open("v4img/"+aid+".png"),np.uint8))
    syear+=1
img=np.array(img)
outimg=np.zeros((100,100))
for i in range(100):
    for j in range(100):
        var=0
        m=img[:,i,j].mean()
        for k in range(tyear):
            var+=abs(m-img[k,i,j])        
        outimg[i,j]=var/tyear
outimg=abs(outimg-outimg.mean())

del img
