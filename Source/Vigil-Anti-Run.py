import os
import re
import sys
sys.path.append('Vigi_EXE')
sys.path.append('Vigi_PDF')
import VGhelpers as VA




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





def scanFile(file_path):
    return VA.FileScan(filePath=file_path)

def scanFolder(folder_path):
    return VA.Folder_Scan(folder=folder_path)


root= ctk.CTk()
root.geometry("800x600")

scan_file_button = ctk.CTkButton(root, text='Scan a File!', command=getFilePath)
scan_file_button.pack()
scan_folder_button = ctk.CTkButton(root, text='Scan a Folder!', command=getFolderPath)
scan_folder_button.pack()




root.mainloop()