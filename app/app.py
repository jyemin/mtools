from flask import Flask, render_template, request, redirect, url_for
import pymongo
import gridfs
from bson import ObjectId
app = Flask(__name__)

conn = pymongo.Connection()
filedb = conn.files

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        logfile = request.files['logfile']
        if logfile:
            gfs = gridfs.GridFS(filedb)
            file_id = gfs.put(logfile,
                    filename=logfile.filename,
                    content_type=logfile.content_type)
            return redirect(url_for('view', file_id=file_id))
        else:
            return render_template('home.html')

@app.route('/<file_id>', methods=['GET', 'PUT'])
def view(file_id):
            gfs = gridfs.GridFS(filedb)
            logfile = gfs.get(ObjectId(file_id))
            app.logger.info("asdf: {0}".format(dir(logfile)))
            reports = filedb.reports.find({'file_id': file_id})
            return render_template('log_view.html',
                    reports=reports,
                    logfile=logfile)

if __name__ == "__main__":
    app.run(debug=True)
