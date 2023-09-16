import os
import re, pickle, threading
from tkinter import *
import _thread, time
import sys
from random import randint
from numpy.random import choice
sys.path.append('Vigi_EXE')
sys.path.append('Vigi_PDF')
import VGhelpers as VA
from PIL import Image, ImageTk

current_Directory = os.path.split(os.path.realpath(__file__))[0]
parent_Directory = os.path.split(current_Directory)[0]
with open(os.path.join(current_Directory, 'Vigi_EXE', 'models', 'secret_tips.pkl'), 'rb') as f:
    secret_tip_list = pickle.load(f)
    secret_tip = secret_tip_list[randint(0, len(secret_tip_list)-1)]
Aymans_Word = r'''
Vigil-Anti is a Free Open Source
Anti virus, built to be as light
and efficient as possible while 
being user friendly and reliable.

right now, We support detecting:
PE executables and PDF formats.'''


class Indigo_Preset:
    window_color="#02010a"
    button_color="#22007c"
    button_hover_color="#15004e"
    red_button_color="#690000"
    red_button_hover_color="#330101"
    malicious_color = "#a80000"
    safe_color = "#005d1d"
    yellow_color="#eca72c"

    frame_color = "#030427"
    brown_color="#7f5539"




import customtkinter as ctk

global file_path, folder_path
already_Placed = False
root = None

file_path, folder_path = False, False
sch_output =[]

def getFileStatus_from_code(return_code):
    if return_code ==0:
        return ("Safe")
    elif return_code ==1:
        return ("Malicious")
    elif return_code == -1:
        return ("Format Not Supported yet")
    else:
        return ("No Data")



def Display_Single_Result(file_path, result):
    new_window = ctk.CTk()
    fm = ctk.CTkFrame(new_window)
    fm.pack()
    label_file = ctk.CTkLabel(fm, text=file_path)
    label_result = ctk.CTkLabel(fm, text=result)
    label_file.pack(anchor=ctk.W)
    label_result.pack(anchor=ctk.E)
    new_window.mainloop()

def getFilePath_and_scan():
    global file_path
    file_path = ctk.filedialog.askopenfilename()
    if(file_path):
        print(file_path)
        result = scanFile(file_path=file_path)
        font= ctk.CTkFont(size=30, family='Helvetica', weight='bold')
        text_colour='white'
        if(result == 1): colour=Indigo_Preset.malicious_color
        elif(result == 0): colour=Indigo_Preset.safe_color
        else:
            colour=Indigo_Preset.yellow_color
            font= ctk.CTkFont(size=22, family='Helvetica', weight='bold')
            text_colour='green'
        Result_of_File_label.configure(text=getFileStatus_from_code(result), bg_color=Indigo_Preset.window_color,fg_color=colour, font=font, text_color=text_colour)
        Result_of_File_label.lift()
        #label = ctk.CTkLabel(root, text= getFileStatus_from_code(result), fg_color=colour, font=ctk.CTkFont(size=30, family='Helvetica', weight='bold'), corner_radius=20, width=50, height=20)
        #label.place(relx=0.75, rely=0.6, anchor='center')
        #Display_Single_Result(file_path=file_path, result=getFileStatus_from_code(result))




All_gifImages = [os.path.join(parent_Directory, 'icons', i) for i in ['resized_duck.gif', 'resized_bird.gif', 'resized_nyan.gif']]
gifImage = All_gifImages[choice((0,1,2), p=[0.5,0.2,0.3])]
openImage = Image.open(gifImage)
frames = openImage.n_frames
currentFrameIndex = 0
imageObject =[]
final_result = {}
stopFlag = False
thread1 = None


