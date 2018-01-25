try:
   import cPickle as pickle
except:
   import pickle
try:
    import Tkinter as tk  # for python2
    import tkFileDialog as tkfiledialog
    import tkMessageBox
except ImportError:
    import tkinter as tk  # for python3
    import tkinter.filedialog as tkfiledialog
    import tkinter.messagebox as tkMessageBox
import csv
import os
import re
import shutil
import subprocess
import time
import sys
crawl_files_list = []

def crawl_files(obj):
    #self.start_button.config(state="disable")
    global crawl_files_list
    crawl_files_list = []
    if len(obj.checked_boxes)==0:
        tkMessageBox.showinfo("Error", "You must select some file types!")
        #obj.file_type_chooser()
        return
    if obj.recurse_or_scan:
        if not obj.crawl_dir.endswith('.csv'):
            tkMessageBox.showinfo("Error", "You must provide a csv file to scan or uncheck the top box.")
            return
        crawl_files_from_csv(obj, obj.crawl_dir)
    else:
        if not os.path.isdir(obj.crawl_dir):
            tkMessageBox.showinfo("Error", "You must provide a directory to crawl.")
            return
        crawl_files_recursive(obj, obj.crawl_dir)

def crawl_files_from_csv(obj, filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=',', )
        next(reader, None)
        for row in reader:
            # filtering by month
            m = re.search(r'[0-9]{2}_[0-9]{2}/', row[0])
            if re.search(r'[0-9]{2}_[0-9]{2}/', row[0]):
                splt = m.group(0).split("_")
                month = int(splt[1].strip('/'))
                if month > int(obj.end_month_var) or month < int(obj.start_month_var):
                    continue
            # filtering by subject
            n = re.search(r'[0-9]{2}_[0-9]{2}-[0-9]{2}-[0-9]{4}', row[0])
            if re.search(r'[0-9]{2}_[0-9]{2}-[0-9]{2}-[0-9]{4}', row[0]):
                splt = n.group(0).split("_")
                subject = int(splt[0])
                if subject not in obj.chosen_subjects:
                    continue
            update_tups(row[0], row[1])
        # once done
        if obj.copy_or_csv=="copy":
            copy_files(obj)
        else:
            copy_to_csv(obj)


def crawl_files_recursive(obj, dirname):
    # if the save file name is empty and you want a csv
    if not obj.filename and obj.copy_or_csv=="csv":
        tkMessageBox.showinfo("Error", "You must provide a name for your file!")
        return
    # for each item in this directory
    try:
        for sub in os.listdir(dirname):
            path = os.path.join(dirname, sub)
            # if the current item is a directory, recurse
            if os.path.isdir(path):
                # only recurse into dirs that lie within specified month ranges
                if re.match(r'[0-9]{2}_[0-9]{2}$', sub):
                    splt = sub.split("_")
                    month = int(splt[1])
                    if month > int(obj.end_month_var or month < int(obj.start_month_var)):
                        continue
                if re.search(r'[0-9]{2}_[0-9]{2}-[0-9]{2}-[0-9]{4}', sub):
                    splt = sub.split("_")
                    subject = int(splt[0])
                    if subject not in obj.chosen_subjects:
                        continue
                crawl_files_recursive(obj, path)
            # else, here's a file to check
            else:
                #self.tups.append((str(path), str(sub)))
                # add file paths to tups if it fits criteria
                update_tups(obj, path, sub)
    # this only happens if we don't have permissions to files
    except OSError as e:
        print(e)
    # once all of the items in the top level directory have been searched, we're done
    if dirname==obj.crawl_dir:
        if obj.copy_or_csv=="copy":
            copy_files(obj)
        else:
            copy_to_csv(obj)

def copy_to_csv(obj):
    global crawl_files_list
    if len(crawl_files_list)==0:
        tkMessageBox.showinfo("Error", "No files of the selected type exist in your chosen directory!")
        return
    x = obj.filename.strip()
    if not re.match("(.csv)$", obj.filename):
        x+=".csv"
    with open(obj.output_dir+'/'+x, 'a+') as f:
        writer = csv.writer(f)
        writer.writerow(["full path", "file name"])
        for item in crawl_files_list:
            writer.writerow(item)
    tkMessageBox.showinfo("Completed", "Directory successfully copied to csv!")

