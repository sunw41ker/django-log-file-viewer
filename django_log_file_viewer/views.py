# -*- coding: utf-8 -*-

# system
import os
import csv

# django
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, user_passes_test
from .settings import *

from .models import LogFilesManager

__all__ = ['logfiles_list', 'logfile_view', 'logfile_to_csv']


@login_required
@user_passes_test(lambda u: u.is_staff)
def logfiles_list(request, template_name='logfiles_admin.html'):
    """
    Lists Log Files in settings directory
    """
    manager = LogFilesManager()
    files_list = manager.list_logfiles(LOG_FILES_DIR)
    indexes = {}
    if files_list:
        count = 0
        for index in files_list:
            indexes[str(count)] = index[0]
            count += 1
    context = {'files_list': indexes, 'user': request.user}
    return render_to_response(template_name, context,
                              context_instance=RequestContext(request))


@login_required
@user_passes_test(lambda u: u.is_staff)
def logfile_view(request, logfile_id, template_name='logfile_admin.html'):
    """
    Returns a list of Log File content parsed by main regexp
    """
    search_input = request.GET.get('q')

    page = request.GET.get('page', '1')
    manager = LogFilesManager()
    files_list = manager.list_logfiles(LOG_FILES_DIR)
    file = files_list[int(logfile_id)]
    try:
        filename = file[0]
        logfile = os.path.join(LOG_FILES_DIR, file[0])
    except Exception:
        raise Http404('File not found')

    try:
        page = int(page)
    except ValueError:
        page = 1

    # log_file_object = manager.get_file(logfile)
    log_file_lines = manager.parse_log_file(logfile, file[1], 0)
    log_file_lines_filtered = log_file_lines
    if search_input:
        log_file_lines_filtered = [
            l for l in log_file_lines
            if search_input in ''.join(l).decode('utf-8')]
    pag_log_file_lines = Paginator(
        log_file_lines_filtered, LOG_FILES_PAGINATE_LINES)

    try:
        paginated_lines = pag_log_file_lines.page(page)
    except EmptyPage:
        paginated_lines = pag_log_file_lines.page(pag_log_file_lines.num_pages)

    header_list = manager.compile_header_from_regexp(file[1])
    context = {
        'header_list': header_list,
        'file_name': filename,
        'file_id': logfile_id,
        'paginator': paginated_lines,
        'page': page,
        'user': request.user
    }
    return render_to_response(template_name, context,
                              context_instance=RequestContext(request))


@login_required
@user_passes_test(lambda u: u.is_staff)
def logfile_to_csv(request, logfile_id):
    """
    Exports selected log file to CSV
    """
    manager = LogFilesManager()
    files_list = manager.list_logfiles(LOG_FILES_DIR)
    try:
        filename = files_list[int(logfile_id)]
    except Exception:
        return HttpResponseBadRequest()
    logfile = os.path.join(LOG_FILES_DIR, files_list[int(logfile_id)])
    file_dict = manager.parse_log_file(logfile, 0, full=True)
    # Constructing CSV file
    header_list = manager.compile_header_from_regexp()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % filename
    writer = csv.writer(response)
    if header_list:
        writer.writerow(header_list)
    if file_dict:
        for item in file_dict:
            row_list = []
            for cell in item:
                row_list += [unicode(cell).encode('utf8'), ]
            writer.writerow(row_list)
    return response