def Folder_result_Loading_window():
    
    def animation(gif_label, imageObject):
        fold_win.configure(bg=Indigo_Preset.window_color, fg=Indigo_Preset.window_color) 
        global currentFrameIndex
        #global imageObject
        newImage = imageObject[currentFrameIndex]
        gif_label.configure(image=newImage)
        gif_label.image= newImage
        currentFrameIndex += 1
        if(currentFrameIndex == frames): currentFrameIndex=0


    def getFolderPath_and_scan():
        fold_win.configure(bg=Indigo_Preset.window_color, fg=Indigo_Preset.window_color)
        global thread1
        global folder_path
        folder_path = ctk.filedialog.askdirectory()
        print(folder_path)
        if (folder_path == ''):
            fold_win.destroy()
        if folder_path:
            progress_label = ctk.CTkLabel(fold_win, text=f"Please wait while Vigil-Anti is Scanning {folder_path} ...",font=ctk.CTkFont(size=20, family='Helvetica', weight='bold'), fg_color=Indigo_Preset.window_color, bg_color=Indigo_Preset.window_color)
            progress_label.place(relx = 0.5, rely= 0.2, anchor='center')
            progbar = ctk.CTkProgressBar(fold_win, orientation=ctk.HORIZONTAL, width=470, border_width=1, border_color='black',height=13,mode="determinate")
            progbar.set(0)
            progbar.place(relx=0.5, rely=0.3, anchor='center')

            def anime():
                global stopFlag
                while(True):
                    fold_win.after(50, animation,load_label, imageObject)
                    if(stopFlag):
                        return
                    time.sleep(0.05)
            def update_progress():
                global stopFlag
                global final_result
                fl = False
                for iter in scanFolder(folder_path=folder_path):
                    fold_win.after(50, animation,load_label, imageObject)
                    if not fl:
                        num_files = iter
                        fl = True
                    if type(iter) == int and iter > 0:
                        progbar.set(iter / num_files)
                    else:
                        progbar.set(1)
                        final_result = iter
                stopFlag = True
                fold_win.destroy()
                Folder_result_window(final_result)
                
                
    
            thread1 = threading.Thread(target=update_progress)
            thread1.start()
            thread2 = threading.Thread(target=anime)
            thread2.start()
            


    fold_win = ctk.CTk()
    w, h = 800,400
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    fold_win.geometry('%dx%d+%d+%d' % (w, h, x, y))
    fold_win.overrideredirect(True)
    fold_win.resizable(False,False)
    fold_win.configure(fg_color=Indigo_Preset.window_color)
    fold_win.iconbitmap(os.path.join(parent_Directory, 'icons', 'logo_white.ico'))
    

    imageObject = [PhotoImage(master=fold_win, file=gifImage, format=f"gif -index {i}") for i in range(frames)]
    
    load_label= ctk.CTkLabel(fold_win, text='', bg_color=Indigo_Preset.window_color, fg_color=Indigo_Preset.window_color)
    load_label.place(relx=0.5, rely=0.7, anchor='center')
    #animation(load_label)
    
    #if(not getFolderPath_and_scan()): fold_win.destroy()
    getFolderPath_and_scan()
    #fold_win.after(50, lambda: animation(load_label, imageObject))

    fold_win.mainloop()

def cleanse_n_sort(res:dict):
    mal_list= []
    safe_list = []
    unk_list = []
    for k,v in res.items():
        if v == 1:
            mal_list.append((k,v))
        elif v==0:
            safe_list.append((k,v))
        else:
            unk_list.append((k,v))
    return mal_list + safe_list + unk_list

