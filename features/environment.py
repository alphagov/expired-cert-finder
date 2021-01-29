from glob import glob
from shutil import copy

from os import mkdir, rmdir, remove, system
from os.path import exists


DEBUG = False

WORK_DIR = './work'

def before_all(context):
    if DEBUG:
        print("BEFORE_ALL")

    system("pip install -r requirements.txt")

    if exists(WORK_DIR):
        clean_dir()
        rmdir(WORK_DIR)
    mkdir(WORK_DIR)


def before_scenario(context, step):
    if DEBUG:
        print("BEFORE_SCENARIO")

    clean_dir()
    

def clean_dir():
    if DEBUG:
        print("CLEAN_DIR")
        
    for file in glob(WORK_DIR + '/*'):
        remove(file)