from django.conf.urls import patterns, url
from views import *

urlpatterns = patterns(
    '',
    url(r'^logs/$', logfiles_list, name='log-files-list-admin'),
    url(r'^logs/(?P<logfile_id>\d+)/$', logfile_view,
        name='log-file-admin'),
    url(r'^logs/(?P<logfile_id>\d+)/csv$', logfile_to_csv,
        name='log-file-to-csv-admin'),
)