def Folder_result_window(results:dict):

    def delete_threat(filepath):
        
        # def warning_window():
        #     warn_window= ctk.CTk()
        #     warn_window.geometry('300x200')
        #     im = Image.open(os.path.join(parent_Directory, 'icons', 'warning.png'))
        #     img_label=ctk.CTkLabel(warn_window, image=ctk.CTkImage(light_image=im,dark_image=im, size=(100,100)))
        #     img_label.image=im
        #     img_label.pack()
        #     warnLabel = ctk.CTkLabel(warn_window, text='''Vigil-Anti does not have permission to delete this file
        #                              go delete it yourself :)''')
        #     close_button = ctk.CTkButton(warn_window, text='Close', command=warn_window.destroy)
        #     warn_window.mainloop()
            
        try:
            os.remove(os.path.abspath(filepath))
            delete_widget(filpath=filepath)
            #warning_window()
        except Exception as e:
            print(f'\n\n\n                           WARNING\n\n\n{e}')


    def delete_widget(filpath):
        for wid in widget_list:
            if wid[0].cget('text') == filpath:
                wid[2].destroy()
                wid[1].destroy()
                wid[0].destroy()
                wid[3].destroy()


    results = cleanse_n_sort(results)
    fold_res_window = ctk.CTk()
    fold_res_window.configure(fg_color=Indigo_Preset.window_color)
    w, h = 800,450
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    fold_res_window.geometry('%dx%d+%d+%d' % (w, h, x, y))
    fold_res_window.resizable(False, False)
    widget_list = []
    scrollable_frame = ctk.CTkScrollableFrame(fold_res_window, width=770, height=430, fg_color=Indigo_Preset.window_color)
    scrollable_frame.pack()
    for path, status in results:
        task_frame = ctk.CTkFrame(scrollable_frame, width=750, height=50, bg_color=Indigo_Preset.window_color, fg_color=Indigo_Preset.frame_color)
        task_frame.pack(pady=5)
        task_path_label = ctk.CTkLabel(task_frame, text= str(path), font=ctk.CTkFont(size=15, family='Helvetica', weight='normal'))
        task_path_label.place(relx=0.02, rely=0.5, anchor='w')
        
        if status == 1:
            status_string = "Malicious"
            fg_color = Indigo_Preset.malicious_color
            width = len(status_string)*13
        elif status == 0:
            status_string = "Safe"
            fg_color = Indigo_Preset.safe_color
            width = len(status_string)*15
        else:
            status_string="Format not supported yet"
            fg_color = Indigo_Preset.brown_color
            width = 50
        task_duration = ctk.CTkLabel(task_frame, text=status_string, fg_color=fg_color, corner_radius=30, width=width, font=ctk.CTkFont(size=15, family='Helvetica', weight='bold'))
        task_duration.place(relx=0.6, rely=0.5, anchor='center')
        if(status ==1):
            delete_button = ctk.CTkButton(task_frame, text= 'Remove Threat', fg_color=Indigo_Preset.red_button_color, hover_color=Indigo_Preset.red_button_hover_color, bg_color=Indigo_Preset.window_color, width=60, command= lambda filepath=str(path): delete_threat(filepath), font=ctk.CTkFont(size=15, family='Helvetica', weight='normal'))
            delete_button.place(relx=0.8, rely=0.5, anchor='w')
            widget_list.append((task_path_label, task_duration, delete_button, task_frame))
        else:
            widget_list.append((task_path_label, task_duration, ctk.CTkButton, task_frame))
    
    fold_res_window.mainloop()






def parse_schedule():
    if(os.path.isfile(os.path.join(current_Directory, 'Config', 'config.txt'))):
        with open(os.path.join(current_Directory, 'Config', 'config.txt'), 'r') as f:
            file_content = f.readlines()
        if(not file_content):
            return -1
        schedule=[]
        for lin in file_content:
            line = re.sub(r'\n', '', lin)
            file_path = re.findall('.*@@', line)
            if(not file_path): print('\n\n\nEEEERRRRRRRRRRROOOOOOOOOOOOR in scheduler')
            file_path = file_path[0][:-2]
            n = re.findall('@@\d+::', line)
            n = n[0][2:-2]
            minutes_flag = True if re.findall('::mins', line) else False
            days_flag = True if re.findall('::days', line) else False
            time_span = 'DAILY' if days_flag else 'MINUTE'
            schedule.append((file_path, n, time_span))
        return schedule
    else:
        return -1


