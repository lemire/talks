import exifread

# pip3 install exifread
# source: https://gist.github.com/snakeye/fdc372dbf11370fe29eb

def get_if_exist(data, key):
    if key in data:
        return data[key]
    return None


def _convert_to_degress(value):
    """
    Helper function to convert the GPS coordinates stored in the EXIF to degress in float format
    :param value:
    :type value: exifread.utils.Ratio
    :rtype: float
    """
    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)

    return d + (m / 60.0) + (s / 3600.0)
    
def get_exif_location(exif_data):
    """
    Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)
    """
    lat = None
    lon = None

    gps_latitude = get_if_exist(exif_data, 'GPS GPSLatitude')
    gps_latitude_ref = get_if_exist(exif_data, 'GPS GPSLatitudeRef')
    gps_longitude = get_if_exist(exif_data, 'GPS GPSLongitude')
    gps_longitude_ref = get_if_exist(exif_data, 'GPS GPSLongitudeRef')

    if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
        lat = _convert_to_degress(gps_latitude)
        if gps_latitude_ref.values[0] != 'N':
            lat = 0 - lat

        lon = _convert_to_degress(gps_longitude)
        if gps_longitude_ref.values[0] != 'E':
            lon = 0 - lon

    return lat, lon


def get_exif_data(image_file):
    with open(image_file, 'rb') as f:
        exif_tags = exifread.process_file(f)
    return exif_tags 

from datetime import datetime
import sqlite3

def log(long,lat):
  con = sqlite3.connect("img.db")
  with con:
    tables = [row[0] for row in con.execute("SELECT name FROM sqlite_master WHERE type='table'")]
    if not "geo" in tables:
        con.execute("CREATE TABLE geo (date TEXT, long NUMERIC, lat NUMERIC)")
    dt = datetime.now()
    con.execute("INSERT INTO geo (date,long,lat) values (\""+str(dt)+"\","+str(long)+", "+str(lat)+") ")
  con.close()

# credit : https://pythonbasics.org/flask-upload-file/
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/upload')
def upload_file_render():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      sn = secure_filename(f.filename)
      print("saving ",sn)
      f.save(sn)
      lat, long = get_exif_location(get_exif_data(sn))
      print(lat, long)
      if lat is None:
          return render_template('upload.html')
      link = "https://www.openstreetmap.org/?mlat="+str(lat)+"&mlon="+str(long)+"&zoom=15"
      print(link)
      log(long,lat)
      return "<html><body><a href=\""+link+"\">map</a></body></html>"
		
if __name__ == '__main__':
   app.run(debug = True)