from celery_conf import celery

@celery.task
def run_report(file_id, report_type):
    print "i am running the reportttttt"
    generate_plot_report(file_id) # write result of the report



    #print 'report: {0}'.format(report_type)