def unschedule_window(but):
    
    def unschedule_task(index):
            widget_to_be_destroyed = widget_list[index]
            path= widget_to_be_destroyed[0].cget('text')
            often = re.findall('\d+ (\w+)', widget_to_be_destroyed[1].cget('text'))[0]
            VA.delete_schedule(file_path=os.path.abspath(path))
            widget_to_be_destroyed[2].destroy()
            widget_to_be_destroyed[1].destroy()
            widget_to_be_destroyed[0].destroy()
            widget_to_be_destroyed[3].destroy()
            if(len(widget_list) == 1):
                but.configure(text='no scheduled scans',state=ctk.DISABLED)
                unsch_window.destroy()
    
    

    unsch_window = ctk.CTk()
    unsch_window.configure(fg_color=Indigo_Preset.window_color)
    unsch_window.resizable(False, False)
    w, h = 600, 150
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    unsch_window.geometry('%dx%d+%d+%d' % (w, h, x, y))
    scheduled_tasks=parse_schedule()
    widget_list = []
    if(type(scheduled_tasks) != list): return
    for index, task in enumerate(scheduled_tasks):
        task_frame = ctk.CTkFrame(unsch_window, width=570, height=50, fg_color=Indigo_Preset.frame_color, bg_color=Indigo_Preset.window_color)
        task_frame.pack(pady=5)
        task_path_label = ctk.CTkLabel(task_frame, text= task[0], fg_color=Indigo_Preset.frame_color)
        task_path_label.place(relx=0.05, rely=0.5, anchor='w')
        task_duration = ctk.CTkLabel(task_frame, text=f"every {task[1]} "+f"{'Minutes' if task[2] == 'MINUTE' else 'Days'}")
        task_duration.place(relx=0.5, rely=0.5, anchor='w')
        delete_button = ctk.CTkButton(task_frame, text= 'Unschedule', fg_color=Indigo_Preset.red_button_color, bg_color=Indigo_Preset.frame_color, corner_radius=9, hover_color=Indigo_Preset.red_button_hover_color, width=60, command= lambda index=index: unschedule_task(index))
        delete_button.place(relx=0.8, rely=0.5, anchor='w')
        widget_list.append((task_path_label, task_duration, delete_button, task_frame))
    unsch_window.mainloop()


