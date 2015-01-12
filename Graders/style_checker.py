#!/usr/bin/env python
'''
<header information>

Author: Alexander Roth
UNI:    air2112
Date:   2014-12-21
'''
import re
import os
import sys
import time

WS_OP_REGEX = re.compile('\\s[-+/%<=>*!]+\\s')
NO_WS_OP_REGEX = re.compile('[^\\s][-+/%<=>*!]+[^\\s]')
EXCESS_WS_OP_REGEX = re.compile('[\\s]{2,}[-+/%<=>*!]+[\\s]')
ANY_STRING_REGEX = re.compile('.+\n')
NEWLINE_REGEX = re.compile('^\n$')
COMMENT_REGEX = re.compile('^.*#\\s.+')


class Checker(object):

    def __init__(self, line_list):
        self.line_list = line_list
        self.errs = Report()
        self.msgs = Report()

    def addMsg(self, msg):
        pass


class Report(object):

    def __init__(self):
        self.msgs = []


def main(filename):
    file_list = readlines(filename)
    errs = []
    msgs = []
    detect_header(file_list, errs, msgs)
    detect_imports(file_list, errs, msgs)
    detect_whitespace(file_list, errs, msgs)
    detect_docstrings(file_list, errs, msgs)
    detect_line_length(file_list, errs, msgs)
    detect_comments(file_list, errs, msgs)
    detect_indentation(file_list, errs, msgs)
    print_errors(errs)
    print_std(msgs)


def readlines(filename):
    open_file = open(filename, 'r')
    file_list = open_file.readlines()
    open_file.close()
    return file_list


def detect_header(file_list, errs, msgs):
    header_end = 0

    for i in range(len(file_list)):
        if '#' not in file_list[i]:
            header_end = i + 1
            break

    if header_end == 1:
        err_no_header(errs)
    else:
        msg_header_len(msgs, header_end)


def err_no_header(errs):
    errs.append('HEADER: No header detected')


def msg_header_len(msgs, index):
    msgs.append('HEADER: Header length: %d lines' % index)


def detect_imports(file_list, errs, msgs):
    for i in range(len(file_list)):
        if 'import' in file_list[i]:

            origin_len = len(file_list[i])
            clean_len = len(file_list[i].lstrip())

            if line_len_not_equal(origin_len, clean_len):
                err_import_in_func(errs, i)
            else:
                msg_import_location(msgs, i)

            if i > 15:
                err_import_not_top(errs, i)


def line_len_not_equal(source_len, target_len):
    return source_len - target_len != 0


def err_import_in_func(errs, index):
    errs.append('IMPORT: Import statement possibly inside '
                'function on line %d' % (index + 1))


def msg_import_location(msgs, index):
    msgs.append('IMPORT: Import statement found on line %d' % (index + 1))


def err_import_not_top(errs, index):
    errs.append('IMPORT: WARNING: Import statement found '
                'on line %d, not top of file.' % (index + 1))


def detect_whitespace(file_list, errs, msgs):
    detect_ws_in_op(file_list, errs, msgs)
    detect_nl_in_func(file_list, errs, msgs)
    detect_nls_between_func(file_list, errs, msgs)


def detect_ws_in_op(file_list, errs, msgs):
    ws_total = 0
    no_ws_total = 0
    excess_ws_total = 0

    for i in range(len(file_list)):
        ws_matches = re.findall(WS_OP_REGEX, file_list[i])
        no_ws_matches = re.findall(NO_WS_OP_REGEX, file_list[i])
        excess_ws_matches = re.findall(EXCESS_WS_OP_REGEX, file_list[i])

        if (len(no_ws_matches)):
            no_ws_total += len(no_ws_matches)

        if (len(excess_ws_matches)):
            excess_ws_total += len(excess_ws_matches)

        if (len(ws_matches)):
            ws_total += len(ws_matches)

    err_no_ws_op(errs, no_ws_total) if no_ws_total else False
    err_excess_ws_op(errs, excess_ws_total) if excess_ws_total else False
    msgs_good_ws_op(msgs, ws_total) if ws_total else False


def err_no_ws_op(errs, total):
    errs.append('WHITESPACE: No whitespace found around '
                '%d operators in file' % (total))


