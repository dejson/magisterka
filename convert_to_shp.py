import sys
import os
import pickle
import osgeo.ogr as ogr
import osgeo.osr as osr

def convert(filename, layer):
    
    with open(filename, 'rb') as f:
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


def main(argv):
    filename = argv[0]
    result_file = argv[1]
    import ipdb; ipdb.set_trace()

    spatialReference = osr.SpatialReference()
    spatialReference.ImportFromProj4('+proj=longlat +ellps=GRS80 +vunits=m +no_defs ')

    driver = ogr.GetDriverByName('ESRI Shapefile')
    shapeData = driver.CreateDataSource(result_file)

    layer = shapeData.CreateLayer('Layer1', spatialReference, ogr.wkbPolygon)
    convert(filename, layer)

    shapeData.Destroy()

if __name__ == '__main__':
    main(sys.argv[1:])