def ConfigureWindow():
    fullCommand = {'path':'', 'folder':0,'sm':0, 'sd':0, 'duration':-1}
    scheduled_tasks=parse_schedule()

    def update_slider_val(val):#, slider_val:ctk.CTkLabel):
        slider_val.configure(text=int(slider.get()))
        if(radio_var.get() == 1):
            fullCommand['sm'] = 1
            fullCommand['sd'] = 0
        elif(radio_var.get() == 2):
            fullCommand['sm'] = 0
            fullCommand['sd'] = 1
        fullCommand['duration'] = int(slider.get())
        if(fullCommand['path'] and fullCommand['duration'] > 0):
            apply_button.configure(state=ctk.NORMAL, fg_color=Indigo_Preset.button_color)
        else:
            apply_button.configure(state=ctk.DISABLED, fg_color=Indigo_Preset.button_hover_color)
        #print(fullCommand)
    
    def getFilePath():
        file_path = ctk.filedialog.askopenfilename()
        if(file_path):
            print(file_path)
            fullCommand['path'] = file_path
            fullCommand['folder'] = 0
            if(fullCommand['duration'] > 0):
                apply_button.configure(state=ctk.NORMAL, fg_color=Indigo_Preset.button_color)
            
            path_label.configure(text=file_path)
            conf_window.lift()

            return file_path
        else:
            conf_window.lift()

    def getFolderPath():
        folder_path = ctk.filedialog.askdirectory()
        if(folder_path):
            print(folder_path)
            fullCommand['path'] = folder_path
            fullCommand['folder'] = 1
            if(fullCommand['duration'] > 0):
                apply_button.configure(state=ctk.NORMAL, fg_color=Indigo_Preset.button_color)
            conf_window.lift()
            path_label.configure(text=folder_path)
            return folder_path
        else:
            conf_window.lift()
    
    def schedule():
        if (fullCommand['sm']):
            VA.schedule_minutes(file_path= fullCommand['path'], N_minutes=fullCommand['duration'])
            VA.run_scheduler(fullCommand['folder'])
        else:
            VA.schedule_days(file_path=fullCommand['path'], N_days=fullCommand['duration'])
            VA.run_scheduler(fullCommand['folder'])
        scheduled_tasks = parse_schedule()
        if(scheduled_tasks == -1):
            del_prev_button.configure(state=ctk.DISABLED, text='no scheduled scans', fg_color=Indigo_Preset.button_hover_color)
        else:
            del_prev_button.configure(state=ctk.NORMAL, fg_color=Indigo_Preset.button_color)
        #del_prev_button.configure(state=ctk.DISABLED if scheduled_tasks == -1 else ctk.NORMAL)
        #fullCommand['path']=''
        path_label.configure(text='')

    def unschedule():
        unschedule_window(del_prev_button)
        scheduled_tasks = parse_schedule()
        if(scheduled_tasks == -1):
            del_prev_button.configure(state=ctk.DISABLED, text='no scheduled scans', fg_color=Indigo_Preset.button_hover_color)
        else:
            del_prev_button.configure(state=ctk.NORMAL, fg_color=Indigo_Preset.button_color)

        

    conf_window = ctk.CTk()
    conf_window.title('Configure Schedules')
    w, h = 550,400
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    conf_window.geometry('%dx%d+%d+%d' % (w, h, x, y))
    conf_window.resizable(False,False)
    conf_window.configure(fg_color=Indigo_Preset.window_color)
    select_file = ctk.CTkButton(conf_window, text='Select Target File', command=getFilePath, corner_radius=9, font=ctk.CTkFont(size=20, family='Helvetica', weight='bold'), height=35, fg_color=Indigo_Preset.button_color, bg_color=Indigo_Preset.window_color, hover_color=Indigo_Preset.button_hover_color)
    select_file.place(relx=0.3, rely=0.2, anchor='center')
    select_folder = ctk.CTkButton(conf_window, text='Select Target Folder', command=getFolderPath, corner_radius=9, font=ctk.CTkFont(size=20, family='Helvetica', weight='bold'), height=35, fg_color=Indigo_Preset.button_color, bg_color=Indigo_Preset.window_color, hover_color=Indigo_Preset.button_hover_color)
    select_folder.place(relx=0.7, rely=0.2, anchor='center')

    slider_frame= ctk.CTkFrame(conf_window, width=230, height=130, corner_radius=20, fg_color=Indigo_Preset.frame_color)
    slider_frame.place(relx=0.5, rely=0.65, anchor='center')

    label=ctk.CTkLabel(slider_frame, text='Scan every')
    label.place(relx=0.5, rely=0.1, anchor='center')

    path_label = ctk.CTkLabel(conf_window, text='', font=ctk.CTkFont(size=20, family='Helvetica', weight='normal'))
    path_label.place(relx=0.5, rely=0.38 ,anchor='center')

    text_above_slider = ctk.IntVar()

    slider_val = ctk.CTkLabel(slider_frame, text='0', font=ctk.CTkFont(size=12, family='Helvetica'))
    slider_val.place(relx=0.5, rely=0.25, anchor='center')

    slider=ctk.CTkSlider(slider_frame, from_=0, to=60, command=update_slider_val, variable=text_above_slider)
    slider.place(relx=0.5, rely=0.5, anchor='center')
    
    radio_var = ctk.IntVar(value=1)
    radiobutton_1 = ctk.CTkRadioButton(slider_frame, text="Minutes", variable= radio_var, value=1)
    radiobutton_2 = ctk.CTkRadioButton(slider_frame, text="Days", variable= radio_var, value=2)
    radiobutton_1.place(relx=0.4, rely=0.8, anchor='center')
    radiobutton_2.place(relx=0.84, rely=0.8, anchor='center')

    if scheduled_tasks == -1:
        stt=ctk.DISABLED
        fgcolor=Indigo_Preset.button_hover_color
    else:
        stt=ctk.NORMAL
        fgcolor=Indigo_Preset.button_color
    del_prev_button = ctk.CTkButton(conf_window, text='Un-schedule tasks', corner_radius=9, font=ctk.CTkFont(size=12, family='Helvetica'), state=stt, command=unschedule, fg_color=fgcolor, bg_color=Indigo_Preset.window_color, hover_color=Indigo_Preset.button_hover_color)
    del_prev_button.place(relx=0.5, rely=0.9, anchor='center')

    apply_button = ctk.CTkButton(conf_window, text='Apply', corner_radius=9, font=ctk.CTkFont(size=12, family='Helvetica'), width=80, state=ctk.DISABLED, command=schedule, fg_color=Indigo_Preset.button_hover_color, bg_color=Indigo_Preset.window_color, hover_color=Indigo_Preset.button_hover_color)
    apply_button.place(relx=0.8, rely=0.9, anchor='center')


    Cancel_button = ctk.CTkButton(conf_window, text='Cancel', corner_radius=9, font=ctk.CTkFont(size=12, family='Helvetica'), width=80, command=conf_window.destroy, fg_color=Indigo_Preset.button_color, bg_color=Indigo_Preset.window_color, hover_color=Indigo_Preset.button_hover_color)
    Cancel_button.place(relx=0.2, rely=0.9, anchor='center')

    conf_window.mainloop()


