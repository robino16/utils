"""
String Replace v1.0.0
by robinoms
"""

import logging
import json
import os

BANNED = '<banned>'
ROOT_DIR = '.'


class FileIO:
    @staticmethod
    def file_exist(path: str) -> bool:
        return os.path.isfile(path)

    @staticmethod
    def read_file(path: str) -> str:
        return open(path, 'r').read()

    @staticmethod
    def read_lines(path: str) -> list:
        return open(path, 'r').readlines()

    @staticmethod
    def write_lines(path: str, lines: list, mode='w') -> None:
        with open(path, mode) as file:
            for line in lines:
                file.write(line + '\n')

    @staticmethod
    def write_line(path: str, line: str) -> None:
        FileIO.write_lines(path, [line])


class AppConfig:
    def __init__(self, json_dict=None) -> None:
        self.search_directory = ROOT_DIR
        self.string_to_replace = BANNED
        self.string_to_replace_with = BANNED
        self.file_types = ['.h', '.c', '.py', '.md']

        self.log_level = logging.INFO
        self.log_output_file = 'srv2.log'
        if json_dict:
            vars(self).update(json_dict)

    def to_json(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


def save_app_config(config: AppConfig, path: str) -> None:
    FileIO.write_line(path, config.to_json())


def load_app_config(path: str) -> AppConfig:
    if FileIO.file_exist(path):
        config = json.loads(FileIO.read_file(path), object_hook=AppConfig)
    else:
        config = AppConfig(None)
        save_app_config(config, path)
    return config


# global parameters
CONF_FILE = 'srv2.conf'
CONF = load_app_config(CONF_FILE)
logging.basicConfig(level=CONF.log_level, 
                    handlers=[logging.FileHandler(CONF.log_output_file), logging.StreamHandler()])
LOG = logging.getLogger()


def get_user_input(prompt: str = '') -> str:
    return input(prompt).replace('\n', '')


def get_generic(value: str, default: str = BANNED) -> str:
    while True:
        print(f'please specify your {value}:')
        if default is not BANNED:
            print(f'(press enter to use: \'{default}\')')
        usr = get_user_input()
        if usr == '':
            if default is not BANNED:
                return default
            else:
                LOG.error('invalid/banned value')
                continue
        return usr


def set_search_dir() -> None:
    CONF.search_directory = get_generic('search directory', CONF.search_directory)


def set_search_string():
    CONF.string_to_replace = get_generic('string to replace', CONF.string_to_replace)


def set_replacement_string():
    CONF.string_to_replace_with = get_generic('replacement string', CONF.string_to_replace_with)


def set_file_types():
    print(f'\nplease specify your file types (separated with comma):')
    print(f'(press enter to use: \'{CONF.file_types}\')')
    usr = get_user_input()
    if usr != '':
        CONF.file_types = usr.split(',')


def main():
    print('~ STRING SEARCH AND REPLACE ~')

    set_search_dir()
    set_search_string()
    set_replacement_string()
    set_file_types()

    save_app_config(CONF, CONF_FILE)

    count_occurances = 0
    count_replacements = 0
    count_modified = 0
    count_files = 0

    print(f'press enter to accept incoming changes\ntype \'s\' to skip\ntype \'a\' to accept all in current file\n')
    print('searching...')
    for subdir, dirs, files in os.walk(CONF.search_directory):
        for file in files:
            filepath = subdir + os.sep + file
            count_files += 1
            # print(f'    file {count_files}/{len(files)}: {file}')
            is_correct_file_type = False
            for file_type in CONF.file_types:
                if filepath.endswith(file_type):
                    is_correct_file_type = True
            if not is_correct_file_type:
                continue
            try:
                file_modified = False
                count_occurances_in_file = 0
                count_changes_in_file = 0
                new_lines = []
                line_number = 0
                lines = FileIO.read_lines(filepath)
                accept_all = False

                for line in lines:
                    line_number += 1
                    old = line.replace('\n', '')
                    if old.find(CONF.string_to_replace) != -1:
                        
                        new = old.replace(CONF.string_to_replace, CONF.string_to_replace_with)

                        if count_occurances_in_file == 0:
                            print(f'\n\n    {file}')
                            print('    ' + ''.join(['~' for _ in range(34)]))
                            print(f'    found \'{CONF.string_to_replace}\'')
                            print(f'    in file \'{filepath}\'')

                        count_occurances += 1
                        count_occurances_in_file += 1
                        print(f'\n        occurance #{count_occurances_in_file}')
                        print('        ' + ''.join(['~' for _ in range(30)]))
                        print(f'        line #{line_number}:\t"{old}\"')
                        print(f'              -> \t\"{new}\"')
                        while True:
                            usr = '' if accept_all else get_user_input()
                            if usr == 's':
                                new_lines.append(old)
                                print(f'             \t\tREJECTED')
                                break
                            elif usr == 'a':
                                accept_all = True
                                usr = ''
                            if usr == '':
                                new_lines.append(new)
                                count_replacements += 1
                                count_changes_in_file += 1
                                file_modified = True
                                print(f'             \t\tACCEPTED')
                                break
                            LOG.error('invalid user input')
                    else:
                        new_lines.append(old)
                if file_modified:
                    remaining = count_occurances_in_file - count_changes_in_file
                    print(f'\n    APPLIED {count_changes_in_file} CHANGES TO FILE \'{filepath}\'')
                    if remaining == 0:
                        print(f'    poof! {CONF.string_to_replace} was removed from file')
                    else:
                        print(f'    oops! {remaining} remnants of {CONF.string_to_replace} still remains...')
                    print('    ' + ''.join(['_' for _ in range(34)]) + '\n')
                    count_modified += 1
                    FileIO.write_lines(filepath, new_lines)
            except Exception as e:
                LOG.error("Could not read file: {}:\n{}".format(filepath, e))
    print(f'\n{count_modified} files ({count_replacements} lines) changed')
    remaining = count_occurances - count_replacements
    if count_occurances == 0:
        print(f'did not find any {CONF.string_to_replace}s')
    elif remaining == 0:
        print(f'poof! \'{CONF.string_to_replace}\' has been completely erased')
    else:
        print(f'oops! {remaining} occurances of {CONF.string_to_replace} may still remain...')


if __name__ == '__main__':
    main()
