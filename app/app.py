from flask import Flask, render_template, request, redirect, url_for
import json
import os
import pymongo
from bson import ObjectId
from mtools.util.logline import LogLine

app = Flask(__name__)

conn = pymongo.Connection()
filedb = conn.files
storage_dir = "/tmp/mtools_storage"

from celery_conf import celery
from report_tasks import run_report

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        logfile = request.files['logfile']
        if logfile:
            filename = ObjectId()
            filedb.files.insert({'_id': filename, 'reports': {}})
            logfile.save(os.path.join(storage_dir, str(filename)))
            return redirect(url_for('view', file_id=filename))
        else:
            return render_template('home.html')

@app.route("/plot_queries/<file_id>", methods=['GET'])
def plot_queries(file_id):
    logfile = open(os.path.join(storage_dir, str(file_id)))
    i = 0
    while True:
        i += 1
        x = logfile.readline()
        #ll = LogLine(x)
        print i
        if not x:
            break

    return ''

@app.route('/files/', methods=['GET'])
def index():
    file_list = os.listdir(storage_dir)
    return render_template('log/index.html', files=file_list)

@app.route('/files/view/<file_id>', methods=['GET'])
def view(file_id):
    filepath = os.path.join(storage_dir, str(file_id))
    logfile = open(filepath, 'r')
    file_obj = filedb.files.find_one({'_id': ObjectId(file_id)})
    reports = {}
    for report_type, task_id in file_obj.get('reports', {}).items():
        task = celery.AsyncResult(task_id)
        reports[report_type] = task.state
    return render_template('log/view.html',
            reports=reports,
            logfile=logfile)

@app.route('/reports/<file_id>/<report_type>', methods=['GET'])
def load_report(file_id, report_type):
    print str(file_id) + "_" + "durationplot"
    return json.dumps(filedb.reports.find_one({"_id":str(file_id) + "_" + "durationplot"}))

@app.route('/files/<file_id>/register/<report_type>', methods=['POST'])
def register_report(file_id, report_type):
    app.logger.info("report type {0}".format(report_type))
    result = run_report.apply_async((file_id, report_type))

    filedb.files.update({'_id': ObjectId(file_id)},
            {'$set': {'reports.{0}'.format(report_type): result.id}})
    return result.id

if __name__ == "__main__":
    app.run(debug=True)
