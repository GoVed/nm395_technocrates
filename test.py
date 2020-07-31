import ee

# Initialize the Earth Engine module.
ee.Initialize()
img = ee.ImageCollection('LANDSAT/LE07/C01/T1').filterDate('1999-01-01', '2002-12-31')


# Print image object WITHOUT call to getInfo(); prints serialized request instructions
print(img)