def scanFile(file_path):
    return VA.FileScan(filePath=file_path)

def scanFolder(folder_path):
    return VA.Folder_Scan_with_metrics(folder=folder_path)



def remove_from_output_files(file_path, but):
    global sch_output
    config_directory = os.path.join(current_Directory, 'Config')
    allFiles = os.listdir(config_directory)
    for file in allFiles:
        if file.startswith('Output') and file.endswith('.txt'):
            output_file_path = os.path.join(config_directory, file)
            with open(output_file_path, 'r') as f:
                if(not f.read() ):
                    continue
            with open(output_file_path, 'r') as f:
                if(len(f.readlines())< 2):
                    continue
            with open(output_file_path, 'r') as f:
                fileLines=f.readlines()
            modified=[]
            modified.append(re.sub('\n','',fileLines[0]))
            for lin in fileLines[1:]:
                line_with_no_newlines = re.sub('\n', '', lin)
                smolPath = re.findall('(.*)\s+Malicious', line_with_no_newlines)
                if(not smolPath): continue
                smolPath = smolPath[0]
                if(os.path.abspath(file_path) == os.path.abspath(smolPath)):
                    continue
                modified.append(line_with_no_newlines)
            with open(os.path.join(config_directory, file), 'w') as f:
               if(modified):
                    f.write('\n'.join(modified))
                    f.write('\n')
            if(len(modified) == 1):
                os.remove(os.path.join(config_directory, file))
        else: continue
    
    sch_output = check_sch_output()
    if(not sch_output):
        but.configure(text='All threats resolved', fg_color='green', state=ctk.DISABLED)
        return



def show_threats(results:dict, but:ctk.CTkButton):
    def delete_threat(filepath):
        try:
            print(os.path.abspath(filepath))
            os.remove(os.path.abspath(filepath))
            remove_from_output_files(filepath, but)
            delete_widget(filpath=filepath)
            #warning_window()
        except Exception as e:
            print(f'\n\n\n                           WARNING\n\n\n{e}')


    def delete_widget(filpath):
        for wid in widget_list:
            if wid[0].cget('text') == filpath:
                wid[2].destroy()
                wid[1].destroy()
                wid[0].destroy()
                wid[3].destroy()

    if(not check_sch_output()): 
        but.configure(text='All threats resolved', fg_color='green', state=ctk.DISABLED)
        return
    threats_win = ctk.CTk()
    w, h = 800,450
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    threats_win.geometry('%dx%d+%d+%d' % (w, h, x, y))
    widget_list = []
    scrol_Frame = ctk.CTkScrollableFrame(threats_win, width=770, height=430, fg_color=Indigo_Preset.window_color)
    scrol_Frame.pack()
    for pth, stts in results.items():
        if(not stts):
            continue
        pth_Frame = ctk.CTkFrame(scrol_Frame, width=750, height=50, bg_color=Indigo_Preset.window_color, fg_color=Indigo_Preset.frame_color)
        pth_Frame.pack(pady=5)
        tsk_pth_Label = ctk.CTkLabel(pth_Frame, text= str(pth), font=ctk.CTkFont(size=15, family='Helvetica', weight='normal'))
        tsk_pth_Label.place(relx=0.02, rely=0.5, anchor='w')
        if stts == 1:
            status_string = "Malicious"
            fg_color = Indigo_Preset.malicious_color
            width = len(status_string)*13
        
        tsk_duration = ctk.CTkLabel(pth_Frame, text=status_string, fg_color=fg_color, corner_radius=30, width=width, font=ctk.CTkFont(size=15, family='Helvetica', weight='bold'))
        tsk_duration.place(relx=0.6, rely=0.5, anchor='center')
        dlt_button = ctk.CTkButton(pth_Frame, text= 'Remove Threat', width=60, command= lambda filepath=str(pth): delete_threat(filepath), fg_color=Indigo_Preset.red_button_color, hover_color=Indigo_Preset.red_button_hover_color, bg_color=Indigo_Preset.window_color,font=ctk.CTkFont(size=15, family='Helvetica', weight='normal'))
        dlt_button.place(relx=0.8, rely=0.5, anchor='w')
        widget_list.append((tsk_pth_Label, tsk_duration, dlt_button, pth_Frame))
    sch_output = check_sch_output()
    if(not sch_output):
        but.configure(text='All threats resolved', fg_color='green', state=ctk.DISABLED)
        return
    threats_win.mainloop()


