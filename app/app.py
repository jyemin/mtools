from flask import Flask, render_template, request, redirect, url_for
import os
import pymongo
import gridfs
from bson import ObjectId
from mtools.util.logline import LogLine
app = Flask(__name__)

conn = pymongo.Connection()
filedb = conn.files
storage_dir = "/tmp/mtools_storage"

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        logfile = request.files['logfile']
        if logfile:
            filename = ObjectId()
            logfile.save(os.path.join(storage_dir, str(filename)))
            return redirect(url_for('view', file_id=filename))
        else:
            return render_template('home.html')

@app.route("/plot_queries/<file_id>", methods=['GET'])
def plot_queries(file_id):
    gfs = gridfs.GridFS(filedb)
    logfile = gfs.get(ObjectId(file_id))
    i = 0
    while True:
        i += 1
        x = logfile.readline()
        #ll = LogLine(x)
        print i
        if not x:
            break

    return ''

@app.route('/<file_id>', methods=['GET', 'PUT'])
def view(file_id):
    filepath = os.path.join(storage_dir, str(file_id))
    logfile = open(filepath, 'r')
    return render_template('log_view.html',
            reports=[],
            logfile=logfile)

if __name__ == "__main__":
    app.run(debug=True)
