#!/usr/bin/env python
import os
import sqlite3
import math
import random
from osgeo import osr, gdal
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash


# create our little application
app = Flask(__name__)
app.config.from_object(__name__)
DATABASE = os.path.join(app.root_path, 'sqlite_db.db')

@app.route('/')
def show_landing():
    return render_template('home.html')

@app.route('/timeline')
def show_timeline():
    return render_template('timeline.html')

def getMapInfo(name):
        # get the existing coordinate system
    ds = gdal.Open(name)
    old_cs= osr.SpatialReference()
    old_cs.ImportFromWkt(ds.GetProjectionRef())

    # create the new coordinate system
    wgs84_wkt = """
    GEOGCS["WGS 84",
        DATUM["WGS_1984",
            SPHEROID["WGS 84",6378137,298.257223563,
                AUTHORITY["EPSG","7030"]],
            AUTHORITY["EPSG","6326"]],
        PRIMEM["Greenwich",0,
            AUTHORITY["EPSG","8901"]],
        UNIT["degree",0.01745329251994328,
            AUTHORITY["EPSG","9122"]],
        AUTHORITY["EPSG","4326"]]"""
    new_cs = osr.SpatialReference()
    new_cs .ImportFromWkt(wgs84_wkt)

    # create a transform object to convert between coordinate systems
    transform = osr.CoordinateTransformation(old_cs,new_cs) 

    #get the point to transform, pixel (0,0) in this case
    width = ds.RasterXSize
    height = ds.RasterYSize
    gt = ds.GetGeoTransform()
    minx = gt[0]
    miny = gt[3] + width*gt[4] + height*gt[5] 
    maxx = gt[0] + width*gt[1] + height*gt[2]
    maxy = gt[3]

    #get the coordinates in lat long
    sw = transform.TransformPoint(minx,miny)
    ne = transform.TransformPoint(maxx, maxy)
    sw = (sw[1],sw[0])
    ne = (ne[1], ne[0])
    return (sw,ne)

@app.route('/maps1572')
def show_maps():
    url = '../static/1572-jones.jpg'
  #  result = getMapInfo('static/1572-geo.tiff')
   # print result
    sw = (51.37664244922259, -2.3664062869774063)
    ne = (51.3854469338053, -2.3507642429564233)
    return render_template('maps.html', sw=sw, ne=ne, url=url, year='1572')

@app.route('/maps1891')
def show_maps1():
    url = '../static/bath-1891.jpg'
    #result = getMapInfo('static/bath-1891-geo.tiff')
    #print result
    sw = (51.3707976034083, -2.389822300856615)
    ne = (51.39919189594104, -2.3322347272066253)
    return render_template('maps.html', sw=sw, ne=ne, url=url, year='1891')

@app.route('/league')
def show_league():
    temp = query_db("SELECT * FROM score WHERE Postcode IS NOT NULL AND Metric=\"Final\" ORDER BY Score DESC LIMIT 20")
    count = 1;
    records =[]
    for item in temp:
        recycling = query_db('select score from score where Postcode= \"' + item[1] + '\" and Metric = \"Recycling\"')
        transport = query_db('select score from score where Ward LIKE \"' + item[2] + '\" and Metric = \"Transport\"')
        electricity = query_db('select score from score where Ward= \"' + item[2] + '\" and Metric = \"Electricity\" LIMIT 1')
        gas = query_db('select score from score where Ward= \"' + item[2] + '\" and Metric = \"Gas\"')
        transport = random.randint(7,9)
        records.append([count, item[1], item[2], item[4], recycling, transport, electricity, gas])
        count = count + 1
    return render_template('league.html', records=records)

@app.route('/about')
def show_about():
    return render_template('about.html')

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

#Fires up the server
if __name__ == '__main__':
    app.run(debug=True)
