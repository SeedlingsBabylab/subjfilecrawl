'''
Created on Jan 20, 2017

@author: nicky
'''
try:
    import Tkinter as tk  # for python2
    import tkFileDialog as tkfiledialog
    import tkMessageBox
    import ttk
except ImportError:
    import tkinter as tk  # for python3
    import tkinter.filedialog as tkfiledialog
    import tkinter.messagebox as tkMessageBox
    from tkinter import ttk
import os, subprocess, re, csv
import time
from os.path import join, getsize
from math import trunc
from multiprocessing import Pool

class mirror_directory(object):
    is_time_to_mirror = False
    listy = []
    subDirectoryList = []
    '''
    classdocs
    '''
    def __init__(self, master):
        '''
        Constructor
        '''
        self.start=0
        self.lst = []
        self.init_gui_mirror(master)

    def init_gui_mirror(self, master):
        self.master = master
        master.title("Mirror directory")
        # close button
        self.close_button = tk.Button(master, text="close", command = lambda: master.destroy())
        self.close_button.pack(side=tk.BOTTOM)
        # label for mirror directory
        self.mirror_dir = os.getcwd()
        mirrorDirLabel = tk.Label(master, text="Mirror this directory:")
        mirrorDirLabel.pack(anchor="w")
        self.current_mirror_dir = tk.Label(master, bg="white", text = self.mirror_dir)
        self.current_mirror_dir.pack(anchor="w", padx=5)
        #browser to choose mirror directory
        self.choose_mirror_directory_button = tk.Button(master, text="Browse", command=lambda: self.choose_directory("mirror"))
        self.choose_mirror_directory_button.pack(anchor="center", pady=(0,10))
        self.mirror_dir_opt = options = {}
        options["initialdir"] = os.getcwd()
        options["mustexist"] = True
        # label for output directory
        self.output_dir = os.getcwd()
        outputDirLabel = tk.Label(master, text="Output directory:")
        outputDirLabel.pack(anchor="w")
        self.current_output_dir = tk.Label(master, bg="white", text=self.output_dir)
        self.current_output_dir.pack(anchor="w", padx=5)
        # browser to choose output directory
        self.choose_output_directory_button = tk.Button(master, text="Browse", command=lambda: self.choose_directory("output"))
        self.choose_output_directory_button.pack(anchor='center', pady=(0,10))
        self.output_dir_opt = options
        # choose to save as csv or copy files to directory
        self.copy_or_csv = tk.StringVar()
        self.saveLabel = tk.Label(master, text="What do you want to do with these files?")
        self.saveLabel.pack(anchor='w')
        self.filename = tk.Entry(master)
        self.copy_files_radio = tk.Radiobutton(master, text="copy files to output directory", variable=self.copy_or_csv, value="copy", command=self.disableEntry)
        self.copy_files_radio.pack(anchor="w", padx=(20, 0))
        self.save_as_CSV_radio = tk.Radiobutton(master, text="save as CSV of all filepaths in output directory.\n File name:", variable=self.copy_or_csv,value="csv", command=self.enableEntry, justify="left")
        self.save_as_CSV_radio.pack(anchor="w", padx=(20,0))
        self.filename.pack(anchor="w", padx=(48, 0), pady=(0,10))
        self.copy_files_radio.invoke()
        # start process
        self.start_button = tk.Button(master, text="start", command = lambda: self.call_mirror_functions())
        self.start_button.pack(side=tk.BOTTOM, pady=(10,0))


    def enableEntry(self):
        self.copy_or_csv.set("csv")
        self.filename.configure(state="normal")
        self.filename.update()

    def disableEntry(self):
        self.copy_or_csv.set("copy")
        self.filename.configure(state="disabled")
        self.filename.update()

    def write_copy_or_csv(self):
        with open('copy_or_csv.txt', 'w') as fileW:
            fileW.write(self.copy_or_csv.get())
        fileW.close()

    def write_filename(self):
        with open('filename.txt', 'w') as fileW:
            fileW.write(self.filename.get())
        fileW.close()

    def call_mirror_functions(self):
        self.write_filename()
        self.write_copy_or_csv()
        if not self.filename.get()and self.copy_or_csv.get()=='csv':
            tkMessageBox.showinfo("Error", "You must provide a name for your file!")
            return
        subprocess.call(['python3', os.path.join('mirror_script','mirror_functions2.py')])

    def choose_directory(self, dir_type):
        if dir_type == "output":
            # save the output directory
            self.output_dir =  tkfiledialog.askdirectory(**self.output_dir_opt)
            # update the GUI to reflect the change
            self.current_output_dir["text"] = self.output_dir
            with open('output_dir.txt', 'w') as fileW1:
                fileW1.write(self.output_dir)
            fileW1.close()
        else:
            # save the mirror directory
            self.mirror_dir = tkfiledialog.askdirectory(**self.mirror_dir_opt)
            # update the GUI to reflect the change
            self.current_mirror_dir["text"] = self.mirror_dir
            with open('mirror_dir.txt', 'w') as fileW2:
                fileW2.write(self.mirror_dir)
            fileW2.close()


if __name__=="__main__":
    root = tk.Tk()
    my_gui = mirror_directory(root)
    root.mainloop()
