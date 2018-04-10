"""
Logging reader
"""
import os
import re

from django.db import models

from .settings import *


class LogFilesManager(object):

    def list_logfiles(self, path):
        """
        Returns  list of log files
        """
        file_list = []
        for f in EXTRA_LOGS:
            path_file = f[0]
            # List only readable files
            if os.path.isfile(path_file) and path_file.endswith('.log'):
                try:
                    fi = open(path_file)
                    fi.close()
                    file_list.append(f)
                except Exception:
                    pass
        return file_list

    def get_file(self, file_full_path):
        fobj = open(file_full_path, 'rb')
        return fobj

    def get_file_lines_count(self, file_obj):
        """
        Creates fake log file list (without real lines,
        but with proper length)
        """
        fake_log_file = []
        log_file_fake_lines = file_obj.xreadlines()
        count = 0
        for line in log_file_fake_lines:
            fake_log_file.append(count)
            count += 1
        if fake_log_file:
            fake_log_file.append(count)
        return fake_log_file

    def compile_re_index(self, regexp=None):
        """
        Creating Regexp prog to match entries
        """
        if not regexp:
            regexp = LOG_FILES_RE
        prog = re.compile(regexp)
        return prog

    def parse_log_file(self, logfile, regexp, from_line=0,
                       to_line=LOG_FILES_PAGINATE_LINES, full=False):
        """
        Returns parsed read file

        in form of entry names header (taken from Rgex group names)
        and lines tuples list
        """
        prog = self.compile_re_index(regexp)
        # Reading amount of lines
        file_obj = self.get_file(logfile)

        text = file_obj.read()
        matches_sets = prog.findall(text)
        matches_sets.reverse()
        # return sorted(matches_sets, reverse=True)
        return matches_sets

    def compile_header_from_regexp(self, regexp=None):
        """Making logfile indexes header"""
        prog = self.compile_re_index(regexp)
        header_length = prog.groups
        header_list = []
        if prog.groupindex:
            for number in range(header_length):
                header_list.append(number)
            for group_name, index in prog.groupindex.iteritems():
                header_list[int(index) - 1] = group_name
        return header_list


class string_with_title(str):

    def __new__(cls, value, title):
        instance = str.__new__(cls, value)
        instance._title = title
        return instance

    def title(self):
        return self._title

    __copy__ = lambda self: self
    __deepcopy__ = lambda self, memodict: self


class LogFile(models.Model):

    """Hack object to be added to Django admin"""
    class Meta:
        app_label = string_with_title("django_log_file_viewer",
                                      "Django Log Files")
    verbose_name = 'Django Log File'
    verbose_name_plural = 'Django Log Files'
