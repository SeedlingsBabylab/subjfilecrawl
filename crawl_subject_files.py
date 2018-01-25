try:
    import Tkinter as tk  # for python2
    import tkFileDialog as tkfiledialog
    import tkMessageBox
except ImportError:
    import tkinter as tk  # for python3
    import tkinter.filedialog as tkfiledialog
    import tkinter.messagebox as tkMessageBox
try:
   import cPickle as pickle
except:
   import pickle
import csv
import os
import re
import shutil
import subprocess
# from pip._vendor.distlib.util import CSVWriter
import mirror_script.mirror_directory4 as mirror


debug = False

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

class crawl_subject_GUI(object):
    def __init__(self, master):
        self.start = 0
        self.checked_boxes=[]
        # list of tups that holds the path -> file structure
        self.tups = []
        self.init_gui(master)

    def init_gui(self, master):
        self.master = master
        master.title("Get subject files")
        # open up mirror directory popup
        self.mirror_button = tk.Button(master, text="Create mirror", command = lambda: self.popup_mirror())
        self.mirror_button.pack(anchor='n')
        # choose between recursing directory or scanning csv
        self.recurse_or_scan = tk.BooleanVar()
        self.recurse_or_scan_button = tk.Checkbutton(master, text='Check box to scan from csv.\n Leave empty to recurse directory.', variable=self.recurse_or_scan)
        self.recurse_or_scan_button.pack(anchor='w')
        # close button
        self.close_button = tk.Button(master, text="close", command = master.quit)
        self.close_button.pack(side=tk.BOTTOM)
        # label for crawl directory
        self.crawl_dir = os.getcwd()
        crawlDirLabel = tk.Label(master, text="Crawl directory:")
        crawlDirLabel.pack(anchor="w")
        self.current_crawl_dir = tk.Label(master, bg="white", text = self.crawl_dir)
        self.current_crawl_dir.pack(anchor="w", padx=5)
        #browser to choose crawl directory
        self.choose_crawl_directory_button = tk.Button(master, text="Browse", command=lambda: self.choose_directory("crawl"))
        self.choose_crawl_directory_button.pack(anchor="center", pady=(0,10))
        self.crawl_dir_opt = options = {}
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
        self.dump_or_keep = tk.BooleanVar()
        self.dump_or_keep_button = tk.Checkbutton(master, text='Check to dump files to output directory.\nLeave unchecked to keep directory structure.', variable=self.dump_or_keep)
        self.dump_or_keep_button.pack(anchor='w', padx=(40, 0))
        self.save_as_CSV_radio = tk.Radiobutton(master, text="save as CSV of all filepaths in output directory.\n File name:", variable=self.copy_or_csv,value="csv", command=self.enableEntry, justify="left")
        self.save_as_CSV_radio.pack(anchor="w", padx=(20,0))
        self.filename.pack(anchor="w", padx=(48, 0), pady=(0,10))
        self.copy_files_radio.invoke()
        # subject ranges
        self.choose_files_button = tk.Button(master, text="Choose file types", command = lambda:self.file_type_chooser())
        self.choose_files_button.pack(anchor='center')
        # start process
        # self.start_button = tk.Button(master, text="start", command = lambda: self.crawl_files(self.crawl_dir))
        self.start_button = tk.Button(master, text="start", command = lambda: self.multi_call())
        #self.start_button.config(state="disable")
        self.start_button.pack(side=tk.BOTTOM, pady=(10,0))

    def multi_call(self):
        #fake_obj = fake_object(self.checked_boxes, self.crawl_dir, self.end_month_var.get(), self.start_month_var.get(), self.chosen_subjects, self.copy_or_csv.get(), self.filename.get(), self.output_dir, self.audio_clan_type.get(), self.video_datavyu_type.get(), self.audio_wav_type.get(), self.custom_regex_text.get(), self.recurse_or_scan.get(), self.dump_or_keep.get())
        box = self.checked_boxes
        cdir = self.crawl_dir
        endm = self.end_month_var.get()
        startm = self.start_month_var.get()
        chosub = self.chosen_subjects
        c_csv = self.copy_or_csv.get()
        filen = self.filename.get()
        outdir = self.output_dir
        a_clan = 0
        v_data = 0
        a_wav = 0
        custom = 0
        if "audio_clan" in self.checked_boxes:
            a_clan = self.audio_clan_type.get()
        if "video_datavyu" in self.checked_boxes:
            v_data = self.video_datavyu_type.get()
        if "audio_wav" in self.checked_boxes:
            a_wav = self.audio_wav_type.get()
        if "custom_regex" in self.checked_boxes:
            custom = self.custom_regex_text.get()
        r_scan = self.recurse_or_scan.get()
        d_keep = self.dump_or_keep.get()
        fake_obj = fake_object(box, cdir, endm, startm, chosub, c_csv, filen, outdir, a_clan, v_data, a_wav, custom, r_scan, d_keep)
        subprocess.call(['python', 'crawl_function.py', pickle.dumps(fake_obj)])

    def file_type_chooser(self):
        window = tk.Toplevel(root)
        window.title("File type chooser")
        #window.overrideredirect(1)
        close = tk.Button(window, text="close", command=window.destroy)
        close.pack(side=tk.BOTTOM, pady=(10,0))
        # options for audio annotations
        self.file_options_label = tk.Label(window, text="What kinds of files do you want?")
        self.file_options_label.pack(anchor='w')
        self.audio_clan = tk.BooleanVar()
        self.clan_file_option = tk.Checkbutton(window, variable = self.audio_clan, text="Audio clan files")
        self.clan_file_option.pack(anchor='w')
        self.audio_basic = tk.BooleanVar()
        self.audio_basic_option = tk.Checkbutton(window, variable = self.audio_basic, text="Basic audio files")
        self.audio_basic_option.pack(anchor='w')
        self.video_datavyu = tk.BooleanVar()
        self.datavyu_file_option = tk.Checkbutton(window, variable = self.video_datavyu,text="Video datavyu files")
        self.datavyu_file_option.pack(anchor='w')
        self.video_basic = tk.BooleanVar()
        self.video_basic_option = tk.Checkbutton(window, variable = self.video_basic, text="Basic video files")
        self.video_basic_option.pack(anchor='w')
        self.silences=tk.BooleanVar()
        self.silences_option = tk.Checkbutton(window, variable=self.silences, text="Silence.txt files")
        self.silences_option.pack(anchor='w')
        self.lena5min = tk.BooleanVar()
        self.lena5min_option = tk.Checkbutton(window, variable=self.lena5min, text="lena5min files")
        self.lena5min_option.pack(anchor='w')
        self.video_mp4 = tk.BooleanVar()
        self.video_mp4_option = tk.Checkbutton(window, variable=self.video_mp4, text="Video mp4 files")
        self.video_mp4_option.pack(anchor='w')
        self.audio_wav = tk.BooleanVar()
        self.audio_wav_option = tk.Checkbutton(window, variable=self.audio_wav, text="Audio wav files")
        self.audio_wav_option.pack(anchor='w')
        self.custom_regex = tk.BooleanVar()
        self.custom_regex_option = tk.Checkbutton(window, variable=self.custom_regex, text="Write your own regex")
        self.custom_regex_option.pack(anchor='w')
        self.custom_regex_text = tk.Entry(window)
        self.custom_regex_text.pack(anchor="w", padx=(20, 0), pady=(0,10))
        # month ranges
        startMonthLabel = tk.Label(window, text="Start Month:")
        startMonthLabel.pack(anchor="w")
        self.start_month_var = tk.StringVar()
        self.start_month = tk.Spinbox(window, from_=6, to=18, textvariable=self.start_month_var, command=self.updateSpinbox)
        self.start_month_var.set(6)
        self.start_month.pack(anchor='w')
        endMonthLabel = tk.Label(window, text="End Month:")
        endMonthLabel.pack(anchor="w")
        self.end_month_var = tk.StringVar()
        self.end_month = tk.Spinbox(window, from_=6, to=18, textvariable=self.end_month_var, command=self.updateSpinbox)
        self.end_month_var.set(18)
        self.end_month.pack(anchor="w")
        # subject ranges
        self.chosen_subjects = range(1,47)
        self.choose_subjects = tk.Button(window, text="Choose subjects (default is all)", command = lambda:self.choose_subjects_window())
        self.choose_subjects.pack(anchor='w')
        # next button
        self.next_button = tk.Button(window, text="submit", command = self.getCheckboxVals)
        self.next_button.pack(side=tk.BOTTOM, pady=(10,0))

    def choose_subjects_window(self):
        window = tk.Toplevel(root)
        window.title("Choose subjects")
        close = tk.Button(window, text="close",command=window.destroy)
        close.pack(side=tk.BOTTOM, pady=(10,0))
        top = tk.Frame(window)
        top.pack(side=tk.BOTTOM)
        bottom = tk.Frame(window)
        bottom.pack(side=tk.BOTTOM)
        label = tk.Label(window, text="Choose subjects")
        label.pack(anchor='w', padx=(120,10), pady=(10,10))
        left_scrollbar = tk.Scrollbar(window)
        left_scrollbar.pack(in_=bottom, side='left', fill="y")
        self.listbox = tk.Listbox(window, selectmode="multiple")
        self.listbox.config(yscrollcommand=left_scrollbar.set)
        self.listbox.pack(in_=bottom,side='left')
        left_scrollbar.config(command=self.listbox.yview)
        for i in range(1,47):
            self.listbox.insert(i, i)
        update = tk.Button(window, text="update", command = lambda: self.update_subjects_chosen())
        update.pack(in_=bottom, side='left')
        self.curr_selection = tk.Listbox(window)
        self.curr_selection.pack(in_=bottom,side='left')
        right_scrollbar = tk.Scrollbar(window)
        right_scrollbar.pack(in_=bottom, side='left', fill='y')
        self.curr_selection.config(yscrollcommand=right_scrollbar.set)
        right_scrollbar.config(command=self.curr_selection.yview)
        for i in self.chosen_subjects:
            self.curr_selection.insert(i,i)

    def update_subjects_chosen(self):
        self.chosen_subjects = [x+1 for x in self.listbox.curselection()]
        self.curr_selection.delete(0, tk.END)
        for i in self.chosen_subjects:
            self.curr_selection.insert(i,i)

    def popup_mirror(self):
        window = tk.Toplevel(root)
        inst = mirror.mirror_directory(window)

    def getCheckboxVals(self):
        self.start = 1
        self.checked_boxes = []
        if (self.audio_clan.get()):
            self.checked_boxes.append("audio_clan")
        if (self.audio_basic.get()):
            self.checked_boxes.append("audio_basic")
        if (self.video_datavyu.get()):
            self.checked_boxes.append("video_datavyu")
        if (self.video_basic.get()):
            self.checked_boxes.append("video_basic")
        if (self.silences.get()):
            self.checked_boxes.append("silences")
        if (self.lena5min.get()):
            self.checked_boxes.append("lena5min")
        if (self.video_mp4.get()):
            self.checked_boxes.append("video_mp4")
        if (self.audio_wav.get()):
            self.checked_boxes.append("audio_wav")
        if (self.custom_regex.get()):
            self.checked_boxes.append("custom_regex")
        self.file_types = self.checked_boxes
        if len(self.checked_boxes) == 0:
            tkMessageBox.showinfo("Error", "You must select at least one type of file")
        else:
            for item in self.checked_boxes:
                self.create_new_window(item)
            #self.start_button.config(state="normal")
            self.getSavePath()
            self.custom_regex_text.update()
            #self.close_button.invoke()

    def updateSpinbox(self):
        start=6
        end=18
        if int(self.start_month.get()) > int(self.end_month.get()):
            self.end_month_var.set(self.start_month_var.get())

    def enableEntry(self):
        self.copy_or_csv.set("csv")
        self.filename.configure(state="normal")
        self.dump_or_keep_button.configure(state='disabled')
        self.filename.update()

    def disableEntry(self):
        self.copy_or_csv.set("copy")
        self.filename.configure(state="disabled")
        self.dump_or_keep_button.configure(state='normal')
        self.filename.update()

    def getSavePath(self):
        self.save_filename = self.filename.get()

    def choose_directory(self, dir_type):
        if dir_type=="output":
            # save the output directory
            self.output_dir =  tkfiledialog.askdirectory(**self.output_dir_opt)
            # update the GUI to reflect the change
            self.current_output_dir["text"] = self.output_dir
        else:
            if self.recurse_or_scan.get():
                # save the path to csv
                FILEOPENOPTIONS = dict(filetypes=[('CSV file','*.csv')])
                self.crawl_dir = tkfiledialog.askopenfilename(**FILEOPENOPTIONS)
            else:
                # save the crawl directory
                self.crawl_dir = tkfiledialog.askdirectory(**self.crawl_dir_opt)
            # update the GUI to reflect the change
            self.current_crawl_dir["text"] = self.crawl_dir


    def create_new_window(self, option):
        self.audio_clan_type = tk.StringVar()
        self.audio_clan_type.set("None")
        self.audio_basic_type = False
        self.video_datavyu_type = tk.StringVar()
        self.video_datavyu_type.set("None")
        self.video_basic_type = False
        self.silences_type = False
        self.lena5min_type = False
        self.video_mp4_type = False
        self.audio_wav_type = tk.StringVar()
        if option == "audio_clan":
            self.audio_clan_window()
        if option == "audio_basic":
            self.audio_basic_window()
        if option == "video_datavyu":
            self.video_datavyu_window()
        if option == "video_basic":
            self.video_basic_window()
        if option == "silences":
            self.silences_window()
        if option == "lena5min":
            self.lena5min_window()
        if option == "video_mp4":
            self.video_mp4_window()
        if option == "audio_wav":
            self.audio_wav_window()

    def audio_clan_window(self):
        window = tk.Toplevel(root)
        window.title("Audio clan options")
        #window.overrideredirect(1)
        label = tk.Label(window, text="Choose which audio clan files you want")
        label.config(font="bold")
        label.pack(anchor="w", padx=(10,10), pady=(10,10))
        silences_button = tk.Radiobutton(window, text='silences', variable=self.audio_clan_type, value='silences', command=self.audio_clan_type.set('silences'))
        newclan_merged_button = tk.Radiobutton(window, text="newclan_merged", variable=self.audio_clan_type, value="newclan_merged", command=self.audio_clan_type.set("newclan_merged"))
        final_button = tk.Radiobutton(window, text="final", variable=self.audio_clan_type, value="final", command=self.audio_clan_type.set("final"))
        newclan_merged_final_button = tk.Radiobutton(window, text="newclan_merged_final", variable = self.audio_clan_type, value="newclan_merged_final", command=self.audio_clan_type.set("newclan_merged_final"))
        final_button.pack(anchor='w')
        newclan_merged_final_button.pack(anchor='w')
        newclan_merged_button.pack(anchor='w')
        silences_button.pack(anchor='w')
        accept = tk.Button(window, text="accept",command=window.destroy)
        accept.pack(side="bottom", pady=(10,0))
        self.audio_clan_type.set("final")

    def audio_basic_window(self):
        window = tk.Toplevel(root)
        window.title("Audio basic options")
        #window.overrideredirect(1)
        accept = tk.Button(window, text="accept", command=window.destroy)
        accept.pack(side="bottom", pady=(10,0))
        label = tk.Label(window, text="sparse_code.csv files are the only option for basic audio files")
        label.config(font="bold")
        label.pack(anchor="w", padx=(10,10), pady=(10,10))
        self.audio_basic_type = True

    def video_datavyu_window(self):
        window = tk.Toplevel(root)
        window.title("Video datavyu options")
        #window.overrideredirect(1)
        accept = tk.Button(window, text="accept", command=window.destroy)
        accept.pack(side="bottom", pady=(10,0))
        label = tk.Label(window, text="Choose which datavyu files you want")
        label.config(font="bold")
        label.pack(anchor="w", padx=(10,10), pady=(10,10))
        button = tk.StringVar()
        final_button = tk.Radiobutton(window, text="final", variable=self.video_datavyu_type, value="final", command=self.video_datavyu_type.set("final"))
        final_button.pack(anchor='w')
        consensus_button = tk.Radiobutton(window, text="consensus", variable=self.video_datavyu_type, value="consensus", command=self.video_datavyu_type.set("consensus"))
        consensus_button.pack(anchor='w')
        self.video_datavyu_type.set("final")

    def video_basic_window(self):
        window = tk.Toplevel(root)
        window.title("Video basic options")
        #window.overrideredirect(1)
        accept = tk.Button(window, text="accept", command=window.destroy)
        accept.pack(side="bottom", pady=(10,0))
        label = tk.Label(window, text="sparse_code.csv files are the only option for basic video files")
        label.config(font="bold")
        label.pack(anchor="w", padx=(10,10), pady=(10,10))
        self.video_basic_type = True

    def silences_window(self):
        window = tk.Toplevel(root)
        window.title("Silence options")
        #window.overrideredirect(1)
        accept = tk.Button(window, text="accept", command=window.destroy)
        accept.pack(side="bottom", pady=(10,0))
        label = tk.Label(window, text="silences.txt files are the only option for silence files")
        label.config(font="bold")
        label.pack(anchor='w', padx=(10,10), pady=(10,10))
        self.silences_type = True

    def lena5min_window(self):
        window=tk.Toplevel(root)
        window.title("lena5min options")
        #window.overrideredirect(1)
        accept = tk.Button(window, text="accept", command=window.destroy)
        accept.pack(side="bottom", pady=(10,0))
        label = tk.Label(window, text="lena5min.csv files are the only option for lena5min")
        label.config(font="bold")
        label.pack(anchor='w', padx=(10,10), pady=(10,10))
        self.lena5min_type=True

    def video_mp4_window(self):
        window=tk.Toplevel(root)
        window.title("video_mp4 options")
        #window.overrideredirect(1)
        accept = tk.Button(window, text="accept", command=window.destroy)
        accept.pack(side="bottom", pady=(10,0))
        label = tk.Label(window, text=".mp4 files are the only option for video_mp4 files")
        label.config(font="bold")
        label.pack(anchor='w', padx=(10,10), pady=(10,10))
        self.lena5min_type=True

    def audio_wav_window(self):
        window = tk.Toplevel(root)
        window.title("Audio wav options")
        #window.overrideredirect(1)
        accept = tk.Button(window, text="accept", command=window.destroy)
        accept.pack(side="bottom", pady=(10,0))
        label = tk.Label(window, text="Choose which audio wav files you want")
        label.config(font="bold")
        label.pack(anchor="w", padx=(10,10), pady=(10,10))
        button = tk.StringVar()
        scrubbed_button = tk.Radiobutton(window, text="scrubbed", variable=self.audio_wav_type, value="scrubbed", command=self.audio_wav_type.set("scrubbed"))
        scrubbed_button.pack(anchor='w')
        unscrubbed_button = tk.Radiobutton(window, text="unscrubbed", variable=self.audio_wav_type, value="unscrubbed", command=self.audio_wav_type.set("unscrubbed"))
        unscrubbed_button.pack(anchor='w')
        self.audio_wav_type.set("scrubbed")


    # def crawl_files(self, file_or_dirname):
    #     #self.start_button.config(state="disable")
    #     if len(self.checked_boxes)==0:
    #         tkMessageBox.showinfo("Error", "You must select some file types!")
    #         self.file_type_chooser()
    #         return
    #     self.tups=[]
    #     if self.recurse_or_scan.get():
    #         if not file_or_dirname.endswith('.csv'):
    #             tkMessageBox.showinfo("Error", "You must provide a csv file to scan or uncheck the top box.")
    #             return
    #         self.crawl_files_from_csv(file_or_dirname)
    #     else:
    #         if not os.path.isdir(file_or_dirname):
    #             tkMessageBox.showinfo("Error", "You must provide a directory to crawl.")
    #             return
    #         self.crawl_files_recursive(file_or_dirname)
    #
    # def crawl_files_from_csv(self, filename):
    #     with open(filename, 'r') as f:
    #         reader = csv.reader(f, delimiter=',', )
    #         next(reader, None)
    #         for row in reader:
    #             # filtering by month
    #             m = re.search(r'[0-9]{2}_[0-9]{2}/', row[0])
    #             if re.search(r'[0-9]{2}_[0-9]{2}/', row[0]):
    #                 splt = m.group(0).split("_")
    #                 month = int(splt[1].strip('/'))
    #                 if month > int(self.end_month_var.get()) or month < int(self.start_month_var.get()):
    #                     continue
    #             # filtering by subject
    #             n = re.search(r'[0-9]{2}_[0-9]{2}-[0-9]{2}-[0-9]{4}', row[0])
    #             if re.search(r'[0-9]{2}_[0-9]{2}-[0-9]{2}-[0-9]{4}', row[0]):
    #                 splt = n.group(0).split("_")
    #                 subject = int(splt[0])
    #                 if subject not in self.chosen_subjects:
    #                     continue
    #             self.update_tups(row[0], row[1])
    #         # once done
    #         if self.copy_or_csv.get()=="copy":
    #             self.copy_files(self.tups)
    #         else:
    #             self.copy_to_csv(self.tups)
    #
    # def crawl_files_recursive(self, dirname):
    #     # if the save file name is empty and you want a csv
    #     if not self.filename.get() and self.copy_or_csv.get()=="csv":
    #         tkMessageBox.showinfo("Error", "You must provide a name for your file!")
    #         return
    #     # for each item in this directory
    #     try:
    #         for sub in os.listdir(dirname):
    #             path = os.path.join(dirname, sub)
    #             # if the current item is a directory, recurse
    #             if os.path.isdir(path):
    #                 # only recurse into dirs that lie within specified month ranges
    #                 if re.match(r'[0-9]{2}_[0-9]{2}$', sub):
    #                     splt = sub.split("_")
    #                     month = int(splt[1])
    #                     if month > int(self.end_month_var.get()) or month < int(self.start_month_var.get()):
    #                         continue
    #                 if re.search(r'[0-9]{2}_[0-9]{2}-[0-9]{2}-[0-9]{4}', sub):
    #                     splt = sub.split("_")
    #                     subject = int(splt[0])
    #                     if subject not in self.chosen_subjects:
    #                         continue
    #                 self.crawl_files_recursive(path)
    #             # else, here's a file to check
    #             else:
    #                 #self.tups.append((str(path), str(sub)))
    #                 # add file paths to tups if it fits criteria
    #                 self.update_tups(path, sub)
    #     # this only happens if we don't have permissions to files
    #     except OSError as e:
    #         print(e)
    #     # once all of the items in the top level directory have been searched, we're done
    #     if dirname==self.crawl_dir:
    #         if self.copy_or_csv.get()=="copy":
    #             self.copy_files(self.tups)
    #         else:
    #             self.copy_to_csv(self.tups)
    #
    #
    # def copy_to_csv(self, lst):
    #     if len(lst)==0:
    #         tkMessageBox.showinfo("Error", "No files of the selected type exist in your chosen directory!")
    #         return
    #     x = self.save_filename.strip()
    #     if not re.match("(.csv)$", self.save_filename):
    #         x+=".csv"
    #     with open(self.output_dir+'/'+x, 'a+') as f:
    #         writer = csv.writer(f)
    #         writer.writerow(["full path", "file name"])
    #         for item in lst:
    #             writer.writerow(item)
    #     tkMessageBox.showinfo("Completed", "Directory successfully copied to csv!")
    #
    # def copy_files(self, lst):
    #     if len(lst)==0:
    #         tkMessageBox.showinfo("Error", "No files of the selected type exist in your chosen directory!")
    #         return
    #     if self.dump_or_keep.get():
    #         for tup in lst:
    #             filepath = tup[0]
    #             savepath = self.output_dir
    #             shutil.copy(filepath, savepath)
    #     else:
    #         for tup in lst:
    #             filepath = tup[0]
    #             drive, localdir = os.path.splitdrive(filepath)
    #             localdir = os.path.normpath(os.path.dirname(localdir).replace(self.crawl_dir, "")).lstrip(r"\\").lstrip("/")
    #             savepath = os.path.join(self.output_dir,os.path.basename(self.crawl_dir),localdir)
    #             try:
    #                 with open(savepath) as f: pass
    #             except IOError as e:
    #                 if not os.path.exists(savepath):
    #                     os.makedirs(savepath)
    #                 shutil.copy(filepath, savepath)
    #     tkMessageBox.showinfo("Completed", "Directory successfully copied!")
    #
    # def update_tups(self, path, sub):
    #     if "audio_basic" in self.checked_boxes:
    #         if os.path.dirname(path).endswith('Audio_Analysis'):
    #             if re.search(r'sparse_code.csv$', sub):
    #                 self.tups.append((str(path), str(sub)))
    #     if "video_basic" in self.checked_boxes:
    #         if os.path.dirname(path).endswith('Video_Analysis'):
    #             if re.search(r'sparse_code.csv$', sub):
    #                 self.tups.append((str(path), str(sub)))
    #     if "silences" in self.checked_boxes:
    #         if re.search(r'silences\.txt$', sub):
    #             self.tups.append((str(path), str(sub)))
    #     if "lena5min" in self.checked_boxes:
    #         if re.search(r'lena5min\.csv$', sub):
    #             self.tups.append((str(path), str(sub)))
    #     if "video_mp4" in self.checked_boxes:
    #         if re.search(r'\.mp4$', sub):
    #             self.tups.append((str(path), str(sub)))
    #     if "audio_clan" in self.checked_boxes:
    #         if self.audio_clan_type.get()=='final':
    #             if os.path.dirname(path).endswith('Audio_Annotation'):
    #                 if re.search(r'(cex|cha)$', sub):
    #                     self.tups.append((str(path), str(sub)))
    #         if self.audio_clan_type.get()=="newclan_merged_final":
    #             if re.search(r'newclan_merged_final\.(cex|cha)$', sub):
    #                 self.tups.append((str(path), str(sub)))
    #         if self.audio_clan_type.get()=='newclan_merged':
    #             if re.search(r'newclan_merged\.(cex|cha)$', sub):
    #                 self.tups.append((str(path), str(sub)))
    #         if self.audio_clan_type.get()=='silences':
    #             if re.search(r'silences.*(cex|cha)$', sub):
    #                 self.tups.append((str(path), str(sub)))
    #     if "video_datavyu" in self.checked_boxes:
    #         if self.video_datavyu_type.get()=='final':
    #             if re.search(r'final\.(opf)$', sub):
    #                 self.tups.append((str(path), str(sub)))
    #         if self.video_datavyu_type.get()=='consensus':
    #             if re.search(r'consensus\.(opf)$', sub):
    #                 self.tups.append((str(path), str(sub)))
    #     if "audio_wav" in self.checked_boxes:
    #         if self.audio_wav_type.get()=='scrubbed':
    #             if re.search(r'scrubbed.*wav$', sub):
    #                 self.tups.append((str(path), str(sub)))
    #         if self.audio_wav_type.get()=='unscrubbed':
    #             if re.search(r'\.wav$', sub) and "scrubbed" not in sub:
    #                 self.tups.append((str(path), str(sub)))
    #     if "custom_regex" in self.checked_boxes:
    #         if re.search(self.custom_regex_text.get(), sub):
    #             self.tups.append((str(path), str(sub)))



if __name__=="__main__":
    root = tk.Tk()
    my_gui = crawl_subject_GUI(root)
    root.mainloop()