def check_sch_output():
    config_directory = os.path.join(current_Directory, 'Config')
    allFiles = os.listdir(config_directory)
    all_lines=[]
    for file in allFiles:
        if file.startswith('Output'):
            output_file_path = os.path.join(config_directory, file)
            try:
                with open(output_file_path, 'r') as f:
                    if not f.read():
                        return False
                with open(output_file_path, 'r') as f:
                    if len(f.readlines()) < 2:
                        return False
                with open(output_file_path, 'r') as f:
                    all_lines+=f.readlines()[1:]
            except: return False
    if(not all_lines or all_lines == []):
        return False
    
    all_lines = [re.sub('\n','',i) for i in all_lines]


    return_dict = {}
    for lin in all_lines:
        file_status_safe = re.findall('Safe$', lin)
        file_status_Malicious = re.findall('Malicious$', lin)
        if(file_status_safe): file_status = 'Safe'
        elif(file_status_Malicious): file_status = 'Malicious'
        else: return False
        remains = re.sub('\w+$','', lin)
        file_path= re.sub('\s+$','', remains)
        return_dict[str(file_path)] = 1 if file_status == 'Malicious' else 0
    for k,v in return_dict.items():
        if(v): return return_dict
    return False



root= ctk.CTk()
root.title('Vigil-Anti')
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen
w, h = 800,600
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
root.geometry('%dx%d+%d+%d' % (w, h, x, y))
root.resizable(False,False)
root.iconbitmap(os.path.join(parent_Directory, 'icons', 'logo_white.ico'))
root.configure(fg=Indigo_Preset.window_color, bg=Indigo_Preset.window_color)
#photo = PhotoImage(file=os.path.join(parent_Directory, 'icons', 'logo.ico'))
#root.wm_iconphoto(True, photo)

logo_image = ctk.CTkImage(light_image=Image.open(os.path.join(parent_Directory, 'icons','Blue_VIGI.png')), dark_image=Image.open(os.path.join(parent_Directory, 'icons','Blue_VIGI.png')), size=(800,1016))
logo_label = ctk.CTkLabel(root, width=400, height=400, image=logo_image, text='', fg_color=Indigo_Preset.window_color)
logo_label.place(relx=0.4, rely=0.0)

leftFrame = ctk.CTkFrame(root, width=370, height=600, fg_color=Indigo_Preset.window_color)
leftFrame.place(relx=0.0, rely=0.0)
scale_logo = ctk.CTkImage(light_image=Image.open(os.path.join(parent_Directory, 'icons','scales_vert.png')), dark_image=Image.open(os.path.join(parent_Directory, 'icons','scales_vert.png')), size=(1000,1000))
scale_lamp=ctk.CTkLabel(leftFrame, image=scale_logo)
#scale_lamp.place(relx=0.4, rely=0.4, anchor='center')
Tip_Of_the_day = ctk.CTkLabel(leftFrame, width=370, height=120, text="Tip of the day", font=ctk.CTkFont(size=30, family='Helvetica', weight='bold'))
Tip_Of_the_day.place(relx = 0.45, rely=0.2, anchor='center')
lamp_img=ctk.CTkImage(light_image=Image.open(os.path.join(parent_Directory, 'icons','yellowlamp.png')), dark_image=Image.open(os.path.join(parent_Directory, 'icons','yellowlamp.png')), size=(48,48))
lamp_label = ctk.CTkLabel(leftFrame, image=lamp_img, text='')
lamp_label.place(relx=0.85, rely=0.2, anchor='center')


