
import os
from multiprocessing import Pool
import csv
import subprocess
import time

subDirectoryList = []
output_dir = ""
mirror_dir = ""
copy_or_csv = ""
filename = ""
filepath = ""

def get_immediate_subdirectories():
    output = []
    print("mirror directory is " + mirror_dir)
    listdir = os.listdir(mirror_dir)
    for item in listdir:
        if os.path.isdir(os.path.join(mirror_dir, item)):
            output.append(os.path.join(mirror_dir, item))
    return output


def walk_directory(mirror_directory):
    listy = []
    walk = os.walk(mirror_directory)
    if os.listdir(mirror_directory) == []:  # if there is nothing in the directory given by dirname
        listy.append((mirror_directory, ""))
    for roots, dirs, files in walk:
        for file in files:
            path = os.path.join(roots, file)
            listy.append((path, file))
    return listy


def mirror_files(lst):
    for tup in lst:
        filepath = tup[0]
        base_name = os.path.basename(filepath)
        drive, localdir = os.path.splitdrive(filepath)
        localdir = os.path.normpath(os.path.dirname(localdir).replace(mirror_dir, "")).lstrip(r"\\").lstrip("/")
        savepath = os.path.join(output_dir,os.path.basename(mirror_dir),localdir)
        try:
            with open(savepath):
                pass
        except IOError:
            if not os.path.exists(savepath):
                os.makedirs(savepath)
            pathBefore = os.getcwd()
            os.chdir(savepath)
            try:
                subprocess.call(['touch', base_name])
            except WindowsError:
                open(base_name, 'a').close()
            os.chdir(pathBefore)

def copy_to_csv(lst, filepath):
    with open(filepath, 'wt') as fileW:
        writer = csv.writer(fileW)
        writer.writerow(["full path", "file name"])
        for item in lst:
            for x in item:
                writer.writerow(x)
    fileW.close()

def get_filepath(filename):
    if not filename.endswith(".csv"):
        filename = filename + ".csv"
    filepath = output_dir + "/" + filename
    return filepath

def get_output_dir():
    with open('output_dir.txt', 'rt') as fileR1:
        output_dir = fileR1.read();
    fileR1.close()
    os.remove('output_dir.txt')
    return output_dir

def get_mirror_dir():
    with open('mirror_dir.txt', 'rt') as fileR2:
        mirror_dir = fileR2.read();
    fileR2.close()
    os.remove('mirror_dir.txt')
    return mirror_dir

def get_copy_or_csv():
    with open('copy_or_csv.txt', 'rt') as fileR3:
        copy_or_csv = fileR3.read();
    fileR3.close()
    os.remove('copy_or_csv.txt')
    return copy_or_csv

def get_filename():
    with open('filename.txt', 'rt') as fileR4:
        filename = fileR4.read();
    fileR4.close()
    os.remove('filename.txt')
    return filename


if __name__=="__main__":

    start_time = time.time()

    output_dir = get_output_dir()
    print("output dir " + output_dir)
    mirror_dir = get_mirror_dir()
    print("mirror_dir " + mirror_dir)
    copy_or_csv = get_copy_or_csv()
    print("copy_or_csv " + copy_or_csv)
    filename = get_filename()
    print("filename " + filename)

    subDirectoryList = get_immediate_subdirectories()

    pool = Pool(processes=len(subDirectoryList))
    listthing = pool.map(walk_directory, subDirectoryList)
    newList = []

    for x in listthing:
        newList.append(x)

    if copy_or_csv == "copy":
        pool.map(mirror_files, newList)
    elif copy_or_csv == "csv":
        filepath = get_filepath(filename)
        print("filepath " + filepath)
        copy_to_csv(newList, filepath)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Successfully mirrored!")
    print("Total time: " + str(elapsed_time))
