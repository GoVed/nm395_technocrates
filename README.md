# nm395_technocrates
SIH2020 project on shifting cultivation


The project structure:-

General
---------------------

seeImg.py : Displays the image in well formatted way for a given time

sectioningImage.py : Generating visualizable image which corresponds to the processed data for visualization



New model
---------------------


v3VarVis.py : The final visualization file. Enter the image as input and it will generate the visualizable image

trainingV3Var.py : For training the model

v3DiffClassify.py : Classification of processed images

ndvitest.py : Generating ndvi and water indexed from the raw data

gettingChange.py : Getting change over 8 years of data (Warning huge array, about 2GB)



Old model
---------------------

classifyTest.py : Test file for classifying shifting cultivation

visualize.py : Visualization of result of the model.

makingModel.py : Generating processed data for training.

trainingModel.py : Training the model over the data.

---------------------


Other
---------------------

.h5 files : Saved models for predicting.

.npy files : Saved numpy array for direct loading (No need to recalculate)


