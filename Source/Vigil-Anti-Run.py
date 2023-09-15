import os
import re, pickle, threading
from tkinter import *
import _thread, time
import sys
from random import randint
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



import customtkinter as ctk

global file_path, folder_path

file_path, folder_path = False, False
All_gifImages = [os.path.join(parent_Directory, 'icons', i) for i in ['duck.gif', 'bird.gif', 'nyan.gif']]
gifImage = All_gifImages[randint(0, 2)]

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
        if(result == 1): colour='red'
        elif(result == 0): colour='green'
        else:
            colour='yellow'
            font= ctk.CTkFont(size=22, family='Helvetica', weight='bold')
            text_colour='green'
        Result_of_File_label.configure(text=getFileStatus_from_code(result), bg_color='transparent',fg_color=colour, font=font, text_color=text_colour)
        Result_of_File_label.lift()
        #label = ctk.CTkLabel(root, text= getFileStatus_from_code(result), fg_color=colour, font=ctk.CTkFont(size=30, family='Helvetica', weight='bold'), corner_radius=20, width=50, height=20)
        #label.place(relx=0.75, rely=0.6, anchor='center')
        #Display_Single_Result(file_path=file_path, result=getFileStatus_from_code(result))






def Folder_result_window():
    

    def getFolderPath_and_scan():
        global folder_path
        folder_path = ctk.filedialog.askdirectory()
        if folder_path:
            print(folder_path)
            progress_label = ctk.CTkLabel(fold_win, text=f"Please wait while Vigil-Anti is Scanning {folder_path} ...",font=ctk.CTkFont(size=20, family='Helvetica', weight='bold'))
            progress_label.place(relx = 0.5, rely= 0.43, anchor='center')
            progbar = ctk.CTkProgressBar(fold_win, orientation=ctk.HORIZONTAL, width=380,mode="determinate")
            progbar.place(relx=0.5, rely=0.5, anchor='center')
            
            def update_progress():
                fl = False
                
                for iter in scanFolder(folder_path=folder_path):
                    if not fl:
                        num_files = iter
                        fl = True
                    if type(iter) == int and iter > 0:
                        progbar.set(iter / num_files)
                    else:
                        final_result = iter

                for k, v in final_result.items():
                    label1 = ctk.CTkLabel(fold_win, text=str(k))
                    label2 = ctk.CTkLabel(fold_win, text=getFileStatus_from_code(v))
                    label1.pack(anchor=ctk.W)
                    label2.pack(anchor=ctk.E)
    
            thread = threading.Thread(target=update_progress)
            thread.start()




    fold_win = ctk.CTk()
    fold_win.geometry('800x600')
    getFolderPath_and_scan()

    fold_win.mainloop()


class gifplay:
    """
    Usage: mygif=gifplay(<<tkinter.label Objec>>,<<GIF path>>,<<frame_rate(in ms)>>)
    example:
    gif=GIF.gifplay(self.model2,'./res/neural.gif',0.1)
    gif.play()
    This will play gif infinitely
    """
    def __init__(self,label,giffile,delay):
        self.frame=[]
        i=0
        while 1:
            try:
                image=PhotoImage(file = giffile, format="gif -index "+str(i))
                self.frame.append(image)
                i=i+1
            except:
                break
        print(i)
        self.totalFrames=i-1
        self.delay=delay
        self.labelspace=label
        self.labelspace.image=self.frame[0]

    def play(self):
        """
        plays the gif
        """
        _thread.start_new_thread(self.infinite,())

    def infinite(self):
        i=0
        while 1:
            self.labelspace.configure(image=self.frame[i])
            i=(i+1)%self.totalFrames
            time.sleep(self.delay)


"""
def animate(i):
    try:
        photo = ImageTk.PhotoImage(Image.open('your_gif.gif').seek(i))
        label.config(image=photo)
        label.image = photo
        root.after(100, animate, i+1)
    except:
        root.after(100, animate, 0)

root = ctk.CTk()
label = ctk.CTkLabel(root)
label.pack()
root.after(0, animate, 0)  # Start the animation
root.mainloop()
"""






# def Folder_result_window():


#     def getFolderPath_and_scan():
#         global folder_path
#         folder_path = ctk.filedialog.askdirectory()
#         if(folder_path):
#             print(folder_path)
            
#             progbar = ctk.CTkProgressBar(fold_win, orientation=ctk.HORIZONTAL, mode="determinate")
#             progbar.place(relx=0.5, rely=0.5, anchor='center')
            
#             fl = False
#             for iter in scanFolder(folder_path=folder_path):
#                 if not fl:
#                     num_files=iter
#                     fl = True
#                 if(type(iter) == int and iter > 0):
#                     progbar.set(iter/num_files)
#                 else:
#                     final_result = iter

