from flask import Flask, render_template, request, jsonify, redirect
from pymongo import MongoClient, GEO2D
from collections import Counter
from jinja2 import Template
from email.utils import parseaddr
import math
import random

app = Flask(__name__)
db = MongoClient('45.79.159.210', 27017).fandemic

#================INDEX=====================
@app.route('/')
@app.route("/index")
def home():

    count = db.stars.find({'email':{'$size': 0}}).count()

    stars = db.stars.find({'email':{'$size': 0}}).limit(30).skip( int(round( random.random() * count )) ) #find the star

    return render_template('index.html', stars = stars, count = count)


@app.route('/batchUpdateEmail', methods=['GET', 'POST'])
def update():

    if request.method == 'POST':
        name = request.form
        for v in request.form:
            email = request.form[v]
            email = parseaddr(email)[1]
            if email != '':
                db.stars.update_one({'id':v},{"$set":{"email.0":email}})

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
