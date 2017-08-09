# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Fichier des fonctions du plugin cc
                                 A QGIS plugin
 Projette des points sur une ligne/bordure de polygone à la distance la plus courte: "decoupeur"
                              -------------------
        begin                : 2013-11-04
        copyright            : (C) 2013 by Jean-Christophe Baudin ONEMA DIR9
                               d'après "Nearest neighbor between a point layer and a line layer
                               in http://gis.stackexchange.com/questions/396/
                               nearest-pojected-point-from-a-point-
                               layer-on-a-line-or-polygon-outer-ring-layer
        email                : jean-christophe.baudin@onema.fr
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import unicodedata,sys
from PyQt4 import QtCore
from PyQt4 import QtGui
from qgis.core import *
from qgis.gui import *

from shapely.geometry import Point, LineString, Polygon
from shapely.wkb import loads
from shapely.wkt import  dumps

from osgeo import ogr
from math import sqrt
from sys import maxint

#handling outputFile: path name, file name and extension
import os, shutil, tempfile

import csv, sys
import re
import os
import unicodedata

# pairs iterator:
# http://stackoverflow.com/questions/1257413/1257446#1257446
def pairs(lst):
    i = iter(lst)
    first = prev = i.next()
    for item in i:
        yield prev, item
        prev = item
    yield item, first

# these methods rewritten from the C version of Paul Bourke's
# geometry computations:
# http://local.wasp.uwa.edu.au/~pbourke/geometry/pointline/

def magnitude(p1, p2):
    vect_x = p2.x - p1.x
    vect_y = p2.y - p1.y
    return sqrt(vect_x**2 + vect_y**2)

def intersect_point_to_line(point, line_start, line_end):
    line_magnitude =  magnitude(line_end, line_start)
    u = ((point.x - line_start.x) * (line_end.x - line_start.x) +
         (point.y - line_start.y) * (line_end.y - line_start.y)) \
         / (line_magnitude ** 2)

    # closest point does not fall within the line segment, 
    # take the shorter distance to an endpoint
    if u < 0.00001 or u > 1:
        ix = magnitude(point, line_start)
        iy = magnitude(point, line_end)
        if ix > iy:
            return line_end
        else:
            return line_start
    else:
        ix = line_start.x + u * (line_end.x - line_start.x)
        iy = line_start.y + u * (line_end.y - line_start.y)
        return Point([ix, iy])
    
# ProjecteurP1 pour lignes   
def ProjecteurP1(ObjetPoint,ObjetBerge):
    nearest_point = None
    min_dist = maxint
    berges = loads(ObjetBerge.asWkb())
    point = loads(ObjetPoint.asWkb())
    
    for seg_start, seg_end in pairs(list(berges.coords)[:-1]):
        line_start = Point(seg_start)
        line_end = Point(seg_end)
        
        intersection_point = intersect_point_to_line(point, line_start, line_end)
        cur_dist =  magnitude(point, intersection_point)

        if cur_dist < min_dist:
            min_dist = cur_dist
            nearest_point = intersection_point
            
    ProjPoint= QgsGeometry.fromWkt(dumps(nearest_point))
    return ProjPoint,min_dist
    
# ProjecteurP2 Pour polygone avec son outer rim           
def ProjecteurP2(ObjetPoint,ObjetBerge):
    nearest_point = None
    min_dist = maxint
    berges = loads(ObjetBerge.asWkb())
    point = loads(ObjetPoint.asWkb())
    
    for seg_start, seg_end in pairs(list(berges.exterior.coords)[:-1]):
        line_start = Point(seg_start)
        line_end = Point(seg_end)

        intersection_point = intersect_point_to_line(point, line_start, line_end)
        cur_dist =  magnitude(point, intersection_point)

        if cur_dist < min_dist:
            min_dist = cur_dist
            nearest_point = intersection_point
            
    ProjPoint= QgsGeometry.fromWkt(dumps(nearest_point))        
    return ProjPoint,min_dist
	
# Projecteurdecoupeur Stackexange Nearest neigbor between a point layer and a line layer
# Pour polygone avec son outer rim

def Projecteurdecoupeur(ObjetPoint,ObjetBerge):
    
    min_dist = maxint
    berges = loads(ObjetBerge.asWkb())
    point = loads(ObjetPoint.asWkb())
	
    ProjPointShapely= berges.interpolate(berges.project(point))
    min_dist=magnitude(point,ProjPointShapely)
    ProjPoint= QgsGeometry.fromWkt(dumps(ProjPointShapely))        
    return ProjPoint,min_dist
	
   

def getVectorLayerByName(NomCouche):
    layermap=QgsMapLayerRegistry.instance().mapLayers()
    for name, layer in layermap.iteritems():
        if layer.type()==QgsMapLayer.VectorLayer and layer.name()==NomCouche:
            if layer.isValid():
               return layer
            else:
               return None
            

    



