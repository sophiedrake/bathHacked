#!/usr/bin/env python
import os
import sqlite3
import math
import random
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash


# create our little application
app = Flask(__name__)
app.config.from_object(__name__)
DATABASE = os.path.join(app.root_path, 'sqlite_db.db')



@app.route('/')
def show_landing():
    return render_template('example_json.html')

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

@app.route('/testing')
def show_testing():
    p = "BA2 3PB"
    postcodes = query_db('select score from Score where Postcode= \"' + p + '\"')
    print postcodes
    return render_template('testing.html', postcodes=postcodes)

@app.route('/map', methods=['POST'])
def show_map():
    p = request.form['address']
    p = p.upper()
    p = p.replace(" ", "")
    
    recycling = query_db('select score from score where Postcode= \"' + p + '\" and Metric = \"Recycling\"')
    if len(recycling) >= 1:
      recycling = recycling[0][0]
    if recycling == []:
      ward = find_ward_by_postcode(p)
      if ward is None:
        recycling = "?"
      else:
        recycling = query_db('select score from score where Ward= \"' + ward[0] + '\" and Metric = \"Recycling\"')
        if len(recycling) >= 1:
          recycling = recycling[0][0]
    if recycling is None:
      recycling = "?"
     
    gas = query_db('select score from score where Postcode= \"' + p + '\" and Metric = \"Gas\"')
    if len(gas) >= 1:
      gas = gas[0][0]
    if gas == []:
      ward = find_ward_by_postcode(p)
      if ward is None:
        gas = "?"
      else:
        gas = query_db('select score from score where Ward= \"' + ward[0] + '\" and Metric = \"Gas\"')
        if len(gas) >= 1:
          gas = gas[0][0]
    if gas is None:
      gas = "?"

    electricity = query_db('select score from score where Postcode= \"' + p + '\" and Metric = \"Electricity\"')
    if len(electricity) >= 1:
      electricity = electricity[0][0]
    if electricity == []:
      ward = find_ward_by_postcode(p)
      if ward is None:
        electricity = "?"
      else:
        electricity = query_db('select score from score where Ward= \"' + ward[0] + '\" and Metric = \"Electricity\"')
        if len(electricity) >= 1:
          electricity = electricity[0][0]
    if electricity is None:
      electricity = "?"
      
    transport = query_db('select score from score where Postcode= \"' + p + '\" and Metric = \"Transport\"')
    if len(transport) >= 1:
      transport = transport[0][0]
    if  transport  == []:
      ward = find_ward_by_postcode(p)
      if ward is None:
         transport  = "?"
      else:
        transport  = query_db('select score from score where Ward= \"' + ward[0] + '\" and Metric = \"Transport\"')
        
        if len(transport) >= 1:
          transport = transport[0][0]
        if  transport  == []:
          transport = "?"
    if  transport  is None:
       transport  = "?"

    final = query_db('select score from score where Postcode= \"' + p + '\" and Metric = \"Final\"')
    if len(final) >= 1:
      final = final[0][0]
    if  final  == []:
      ward = find_ward_by_postcode(p)
      if ward is None:
         final  = "?"
      else:
        final  = query_db('select score from score where Ward= \"' + ward[0] + '\" and Metric = \"Final\"')
        if len(final) >= 1:
          final = final[0][0]
        if  final  == []:
          final = "?"
    if  final  is None:
       final  = "?"

    
    
    return render_template('map.html', address=p, recycling=recycling, gas=gas, electricity=electricity, transport=transport, final=final)

@app.route('/more')
def more():
    return render_template('more.html')

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


#Fires up the server
if __name__ == '__main__':
    app.run(debug=True)
