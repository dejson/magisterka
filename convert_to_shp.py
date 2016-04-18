import sys
import os
import pickle
import osgeo.ogr as ogr
import osgeo.osr as osr

mypath = '/home/ddeja/Documents/studia/lidar/better/'

def convert(filename, layer):
    
    with open(mypath + filename, 'rb') as f:
        f = pickle.load(f)
        result = []

        for points in f:
            ring = ogr.Geometry(ogr.wkbLinearRing)
            for x, y, z in zip(points[0], points[1], points[2]):
                ring.AddPoint(x, y, z)
            poly = ogr.Geometry(ogr.wkbPolygon)
            poly.AddGeometry(ring)
            result.append(poly)

            feature = ogr.Feature(layer.GetLayerDefn())
            feature.SetGeometry(poly)
            layer.CreateFeature(feature) 
            feature.Destroy()

    return result

def get_file_list():
    onlyfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
    return onlyfiles

def main(input_list):
    result_file = input_list[0]
    filelist = get_file_list()

    spatialReference = osr.SpatialReference()
    spatialReference.ImportFromEPSG(2180)

    driver = ogr.GetDriverByName('ESRI Shapefile')
    shapeData = driver.CreateDataSource(result_file)

    layer = shapeData.CreateLayer('Layer1', spatialReference, ogr.wkbPolygon)
    for f in filelist:
        convert(f, layer)

    shapeData.Destroy()

if __name__ == '__main__':
    main(sys.argv[1:])
