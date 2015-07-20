from django.conf.urls import patterns, url
from views import *

urlpatterns = patterns('',
                       url(r'^django_log_file_viewer/logfile/$', logfiles_list,
                           name='log-files-list-admin'),
                       url(r'^django_log_file_viewer/logfile/(?P<logfile_id>\d+)/$',
                           logfile_view,
                           name='log-file-admin'),
                       url(r'^django_log_file_viewer/logfile/(?P<logfile_id>\d+)/csv$',
                           logfile_to_csv,
                           name='log-file-to-csv-admin'),
                       )
