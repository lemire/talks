from flask import Flask, render_template, request, jsonify
import boto3
from datetime import datetime
import uuid

app = Flask(__name__)
with open("secret.txt", "r") as file:
      secret = file.read().strip()


@app.route('/')
def upload_file_render():
   return render_template('map.html')

@app.route('/query')
def query_function():
    dynamodb = boto3.resource('dynamodb', aws_access_key_id="AKIAWTSKHA76FSSB2Z7S", aws_secret_access_key=secret, region_name="ca-central-1" )
    evil = dynamodb.Table("evil_locations")
    return jsonify(evil.scan())

@app.route('/add')
def add_function():
    dynamodb = boto3.resource('dynamodb', aws_access_key_id="AKIAWTSKHA76FSSB2Z7S", aws_secret_access_key=secret, region_name="ca-central-1" )
    evil = dynamodb.Table("evil_locations")
    args = request.args
    if "lat" in args and "long" in args:
        lat=args["lat"]
        long=args["long"]
        dt = str(datetime.now())
        return jsonify(evil.put_item(
              Item = {
               'locationid': str(uuid.uuid4()),
               'latitude': str(lat),
               'longitude': str(long),
               'time': dt
             }
            ))
    else:
        jsonify({})


def list_content():
    import os
    for current_dir, subdirs, files in os.walk( '.' ):
      # Current Iteration Directory
      print( current_dir )

      # Directories
      for dirname in subdirs:
        print( '\t' + dirname )

      # Files
      for filename in files:
        print( '\t' + filename )

if __name__ == '__main__':
    list_content()
    app.run(host='0.0.0.0', port=5005)