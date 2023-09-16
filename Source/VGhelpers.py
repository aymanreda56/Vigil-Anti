import os
import sys
import re
from exiftool import ExifToolHelper
sys.path.append('Vigi_EXE')
sys.path.append('Vigi_PDF')
from argparse import ArgumentParser, Namespace
import Vigi_EXE.Vigi_EXE_lib as VE
import Vigi_PDF.Vigi_PDF_lib as VP
import glob, pathlib
from subprocess import run
import ctypes

# import win10toast
from win10toast import ToastNotifier


# from win32api import *
# from win32gui import *
# import win32con
# import sys, os
# import struct
# import time


current_directory = os.path.split(os.path.realpath(__file__))[0]
parent_directory = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
ExifTool_path = os.path.join(parent_directory, 'exiftool')
os.environ['PATH'] += ';'+ExifTool_path

models_path_exe = os.path.join(current_directory,"Vigi_EXE",'models')
models_path_pdf = os.path.join(current_directory,"Vigi_PDF",'models')
default_model_path_pdf = os.path.join(models_path_pdf, 'rf.pkl')
default_model_path_exe = os.path.join(models_path_exe, 'rf.pkl')



class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def checkFileType(file_path):
     #ee = ExifToolHelper()
     try:
          metadata = ExifToolHelper().get_metadata(file_path)
          
          for i, d in enumerate(metadata):
               if 'File:FileType' in d.keys():
                    fileTypeDict = d
                    break
          if(re.findall('win', fileTypeDict['File:FileType'], re.IGNORECASE)):
               return 1
          elif(re.findall('pdf', fileTypeDict['File:FileType'], re.IGNORECASE)):
               return 2
          else:
               print(color.BOLD+ color.YELLOW + f"File {file_path} is not a windows PE !!"  + color.END)
               return 0
     except:
          print(color.BOLD+ color.PURPLE + f"File {file_path} is Corrupt, delete it if you suspect it!"  + color.END)
          return -1

def Folder_Scan(folder, EXEmodelpath=default_model_path_exe, PDFmodelpath=default_model_path_pdf, quiet=False, aggressive=False, verb=False, outfile='', no_ascii_art=False, notify=False):
     folder_path = pathlib.Path(folder)
     allFile_paths= list(folder_path.glob('*'))
     all_results = {}
     for fp in allFile_paths:
          FileType = checkFileType(file_path=fp)
          result = -1
          if(FileType == 1):
               result = VE.Scan_File_exe(file_path=fp, model_path=EXEmodelpath, quiet=quiet, aggressive=aggressive, verb=verb, outfile=outfile, no_ascii_art=no_ascii_art)
               all_results[fp] = result
          elif(FileType == 2):
               result = VP.ScanFile_pdf(file_path=fp, modelPath=PDFmodelpath, quiet=quiet, aggressive=aggressive, verbose=verb, output=outfile, no_ascii_art=no_ascii_art)
               all_results[fp] = result
          if(notify and fp in all_results.keys() and all_results[fp] == 1):
               #publish a notification
               #publish a notification
               # create an object to ToastNotifier class
               n = ToastNotifier()
               n.show_toast("Vigil-Anti", f'File {str(fp)} is found Malicious', duration = 5,
               icon_path =os.path.join(parent_directory, 'icons', 'logo_white.ico'))
     return all_results

def Folder_Scan_with_metrics(folder, EXEmodelpath=default_model_path_exe, PDFmodelpath=default_model_path_pdf, quiet=False, aggressive=False, verb=False, outfile='', no_ascii_art=False):
     folder_path = pathlib.Path(folder)
     allFile_paths= list(folder_path.glob('*'))
     all_results = {}
     yield len(allFile_paths)
     for i, fp in enumerate(allFile_paths):
          FileType = checkFileType(file_path=fp)
          if(FileType == 1):
               result = VE.Scan_File_exe(file_path=fp, model_path=EXEmodelpath, quiet=quiet, aggressive=aggressive, verb=verb, outfile=outfile, no_ascii_art=no_ascii_art)
               all_results[fp] = result
          elif(FileType == 2):
     
               result = VP.ScanFile_pdf(file_path=fp, modelPath=PDFmodelpath, quiet=quiet, aggressive=aggressive, verbose=verb, output=outfile, no_ascii_art=no_ascii_art)
               all_results[fp] = result
          elif(FileType == -1):
               all_results[fp] = -1
          yield i
     yield all_results



