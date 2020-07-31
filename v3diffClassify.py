#valid at 66

from PIL import Image
import numpy as np


output=[]
yOut=[]
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
            
            aid=str(year)+"07"+str(idp)+"_"+str(ids)


            img=np.array(Image.open("v3var/"+aid+".png"),np.uint8)
            
            valid=40
            
            # ignorance=10 #how much the color could differ?
            chunkReq=3 #MxM square required
            ignorance=1 #how many pixel can be not in chunk? Must be less than chunkReq*chunkReq
            
            containsN = [ img[x][y]>valid for x in range(100) for y in range(100)]
            containsN=np.reshape(containsN,(100,100))
            contains=False
            area=[0,0]
            conchk=np.full((chunkReq,chunkReq),True)
            count=0
            for x in range(100-chunkReq):
                for y in range(100-chunkReq):  
                    if np.count_nonzero(containsN[x:x+chunkReq,y:y+chunkReq])>=(chunkReq*chunkReq)-ignorance:
                        contains=True
                        area=[x,y]
                        count+=1
                        break
            if contains:                
                output.append(str(aid))
                yOut.append(count)
            
            ids+=1
            count+=1
        idp+=1
    year+=1


# year=2019
# idp=2
# ids=1621

# aid=str(year)+"07"+str(idp)+"_"+str(ids)


# img=np.array(Image.open("v3var/"+aid+".png"),np.uint8)

# valid=40

# # ignorance=10 #how much the color could differ?
# chunkReq=3 #MxM square required
# ignorance=1 #how many pixel can be not in chunk? Must be less than chunkReq*chunkReq

# containsN = [ img[x][y]>valid for x in range(100) for y in range(100)]
# containsN=np.reshape(containsN,(100,100))
# contains=False
# area=[0,0]
# conchk=np.full((chunkReq,chunkReq),True)
# for x in range(100-chunkReq):
#     for y in range(100-chunkReq):  
#         if np.count_nonzero(containsN[x:x+chunkReq,y:y+chunkReq])>=(chunkReq*chunkReq)-ignorance:
#             contains=True
#             area=[x,y]
#             break



    