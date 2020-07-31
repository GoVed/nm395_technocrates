import tensorflow as tf
from PIL import Image
import numpy as np

model=tf.keras.models.load_model('tf2model2.h5')

count=0
year=2010
x_predict=np.zeros((3311,100,100,3,2))
while year<2011:
    idp=1
    print('Year',year)
    while idp<2:
        limit=0
        if idp==1 or idp==2:
            limit = 3311
        else:
            limit=275
        ids=0
        while ids<limit:
            did=str(year)+"07"+str(idp)+"_"+str(ids)+"-"+str(year)+"01"+str(idp)+"_"+str(ids)
            x_predict[ids,:,:,:,0]=np.array(Image.open("diffrgb/"+did+".png").convert('RGB'),np.uint8)
            x_predict[ids,:,:,:,1]=np.array(Image.open("diffir/"+did+".png").convert('RGB'),np.uint8)
            
            ids+=1
        idp+=1
    year+=1
y_predicted=model.predict(x_predict)