def FileScan(filePath, EXEmodelpath=default_model_path_exe, PDFmodelpath=default_model_path_pdf, quiet=False, aggressive=False, verb=False, outfile='', no_ascii_art=False, notify=False):
     fileType = checkFileType(file_path=filePath)     
     if(fileType == 1):
          res= VE.Scan_File_exe(file_path=filePath, model_path=EXEmodelpath, quiet=quiet, aggressive=aggressive, verb=verb, outfile=outfile, no_ascii_art=no_ascii_art)
          if(notify and res == 1):
               #publish a notification
               # create an object to ToastNotifier class
               n = ToastNotifier()
               n.show_toast("Vigil-Anti", f'File {filePath} is found Malicious', duration = 5,
               icon_path =os.path.join(parent_directory, 'icons', 'logo_white.ico'))
          return res
     elif(fileType == 2):
          res= VP.ScanFile_pdf(file_path=filePath, modelPath=PDFmodelpath, quiet=quiet, aggressive=aggressive, verbose=verb, output=outfile, no_ascii_art=no_ascii_art)
          if(notify and res == 1):
               #publish a notification
               #publish a notification
               # create an object to ToastNotifier class
               n = ToastNotifier()
               n.show_toast("Vigil-Anti", f'File {filePath} is found Malicious', duration = 5,
               icon_path =os.path.join(parent_directory, 'icons', 'logo_white.ico'))
          return res
     elif(fileType == 0):
          print(f"File is not a windows PE nor PDF, wait for other modules for Vigil-Anti to support it")
          return -1
     else:
          print(f"File is Corrupt, delete it if you suspect it!")
          return -1




def schedule_minutes(file_path, N_minutes):
     delete_schedule(file_path)
     if(not os.path.exists(os.path.join(current_directory, 'Config'))):
          os.mkdir('Config')
     with open(os.path.join(current_directory, 'Config', 'config.txt'), 'a') as f:
          f.write(f"{file_path}@@{N_minutes}::mins\n")

def schedule_days(file_path, N_days):
     delete_schedule(file_path)
     if(not os.path.exists(os.path.join(current_directory, 'Config'))):
          os.mkdir('Config')
     with open(os.path.join(current_directory, 'Config', 'config.txt'), 'a') as f:
          f.write(f"{file_path}@@{N_days}::days\n")

def delete_schedule(file_path):
     if(not os.path.isdir(os.path.join(current_directory, 'Config'))):
          return
     if(not os.path.isfile(os.path.join(current_directory, 'Config', 'config.txt'))):
          return
     with open(os.path.join(current_directory, 'Config', 'config.txt'), 'r') as f:
          scheduleds = f.readlines()
     if(scheduleds):
          modified = []
          for line in scheduleds:
               lin = re.sub('\n', '', line)
               smolPath = re.findall('(.*)@@', lin)[0]
               if(os.path.abspath(file_path) == os.path.abspath(smolPath)):
                    continue
               modified.append(re.sub('\n','',line))
          with open(os.path.join(current_directory, 'Config', 'config.txt'), 'w') as f:
               if(modified):
                    f.write('\n'.join(modified))
                    f.write('\n')
     all_jobs = re.findall('TaskName:.*(Vigil_Anti_\d+)', run(['schtasks', '/query', '/fo', 'LIST'], capture_output=True, text=True).stdout)
     if(all_jobs):
          for job in all_jobs:
               run([ 'schtasks', '/delete', '/tn' ,job, '/f'])



def create_script(file_path, folder_scan):
     name = re.sub("[^\w]", '_', rf"{file_path}")
     if(folder_scan):
          script_contents = f'cd /d "{current_directory}"\npython "Vigil_Anti.py" "{file_path}" -q -N -c -f -o "{os.path.join(current_directory, "Config",f"Output_{name}.txt")}"'
     else:
          script_contents = f'cd /d "{current_directory}"\npython "Vigil_Anti.py" "{file_path}" -q -N -c -o "{os.path.join(current_directory,"Config", f"Output_{name}.txt")}"'
     with open(os.path.join(current_directory, "Config", f'task_{name}.bat'), 'w') as f:
          f.write(script_contents)
     return  os.path.join(current_directory, "Config", f'task_{name}.bat')


