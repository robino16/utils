import os
import os.path


class FileIO:
    @staticmethod
    def write_file(path, line, mode='w'):
        f = open(path, mode)
        f.write(line)
        f.close()

    @staticmethod
    def write_lines_to_file(path, lines, mode='w'):
        f = open(path, mode)
        for line in lines:
            f.write(line + "\n")
        f.close()

    @staticmethod
    def append_line(path, line):
        FileIO.append_lines(path, [line])

    @staticmethod
    def append_lines(path, lines):
        FileIO.write_lines_to_file(path, lines, "a")

    @staticmethod
    def write_line(path, line):
        FileIO.write_lines(path, [line])

    @staticmethod
    def write_lines(path, lines):
        FileIO.write_lines_to_file(path, lines, "w")

    @staticmethod
    def read_lines(path):
        return open(path, 'r').readlines()

    @staticmethod
    def file_exist(path):
        return os.path.isfile(path)

    @staticmethod
    def folder_exist(path):
        return os.path.isdir(path)

    @staticmethod
    def read_file(path):
        return open(path, 'r').read()

    @staticmethod
    def make_dir(path):
        if not FileIO.folder_exist(path):
            os.mkdir(path)

    @staticmethod
    def save_keras_model(model, path):
        model.save(path)

    @staticmethod
    def load_keras_model(path):
        from keras.models import load_model
        return load_model(path)