def copy_files(obj):
    global crawl_files_list
    if len(crawl_files_list)==0:
        tkMessageBox.showinfo("Error", "No files of the selected type exist in your chosen directory!")
        return
    if obj.dump_or_keep:
        for tup in crawl_files_list:
            filepath = tup[0]
            savepath = obj.output_dir
            shutil.copy(filepath, savepath)
    else:
        for tup in crawl_files_list:
            filepath = tup[0]
            drive, localdir = os.path.splitdrive(filepath)
            localdir = os.path.normpath(os.path.dirname(localdir).replace(obj.crawl_dir, "")).lstrip(r"\\").lstrip("/")
            savepath = os.path.join(obj.output_dir,os.path.basename(obj.crawl_dir),localdir)
            try:
                with open(savepath) as f: pass
            except IOError as e:
                if not os.path.exists(savepath):
                    os.makedirs(savepath)
                shutil.copy(filepath, savepath)
    tkMessageBox.showinfo("Completed", "Directory successfully copied!")

def update_tups(obj, path, sub):
    global crawl_files_list
    if "audio_basic" in obj.checked_boxes:
        if os.path.dirname(path).endswith('Audio_Analysis'):
            if re.search(r'sparse_code.csv$', sub):
                crawl_files_list.append((str(path), str(sub)))
    if "video_basic" in obj.checked_boxes:
        if os.path.dirname(path).endswith('Video_Analysis'):
            if re.search(r'sparse_code.csv$', sub):
                crawl_files_list.append((str(path), str(sub)))
    if "silences" in obj.checked_boxes:
        if re.search(r'silences\.txt$', sub):
            crawl_files_list.append((str(path), str(sub)))
    if "lena5min" in obj.checked_boxes:
        if re.search(r'lena5min\.csv$', sub):
            crawl_files_list.append((str(path), str(sub)))
    if "video_mp4" in obj.checked_boxes:
        if re.search(r'\.mp4$', sub):
            crawl_files_list.append((str(path), str(sub)))
    if "audio_clan" in obj.checked_boxes:
        if obj.audio_clan=='final':
            if os.path.dirname(path).endswith('Audio_Annotation'):
                if re.search(r'(cex|cha)$', sub):
                    crawl_files_list.append((str(path), str(sub)))
        if obj.audio_clan=="newclan_merged_final":
            if re.search(r'newclan_merged_final\.(cex|cha)$', sub):
                crawl_files_list.append((str(path), str(sub)))
        if obj.audio_clan=='newclan_merged':
            if re.search(r'newclan_merged\.(cex|cha)$', sub):
                crawl_files_list.append((str(path), str(sub)))
        if obj.audio_clan=='silences':
            if re.search(r'silences.*(cex|cha)$', sub):
                crawl_files_list.append((str(path), str(sub)))
    if "video_datavyu" in obj.checked_boxes:
        if obj.video_datavyu=='final':
            if re.search(r'final\.(opf)$', sub):
                crawl_files_list.append((str(path), str(sub)))
        if obj.video_datavyu=='consensus':
            if re.search(r'consensus\.(opf)$', sub):
                crawl_files_list.append((str(path), str(sub)))
    if "audio_wav" in obj.checked_boxes:
        if obj.audio_wav=='scrubbed':
            if re.search(r'scrubbed.*wav$', sub):
                crawl_files_list.append((str(path), str(sub)))
        if obj.audio_wav=='unscrubbed':
            if re.search(r'\.wav$', sub) and "scrubbed" not in sub:
                crawl_files_list.append((str(path), str(sub)))
    if "custom_regex" in obj.checked_boxes:
        if re.search(obj.custom_regex, sub):
            crawl_files_list.append((str(path), str(sub)))
class fake_object:
    def __init__(self, box, cdir, endm, startm, chosub, c_csv, filen, outdir, a_clan, v_data, a_wav, custom, r_scan, d_keep):
        self.checked_boxes = box
        self.crawl_dir = cdir
        self.end_month_var = endm
        self.start_month_var = startm
        self.chosen_subjects = chosub
        self.copy_or_csv = c_csv
        self.filename = filen
        self.output_dir = outdir
        self.audio_clan = a_clan
        self.video_datavyu = v_data
        self.audio_wav = a_wav
        self.custom_regex = custom
        self.recurse_or_scan = r_scan
        self.dump_or_keep = d_keep

if __name__=="__main__":

    start_time = time.time()

    #crawl or copy, directory, dump or keep(startmonth), crawl_dir(endmonth), list of file(subject),

    objs = sys.argv[1]
    obj = pickle.loads(objs)

    crawl_files(obj)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Successfully mirrored!")
    print("Total time: " + str(elapsed_time))