def run_scheduler(folder_scan):
     if(not os.path.exists(os.path.join(current_directory, 'Config'))):
          return
     with open(os.path.join(current_directory, 'Config', 'config.txt'), 'r') as f:
          scheduleds = f.readlines()
     for i, lin in enumerate(scheduleds):
          line = re.sub(r'\n', '', lin)
          file_path = re.findall('.*@@', line)
          if(not file_path): print('\n\n\nEEEERRRRRRRRRRROOOOOOOOOOOOR in scheduler')
          file_path = file_path[0][:-2]
          n = re.findall('@@\d+::', line)
          n = n[0][2:-2]
          minutes_flag = True if re.findall('::mins', line) else False
          days_flag = True if re.findall('::days', line) else False
          time_span = 'DAILY' if days_flag else 'MINUTE'
          if(is_user_admin()):
               print('admin privilege')
               create_task = run([f'schtasks', '/create','/sc', time_span, '/mo' ,n,'/RL','HIGHEST', '/f', '/tn' ,f"Vigil_Anti_{i}" ,"/tr", str(create_script(file_path=file_path, folder_scan=folder_scan))], capture_output=True, text=True)
          else:
               print('task as a normal user')
               create_task = run([f'schtasks', '/create','/sc', time_span, '/mo' ,n, '/f', '/tn' ,f"Vigil_Anti_{i}" ,"/tr", str(create_script(file_path=file_path, folder_scan=folder_scan))], capture_output=True, text=True)

          run(['schtasks' ,'/run', '/tn' ,f"Vigil_Anti_{i}"])





class AdminStateUnknownError(Exception):
    """Cannot determine whether the user is an admin."""
    pass

def is_user_admin():
    try:
        return os.getuid() == 0
    except AttributeError:
        pass
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() == 1
    except AttributeError:
        return False








def CleanOutput(file_path, result, outfile):
     if (type(result) != dict):
          with open(outfile,'w') as f:
               f.write(f"               Vigil_Anti     By    Ayman Reda\n{file_path}            {'Safe' if result == 0 else 'Malicious'}")
     elif(type(result) == dict):
          result_string = []
          for k,v in result.items():
               #result_string.append(f"{str(k)}              {'Safe' if v == 0 else 'Malicious'}")
               #result_string.append("{:<100}{:<50}".format(''.join(str(k)), 'Safe' if v == 0 else 'Malicious'))
               fi = '{:<100}'.format(str(k))
               st = 'Safe' if v == 0 else 'Malicious'
               result_string.append(fi+ st)
          with open(outfile,'w') as f:
               f.write('               Vigil_Anti     By    Ayman Reda\n')
          with open(outfile,'a') as f:
               f.write('\n'.join(result_string))



# class WindowsBalloonTip:
#     def __init__(self, title, msg):
#         message_map = {
#                 win32con.WM_DESTROY: self.OnDestroy,
#         }
#         # Register the Window class.
#         wc = WNDCLASS()
#         hinst = wc.hInstance = GetModuleHandle(None)
#         wc.lpszClassName = "PythonTaskbar"
#         wc.lpfnWndProc = message_map # could also specify a wndproc.
#         classAtom = RegisterClass(wc)
#         # Create the Window.
#         style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
#         self.hwnd = CreateWindow( classAtom, "Taskbar", style, \
#                 0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, \
#                 0, 0, hinst, None)
#         UpdateWindow(self.hwnd)
#         iconPathName = os.path.abspath(os.path.join( sys.path[0], "balloontip.ico" ))
#         icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
#         try:
#            hicon = LoadImage(hinst, iconPathName, \
#                     win32con.IMAGE_ICON, 0, 0, icon_flags)
#         except:
#           hicon = LoadIcon(0, win32con.IDI_APPLICATION)
#         flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
#         nid = (self.hwnd, 0, flags, win32con.WM_USER+20, hicon, "tooltip")
#         Shell_NotifyIcon(NIM_ADD, nid)
#         Shell_NotifyIcon(NIM_MODIFY, \
#                          (self.hwnd, 0, NIF_INFO, win32con.WM_USER+20,\
#                           hicon, "Balloon  tooltip",title,200,msg))
#         # self.show_balloon(title, msg)
#         time.sleep(10)
#         DestroyWindow(self.hwnd)
#     def OnDestroy(self, hwnd, msg, wparam, lparam):
#         nid = (self.hwnd, 0)
#         Shell_NotifyIcon(NIM_DELETE, nid)
#         PostQuitMessage(0) # Terminate the app.
# def balloon_tip(title, msg):
#     w=WindowsBalloonTip(msg, title)