def err_excess_ws_op(errs, total):
    errs.append('WHITESPACE: Excess whitespace found around '
                '%d operators in file' % (total))


def msgs_good_ws_op(msgs, total):
    msgs.append('WHITESPACE: Whitespace found around '
                '%d operators in file' % (total))


def detect_nl_in_func(file_list, errs, msgs):
    count = 0
    for i in range(len(file_list)):
        if is_just_nl(file_list[i]) and in_between_block(file_list, i):
            count += 1

    if count == 0:
        err_no_nl_logic(errs)
    else:
        msg_nl_logic(msgs, count)


def is_just_nl(line):
    return NEWLINE_REGEX.match(line)


def in_between_block(line_list, index):
    return (next_to_block(line_list[index - 1])
            and next_to_block(line_list[index + 1]))


def next_to_block(line):
    return ANY_STRING_REGEX.match(line)


def msg_nl_logic(msgs, total):
    msgs.append('WHITESPACE: Newlines possibly found '
                'inside %d function(s).' % (total))


def err_no_nl_logic(errs):
    errs.append('WHITESPACE: No newlines found within functions')


def detect_nls_between_func(file_list, errs, msgs):
    count = 0
    for i in range(len(file_list)):
        if (is_just_nl(file_list[i]) and
                is_just_nl(file_list[i - 1]) and
                is_func(file_list[i + 1])):
            count += 1

    if count == 0:
        err_no_nls_func(errs)
    else:
        msg_nls_func(msgs, count)


def is_func(line):
    return 'def' in line


def msg_nls_func(msgs, total):
    msgs.append('WHITESPACE: Newlines possibly found '
                'between %d function(s)' % (total))


def err_no_nls_func(errs):
    errs.append('WHITESPACE: No newlines found between functions')


def detect_docstrings(file_list, errs, msgs):
    pass


def detect_line_length(file_list, errs, msgs):
    count = 0
    for line in file_list:
        if len(line) > 79:
            count += 1

    if count:
        err_over_79_chars(errs, count)
    else:
        msg_no_79_chars(msgs)


def err_over_79_chars(errs, total):
    errs.append('LINE LENGTH: %d line(s) over 79 chars in length' % (total))


def msg_no_79_chars(msgs):
    msgs.append('LINE LENGTH: No lines over 79 chars in length')


def detect_comments(file_list, errs, msgs):
    count = 0
    for line in file_list:
        if COMMENT_REGEX.match(line):
            count += 1

    if count:
        msg_comments(msgs, count)
    else:
        err_no_comments(errs)


def msg_comments(msgs, count):
    msgs.append('COMMENTS: %d comments detected in program' % count)


def err_no_comments(errs):
    errs.append('COMMENTS: No comments detected in program')


def detect_indentation(file_list, errs, msgs):
    incorrect_count = 0
    for line in file_list:
        if not is_just_nl(line):
            indent_diff = get_indentation_difference(line)

            if indent_diff and indent_diff % 4:
                incorrect_count += 1

    if incorrect_count:
        err_incorrect_indentation(errs, incorrect_count)
    else:
        msg_correct_indentation(msgs)


def get_indentation_difference(line):
    origin_line = len(line)
    clean_line = len(line.lstrip())
    indent_diff = origin_line - clean_line
    return indent_diff


def err_incorrect_indentation(errs, total):
    errs.append('INDENTATION: Inconsistent indentation found '
                '%d times throughout file' % (total))


def msg_correct_indentation(msgs):
    msgs.append('INDENTATION: Consistent indentation throughout file')


def detect_variables(file_list, errs, msgs):
    pass


def detect_global_vars(file_list, errs, msgs):
    pass


def print_errors(errs):
    print_headers('ERRORS')

    if errs:
        print_message_list(errs)
    else:
        print 'No errors to report\n'


def print_std(msgs):
    print_headers('STATS')

    if msgs:
        print_message_list(msgs)


def print_headers(section):
    print section
    print '-' * 70


def print_message_list(msg_list):
    for i in msg_list:
        print i
    print ''


def print_arguments(program):
    print 'python %s <file>' % program


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print_arguments(sys.argv[0])
