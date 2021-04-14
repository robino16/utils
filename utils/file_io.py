import os
import os.path
import logging

log = logging.getLogger()


def write_file(path, line, mode='w'):
    f = open(path, mode)
    f.write(line)
    f.close()


def write_lines_to_file(path, lines, mode='w'):
    f = open(path, mode)
    for line in lines:
        f.write(line + "\n")
    f.close()


def append_line(path, line):
    append_lines(path, [line])


def append_lines(path, lines):
    write_lines_to_file(path, lines, "a")


def write_line(path, line):
    write_lines(path, [line])


def write_lines(path, lines):
    write_lines_to_file(path, lines, "w")


def read_lines_from_file(path):
    return open(path, 'r').readlines()


def file_exist(path):
    return os.path.isfile(path)


def folder_exist(path):
    return os.path.isdir(path)


def read_file(filepath):
    return open(filepath, 'r').read()


def make_dir(path):
    if not folder_exist(path):
        os.mkdir(path)


def save_keras_model(model, path):
    model.save(path)


def load_keras_model(path):
    from keras.models import load_model
    return load_model(path)
