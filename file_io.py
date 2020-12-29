"""
File I/O Service v1.0.0 by robino16
"""

import os
import os.path
import logging

log = logging.getLogger()


def write_file(filepath, lines, mode='w'):
    if not file_exist(filepath):
        log.info(f"Writing new file: {filepath}.")
        pass
    f = open(filepath, mode)
    for line in lines:
        f.write(line + "\n")
    f.close()


def append_line(filepath, line):
    append_lines(filepath, [line])


def append_lines(filepath, lines):
    write_file(filepath, lines, "a")


def write_line(filepath, line):
    write_lines(filepath, [line])


def write_lines(filepath, lines):
    write_file(filepath, lines, "w")


def read_lines_from_file(filepath):
    return open(filepath, 'r').readlines()


def file_exist(filepath):
    return os.path.isfile(filepath)


def folder_exist(path):
    return os.path.isdir(path)


def read_file(filepath):
    return open(filepath, 'r').read()


def make_dir(path):
    if not folder_exist(path):
        log.info(f"Creating new directory: {path}.")
        os.mkdir(path)