#             for k,v in final_result.items():
#                 label1 = ctk.CTkLabel(fold_win, text= str(k))
#                 label2 = ctk.CTkLabel(fold_win, text= getFileStatus_from_code(v))
#                 label1.pack(anchor=ctk.W)
#                 label2.pack(anchor=ctk.E)

#     fold_win= ctk.CTk()
#     fold_win.geometry('500x300')
#     getFolderPath_and_scan()
#     fold_win.mainloop()
    
        

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


def unschedule_window():
    
    def unschedule_task(index):
            widget_to_be_destroyed = widget_list[index]
            path= widget_to_be_destroyed[0].cget('text')
            often = re.findall('\d+ (\w+)', widget_to_be_destroyed[1].cget('text'))[0]
            VA.delete_schedule(file_path=os.path.abspath(path))
            widget_to_be_destroyed[2].destroy()
            widget_to_be_destroyed[1].destroy()
            widget_to_be_destroyed[0].destroy()
            widget_to_be_destroyed[3].destroy()
    
    

    unsch_window = ctk.CTk()
    unsch_window.geometry('600x150')
    scheduled_tasks=parse_schedule()
    widget_list = []
    for index, task in enumerate(scheduled_tasks):
        task_frame = ctk.CTkFrame(unsch_window, width=570, height=50)
        task_frame.pack()
        task_path_label = ctk.CTkLabel(task_frame, text= task[0])
        task_path_label.place(relx=0.05, rely=0.5, anchor='w')
        task_duration = ctk.CTkLabel(task_frame, text=f"every {task[1]} "+f"{'Minutes' if task[2] == 'MINUTE' else 'Days'}")
        task_duration.place(relx=0.5, rely=0.5, anchor='w')
        delete_button = ctk.CTkButton(task_frame, text= 'Unschedule', fg_color='red', width=60, command= lambda index=index: unschedule_task(index))
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
            apply_button.configure(state=ctk.NORMAL)
        else:
            apply_button.configure(state=ctk.DISABLED)
        #print(fullCommand)
    
    def getFilePath():
        file_path = ctk.filedialog.askopenfilename()
        if(file_path):
            print(file_path)
            fullCommand['path'] = file_path
            fullCommand['folder'] = 0
            if(fullCommand['duration'] > 0):
                apply_button.configure(state=ctk.NORMAL)
            
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
                apply_button.configure(state=ctk.NORMAL)
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
        del_prev_button.configure(state=ctk.DISABLED if scheduled_tasks == -1 else ctk.NORMAL)
        #fullCommand['path']=''
        path_label.configure(text='')

    def unschedule():
        unschedule_window()
        scheduled_tasks = parse_schedule()
        del_prev_button.configure(state=ctk.DISABLED if scheduled_tasks == -1 else ctk.NORMAL)

        

    conf_window = ctk.CTk()
    conf_window.title('Configure Schedules')
    conf_window.geometry('550x400')
    select_file = ctk.CTkButton(conf_window, text='Select Target File', command=getFilePath, font=ctk.CTkFont(size=20, family='Helvetica', weight='bold'), height=35)
    select_file.place(relx=0.3, rely=0.3, anchor='center')
    select_folder = ctk.CTkButton(conf_window, text='Select Target Folder', command=getFolderPath, font=ctk.CTkFont(size=20, family='Helvetica', weight='bold'), height=35)
    select_folder.place(relx=0.7, rely=0.3, anchor='center')

    slider_frame= ctk.CTkFrame(conf_window, width=230, height=130, corner_radius=20)
    slider_frame.place(relx=0.5, rely=0.7, anchor='center')

    label=ctk.CTkLabel(slider_frame, text='Scan every')
    label.place(relx=0.5, rely=0.1, anchor='center')

    path_label = ctk.CTkLabel(conf_window, text='')
    path_label.place(relx=0.5, rely=0.4 ,anchor='center')

    text_above_slider = ctk.IntVar()

    slider_val = ctk.CTkLabel(conf_window, text='0', font=ctk.CTkFont(size=12, family='Helvetica'))
    slider_val.place(relx=0.5, rely=0.6, anchor='center')

    slider=ctk.CTkSlider(conf_window, from_=0, to=60, command=update_slider_val, variable=text_above_slider)
    slider.place(relx=0.5, rely=0.7, anchor='center')
    
    radio_var = ctk.IntVar(value=1)
    radiobutton_1 = ctk.CTkRadioButton(conf_window, text="Minutes", variable= radio_var, value=1)
    radiobutton_2 = ctk.CTkRadioButton(conf_window, text="Days", variable= radio_var, value=2)
    radiobutton_1.place(relx=0.45, rely=0.8, anchor='center')
    radiobutton_2.place(relx=0.65, rely=0.8, anchor='center')

    del_prev_button = ctk.CTkButton(conf_window, text='Un-schedule tasks',font=ctk.CTkFont(size=12, family='Helvetica'), state=ctk.DISABLED if scheduled_tasks == -1 else ctk.NORMAL, command=unschedule)
    del_prev_button.place(relx=0.5, rely=0.9, anchor='center')

    apply_button = ctk.CTkButton(conf_window, text='Apply',font=ctk.CTkFont(size=12, family='Helvetica'), width=80, state='disabled', command=schedule)
    apply_button.place(relx=0.8, rely=0.9, anchor='center')


    Cancel_button = ctk.CTkButton(conf_window, text='Cancel',font=ctk.CTkFont(size=12, family='Helvetica'), width=80, command=conf_window.destroy)
    Cancel_button.place(relx=0.2, rely=0.9, anchor='center')

    conf_window.mainloop()


