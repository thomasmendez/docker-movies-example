from flask import Flask, render_template, request, redirect, url_for, make_response, g
from werkzeug.utils import secure_filename
import sys
import os
import socket
import random
import json
import psycopg2 # for database connection and SQL execution

hostname = socket.gethostname()

UPLOAD_FOLDER = '/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# ---------------------
# Connect to PostgreSQL
# ---------------------
#t_host = "postgresql://postgres:postgres@localhost/postgres"
#t_host = "localhost"
#t_host = "192.168.1.161" # use the ip address to connect
t_host = "db" # if this does not work use docker-compose down --remove-orphans --volumes and rebuild 
t_port = "5432" #5432 is typically default port
t_dbname = "movies"
t_name_user = "username"
t_password = "password"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.urandom(24)

def Save_Movie_To_Database(title, month, day, year):
    try:
       connection = psycopg2.connect(host=t_host, 
                                     port=t_port, 
                                     dbname=t_dbname, 
                                     user=t_name_user, 
                                     password=t_password)
       cursor = connection.cursor()

       postgres_insert_query = """ INSERT INTO films (title, month, day, year) VALUES (%s,%s,%s,%s)"""
       record_to_insert = (title, month, day, year)
       cursor.execute(postgres_insert_query, record_to_insert)

       connection.commit()
       count = cursor.rowcount
       print (count, "Record inserted successfully into films table", file=sys.stdout)

    except (Exception, psycopg2.Error) as error :
        if(connection):
            print("Failed to insert record into films table", file=sys.stdout)
            print(error, file=sys.stdout)
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed", file=sys.stdout)

def Save_Movie_With_Image_To_Database(title, month, day, year, file_data):
    try:
       connection = psycopg2.connect(host=t_host, 
                                     port=t_port, 
                                     dbname=t_dbname, 
                                     user=t_name_user, 
                                     password=t_password)
       cursor = connection.cursor()

       postgres_insert_query = """ INSERT INTO films (title, month, day, year, file_data) VALUES (%s,%s,%s,%s,%s)"""
       record_to_insert = (title, month, day, year, file_data)
       cursor.execute(postgres_insert_query, record_to_insert)

       connection.commit()
       count = cursor.rowcount
       print (count, "Record inserted successfully into films table", file=sys.stdout)

    except (Exception, psycopg2.Error) as error :
        if(connection):
            print("Failed to insert record into films table", file=sys.stdout)
            print(error, file=sys.stdout)
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed", file=sys.stdout)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=['POST','GET'])
def home():

    title = 'Add Movie Title' 

    if request.method == 'GET':

        print('GET REQUEST', file=sys.stdout)
    
        resp = make_response(render_template(
            'index.html',
            title=title,
            hostname=hostname
        ))
    
        return resp

    elif request.method == 'POST':

        print('POST REQUEST', file=sys.stdout)

        # check if file was uploaded
        if not request.files.get('file_image'):
            print('No File Uploaded', file=sys.stdout)

            movie_title = request.form.get('movie_title')

            release_date = request.form.get('release_date')

            release_date = release_date.split('-')

            year = release_date[0]

            month = release_date[1]

            day = release_date[2]

            Save_Movie_To_Database(movie_title, month, day, year)

            resp = make_response(render_template(
                'index.html',
                title=title,
                hostname=hostname,
                uploaded='noImage'
            ))

            return resp

        file_image = request.files['file_image']

        if file_image and allowed_file(file_image.filename):

            print('File Uploaded', file=sys.stdout)

            print(file_image, file=sys.stdout)

            # convert to bytes
            file_image = file_image.read()

            #print(file_image, file=sys.stdout)

            movie_title = request.form.get('movie_title')

            release_date = request.form.get('release_date')

            release_date = release_date.split('-')

            year = release_date[0]

            month = release_date[1]

            day = release_date[2]

            Save_Movie_With_Image_To_Database(movie_title, month, day, year, file_image)

            resp = make_response(render_template(
                'index.html',
                title=title,
                hostname=hostname,
                uploaded='Image'
            ))

            return resp

        elif file_image and not allowed_file(file_image.filename):

            print('File Not Allowed')

            # incorrect file type
            resp = make_response(render_template(
                'index.html',
                title=title,
                hostname=hostname,
                uploaded='invalidFile'
            ))

            return resp

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)