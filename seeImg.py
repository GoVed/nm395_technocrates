from PIL import Image
import numpy as np
year=2007
idp=2
ids=2740


aid=str(year)+"01"+str(idp)+"_"+str(ids)
bid=str(year)+"07"+str(idp)+"_"+str(ids)
did=str(year)+"07"+str(idp)+"_"+str(ids)+"-"+str(year)+"01"+str(idp)+"_"+str(ids)

img=np.zeros((200,300,3),np.uint8)
rgb1=Image.open("rgb/"+aid+".png").convert('RGB')
ir1=Image.open("ir/"+aid+".png").convert('RGB')
rgb2=Image.open("rgb/"+bid+".png").convert('RGB')
ir2=Image.open("ir/"+bid+".png").convert('RGB')
diffrgb=np.array(Image.open("diffrgb/"+did+".png").convert('RGB'),np.uint8)
diffir=Image.open("diffir/"+did+".png").convert('RGB')
# diffrgb *= 255/diffrgb.max()
# diffrgb = diffrgb.astype('uint8')
img[0:100, 0:100]=rgb1
img[100:200, 0:100]=ir1
img[0:100, 100:200]=rgb2
img[100:200, 100:200]=ir2
img[0:100, 200:300]=diffrgb
img[100:200, 200:300]=diffir
Image.fromarray(img).show()
