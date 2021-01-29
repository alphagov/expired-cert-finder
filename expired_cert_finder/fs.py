from os import walk
from os.path import isdir, isfile

def find_files(path, spinner_func=None):
    files = []

    if isfile(path):
        files.append(path)
        if spinner_func:
            spinner_func()
    for dir_name, subdir_list, file_list in walk(path):
        for file_name in file_list:
            if spinner_func:
                spinner_func()
            delimeter = '/' if dir_name != './' else ''
            file_path = ('%s%s%s' % (dir_name, delimeter, file_name))
            files.append(file_path)

    return files

