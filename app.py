"""
Simple flask app.
"""
from flask import (Flask,
                   jsonify,
                   render_template,
                   request,
                   redirect, 
                   url_for)
import tablib
import os
import pandas as pd

# from ec2.prophet_db import web_query

UPLOAD_FOLDER = 'data/'
ALLOWED_EXTENSIONS = set(['csv'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
dataset = tablib.Dataset()
with open(os.path.join(os.path.dirname(__file__),'data/data-for-html-1.csv')) as f:
    dataset.csv = f.read()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
#            filename = secure_filename(file.filename)
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_file'))
        else:
            return render_template('index.html')
    return render_template('index.html')


@app.route('/uploaded_file', methods = ['GET', 'POST'])
def uploaded_file():
	#for uploading file 
    return render_template('uploaded_file.html')


@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
	# Welcome page to explain what is going on in the site
    return render_template('welcome.html')


@app.route('/favorites', methods=['GET', 'POST'])
def favorites():
	# Favorites page to explain how to get the favorited csv file
    return render_template('favorites.html')


@app.route('/data', methods=['GET', 'POST'])
def data():
	# Data page to show what the data looks like
    data = dataset.html
    return render_template('data.html', data=data)
    


def main():
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    main()