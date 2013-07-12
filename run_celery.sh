#!/bin/sh
celery -A app.report_tasks worker
