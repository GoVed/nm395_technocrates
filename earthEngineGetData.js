var cloudMaskL457 = function(image) {
  var qa = image.select('pixel_qa');
  // If the cloud bit (5) is set and the cloud confidence (7) is high
  // or the cloud shadow bit is set (3), then it's a bad pixel.
  var cloud = qa.bitwiseAnd(1 << 5)
                  .and(qa.bitwiseAnd(1 << 7))
                  .or(qa.bitwiseAnd(1 << 3));
  // Remove edge pixels that don't occur in all bands
  var mask2 = image.mask().reduce(ee.Reducer.min());
  return image.updateMask(cloud.not()).updateMask(mask2);
};
var i=12;

while(i<16){
  try{
      var year=i.toString();
      if(year.length==1)
        year="0"+year;
      var startDate = "20"+year+"-01-01";
      var endDate = "20"+year+"-06-30";
      var dataset = ee.ImageCollection('LANDSAT/LE07/C01/T1_SR')
                        .filterDate(startDate,endDate)
                        .map(cloudMaskL457);
      
      // Create a geometry representing an export region.
      var geometry = ee.Geometry.Rectangle([89, 25, 93, 26.2]);
      
      // Export the image, specifying scale and region.
      Export.image.toDrive({
          image: dataset.median(),
          description: 'meghalaya'+startDate,
          scale: 30,
          region: geometry
        });
        
        
      startDate = "20"+year+"-07-01";
      endDate = "20"+year+"-12-31";
      var dataset2 = ee.ImageCollection('LANDSAT/LE07/C01/T1_SR')
                        .filterDate(startDate,endDate)
                        .map(cloudMaskL457);
      
      // Export the image, specifying scale and region.
      Export.image.toDrive({
          image: dataset2.median(),
          description: 'meghalaya'+startDate,
          scale: 30,
          region: geometry
        });
    }
    catch(err){
      print(err+","+year+month)
    }
  i++;
}