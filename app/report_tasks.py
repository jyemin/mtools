from celery import Celery

celery = Celery('reports', broker='mongodb://localhost:27017/report_tasks')


@celery.task
def run_report(file, report_type):
    print 'report: {0}'.format(report_type)
    return 'wildcat'