tip_label = ctk.CTkLabel(leftFrame, text=secret_tip, font=ctk.CTkFont(size=15, family='Helvetica', weight='bold'))
tip_label.place(relx=0.062, rely=0.28, anchor='nw')
ayman_label = ctk.CTkLabel(leftFrame, text=Aymans_Word, font=ctk.CTkFont(size=17, family='Helvetica', weight='bold'))
ayman_label.place(relx=0.45, rely= 0.8, anchor='center')


vigilanti_place= ctk.CTkLabel(root, width=156,height=150, text='', font=ctk.CTkFont(size=30, family='Kozuka Gothic Pr6N B', weight='bold'), corner_radius=50, fg_color=Indigo_Preset.button_color, bg_color=Indigo_Preset.window_color)
vigilanti_place.place(relx=0.5, rely=0.060, anchor='s')

vigilanti_title= ctk.CTkLabel(root, height=30, text='Vigil-Anti', font=ctk.CTkFont(size=25, family='Kozuka Gothic Pr6N B', weight='bold'), text_color='#ced4da',fg_color=Indigo_Preset.button_color)
vigilanti_title.place(relx=0.5, rely=0.025, anchor='center')


frame_for_buttons = ctk.CTkFrame(root, width=600, height=42, corner_radius=30)
frame_for_buttons.place(relx=0.65, rely=0.7)
frame_for_schedule = ctk.CTkFrame(root, width=150, height=42)
frame_for_schedule.place(relx=0.69, rely=0.78)
scan_file_button = ctk.CTkButton(frame_for_buttons, text='Scan a File!', command=getFilePath_and_scan, width=100, fg_color=Indigo_Preset.button_color, hover_color=Indigo_Preset.button_hover_color)
scan_file_button.pack(side=LEFT, padx=3)
#space_padding= ctk.CTkFrame(frame_for_buttons, width=10, height=42)
#space_padding.grid(row=0, column=2)
scan_folder_button = ctk.CTkButton(frame_for_buttons, text='Scan a Folder!', command=Folder_result_Loading_window, width=100, fg_color=Indigo_Preset.button_color, hover_color=Indigo_Preset.button_hover_color)
scan_folder_button.pack(side=RIGHT, padx=3)


Result_of_File_label = ctk.CTkLabel(root, text='',corner_radius=20, width=50, height=20)
Result_of_File_label.place(relx=0.785, rely=0.65, anchor='center')
Result_of_File_label.lower()

Configure_button = ctk.CTkButton(frame_for_schedule, text='Schedule Scans', command=ConfigureWindow, fg_color=Indigo_Preset.button_color, hover_color=Indigo_Preset.button_hover_color, bg_color=Indigo_Preset.window_color)
Configure_button.grid(row=2,column=2)


sched_scan_result_button = ctk.CTkButton(root, text='Vigil-Anti found present threats\n   click to resolve', font=ctk.CTkFont(size=16, family='Helvetica', weight='bold'), fg_color=Indigo_Preset.red_button_color, corner_radius=50, hover_color=Indigo_Preset.red_button_hover_color, bg_color=Indigo_Preset.window_color)
sched_scan_result_button.configure(command=lambda res=sch_output, but=sched_scan_result_button: show_threats(res, but))


def place_sched_scan_butt():
    global already_Placed
    
    sch_output = check_sch_output()
    if(sch_output):
        if(not already_Placed):
            sched_scan_result_button = ctk.CTkButton(root, text='Vigil-Anti found present threats\n   click to resolve', font=ctk.CTkFont(size=16, family='Helvetica', weight='bold'), fg_color=Indigo_Preset.red_button_color, corner_radius=50, hover_color=Indigo_Preset.red_button_hover_color, bg_color=Indigo_Preset.window_color)
            sched_scan_result_button.configure(command=lambda res=sch_output, but=sched_scan_result_button: show_threats(res, but))

            sched_scan_result_button.place(relx=0.217, rely=0.6, anchor='center')
            already_Placed=True
    else:
        try:
            sched_scan_result_button.destroy()
        except: pass
        already_Placed=False
    root.after(3000, place_sched_scan_butt)

place_sched_scan_butt()


root.mainloop()