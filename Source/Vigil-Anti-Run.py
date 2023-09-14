import os
import re, pickle
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

def getFileStatus_from_code(return_code):
    if return_code ==0:
        return ("Safe")
    elif return_code ==1:
        return ("Malicious")
    elif return_code == -1:
        return ("No Data")
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

def getFilePath():
    global file_path
    file_path = ctk.filedialog.askopenfilename()
    if(file_path):
        print(file_path)
        result = scanFile(file_path=file_path)
        label = ctk.CTkLabel(root, text= getFileStatus_from_code(result))
        label.pack()
        Display_Single_Result(file_path=file_path, result=getFileStatus_from_code(result))

def getFolderPath():
    global folder_path
    folder_path = ctk.filedialog.askdirectory()
    if(folder_path):
        print(folder_path)
        result=scanFolder(folder_path=folder_path)
        for k,v in result.items():
            label1 = ctk.CTkLabel(root, text= str(k))
            label2 = ctk.CTkLabel(root, text= getFileStatus_from_code(v))
            label1.pack(anchor=ctk.W)
            label2.pack(anchor=ctk.E)


def ConfigureWindow():
    conf_window = ctk.CTk()
    select_file = ctk.CTkButton(conf_window, text='Select Target File', command=getFilePath)
    select_file.pack()
    select_folder = ctk.CTkButton(conf_window, text='Select Target File', command=getFolderPath)
    select_folder.pack()
    label=ctk.CTkLabel(conf_window, text='Scan every')
    label.pack()
    slider=ctk.CTkSlider(conf_window)
    slider.pack()
    print(slider.get())
    radio_button1=ctk.CTkRadioButton(conf_window, value=2)
    
    radio_button1.pack()
    
    conf_window.mainloop()


def scanFile(file_path):
    return VA.FileScan(filePath=file_path)

def scanFolder(folder_path):
    return VA.Folder_Scan(folder=folder_path)


root= ctk.CTk()
root.geometry("800x600")


logo_image = ctk.CTkImage(light_image=Image.open(os.path.join(parent_Directory, 'icons','Black_VIGI.png')), dark_image=Image.open(os.path.join(parent_Directory, 'icons','Black_VIGI.png')), size=(800,1016))
logo_label = ctk.CTkLabel(root, width=400, height=400, image=logo_image, text='')
logo_label.place(relx=0.4, rely=0.0)

leftFrame = ctk.CTkFrame(root, width=370, height=600)
leftFrame.place(relx=0.0, rely=0.1)
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
scan_file_button = ctk.CTkButton(frame_for_buttons, text='Scan a File!', command=getFilePath, width=100)
scan_file_button.grid(row=0, column=1)
space_padding= ctk.CTkFrame(frame_for_buttons, width=10, height=42)
space_padding.grid(row=0, column=2)
scan_folder_button = ctk.CTkButton(frame_for_buttons, text='Scan a Folder!', command=getFolderPath, width=100)
scan_folder_button.grid(row=0, column=3)

Configure_button = ctk.CTkButton(frame_for_schedule, text='Schedule Scans', command=ConfigureWindow)
Configure_button.grid(row=2,column=2)




root.mainloop()