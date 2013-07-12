from celery import Celery
from report_generators import generate_plot_report

celery = Celery('reports', broker='mongodb://localhost:27017/report_tasks')


@celery.task
def run_report(file_id, report_type):
    print "i am running the reportttttt"
    generate_plot_report(file_id) # write result of the report



    #print 'report: {0}'.format(report_type)
