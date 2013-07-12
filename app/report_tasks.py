from celery_conf import celery
from report_generators import generate_plot_report

@celery.task
def run_report(file_id, report_type, task_id=None):
    print "i am running the reportttttt"
    generate_plot_report(file_id, task_id) # write result of the report



