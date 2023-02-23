import shutil
import glob
from random import randint
import threading
from time import sleep
import logging
import os
from os import walk
import concurrent.futures

path = r'C:/Users/Zhanna/Desktop/HomeWork_3.2/'

def get_list_files(path_to_derectory):
    list_files = []
    for (path_to_derectory, dir_names, file_names) in walk(path):
        list_files.extend(file_names)
    #print(list_files)
    return list_files

def get_directory_by_extension(list_files):
    list_extension = []
    for file in list_files:
        list_extension.append(file.split('.')[-1])
    return set(list_extension)

def create_directory_by_extension(list):
    for extension in list:
        try: 
            os.mkdir(extension) 
        except OSError as error: 
            #print(error)
            pass

def move_files_to_directory(extensions, number_of_files):
    for extension in extensions:
        files = glob.glob(os.path.join(path, f"*.{extension}"))
        #print(f"[*] Найдено {len(files)} файлов с {extension} расширением")


        threads = list()
        for file in files:
            basename = os.path.basename(file)
            dst = os.path.join(path, extension, basename)
            #print(f"[*] перемещение  {file} в {dst}")
            #shutil.move(file, dst)
            logging.info("Main    : Create and start thread %d.", files.index(file))
            thrd = threading.Thread(target=shutil.move, args=(file, dst))
            threads.append(thrd)
            thrd.start()
            
        for index, thread in enumerate(threads):
            logging.info("Main    : Before joining thread %d.", index)
            thread.join()
            logging.info("Main    : Thread %d done", index)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    list_files = get_list_files(path)
    #print(list_files)
    list_extension = get_directory_by_extension(list_files)
    list_extension.remove("py") # filter .py files
    #print(list_extension)
    create_directory_by_extension(list_extension)
    move_files_to_directory(list_extension, len(list_files))