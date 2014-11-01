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
    return render_template('home.html')

@app.route('/timeline')
def show_timeline():
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

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

#Fires up the server
if __name__ == '__main__':
    app.run(debug=True)