def scanFile(file_path):
    return VA.FileScan(filePath=file_path)

def scanFolder(folder_path):
    return VA.Folder_Scan_with_metrics(folder=folder_path)


root= ctk.CTk()
root.title('Vigil-Anti')
root.geometry("800x600")


logo_image = ctk.CTkImage(light_image=Image.open(os.path.join(parent_Directory, 'icons','Black_VIGI.png')), dark_image=Image.open(os.path.join(parent_Directory, 'icons','Black_VIGI.png')), size=(800,1016))
logo_label = ctk.CTkLabel(root, width=400, height=400, image=logo_image, text='')
logo_label.place(relx=0.4, rely=0.0)

leftFrame = ctk.CTkFrame(root, width=370, height=600)
leftFrame.place(relx=0.0, rely=0.1)
scale_logo = ctk.CTkImage(light_image=Image.open(os.path.join(parent_Directory, 'icons','scales_vert.png')), dark_image=Image.open(os.path.join(parent_Directory, 'icons','scales_vert.png')), size=(1000,1000))
scale_lamp=ctk.CTkLabel(leftFrame, image=scale_logo)
#scale_lamp.place(relx=0.4, rely=0.4, anchor='center')
Tip_Of_the_day = ctk.CTkLabel(leftFrame, width=370, height=120, text="Tip of the day", font=ctk.CTkFont(size=30, family='Helvetica', weight='bold'))
Tip_Of_the_day.place(relx = 0.45, rely=0.1, anchor='center')
lamp_img=ctk.CTkImage(light_image=Image.open(os.path.join(parent_Directory, 'icons','yellowlamp.png')), dark_image=Image.open(os.path.join(parent_Directory, 'icons','yellowlamp.png')), size=(48,48))
lamp_label = ctk.CTkLabel(leftFrame, image=lamp_img, text='')
lamp_label.place(relx=0.85, rely=0.1, anchor='center')


tip_label = ctk.CTkLabel(leftFrame, text=secret_tip, font=ctk.CTkFont(size=15, family='Helvetica', weight='bold'))
tip_label.place(relx=0.062, rely=0.18, anchor='nw')
ayman_label = ctk.CTkLabel(leftFrame, text=Aymans_Word, font=ctk.CTkFont(size=17, family='Helvetica', weight='bold'))
ayman_label.place(relx=0.45, rely= 0.7, anchor='center')


vigilanti_place= ctk.CTkLabel(root, width=160,height=150, text='', font=ctk.CTkFont(size=30, family='Kozuka Gothic Pr6N B', weight='bold'), corner_radius=50, fg_color='blue')
vigilanti_place.place(relx=0.5, rely=0.075, anchor='s')

vigilanti_title= ctk.CTkLabel(root, height=30, text='Vigil-Anti', font=ctk.CTkFont(size=30, family='Kozuka Gothic Pr6N B', weight='bold'), fg_color='blue')
vigilanti_title.place(relx=0.5, rely=0.025, anchor='center')


frame_for_buttons = ctk.CTkFrame(root, width=600, height=42)
frame_for_buttons.place(relx=0.65, rely=0.7)
frame_for_schedule = ctk.CTkFrame(root, width=150, height=42)
frame_for_schedule.place(relx=0.69, rely=0.78)
scan_file_button = ctk.CTkButton(frame_for_buttons, text='Scan a File!', command=getFilePath_and_scan, width=100)
scan_file_button.grid(row=0, column=1)
space_padding= ctk.CTkFrame(frame_for_buttons, width=10, height=42)
space_padding.grid(row=0, column=2)
scan_folder_button = ctk.CTkButton(frame_for_buttons, text='Scan a Folder!', command=Folder_result_window, width=100)
scan_folder_button.grid(row=0, column=3)


Result_of_File_label = ctk.CTkLabel(root, text='',corner_radius=20, width=50, height=20)
Result_of_File_label.place(relx=0.785, rely=0.65, anchor='center')
Result_of_File_label.lower()

Configure_button = ctk.CTkButton(frame_for_schedule, text='Schedule Scans', command=ConfigureWindow)
Configure_button.grid(row=2,column=2)




root.mainloop()