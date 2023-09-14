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

def Folder_Scan(folder, EXEmodelpath=default_model_path_exe, PDFmodelpath=default_model_path_pdf, quiet=False, aggressive=False, verb=False, outfile='', no_ascii_art=False):
     folder_path = pathlib.Path(folder)
     allFile_paths= list(folder_path.glob('*'))
     all_results = {}
     for fp in allFile_paths:
          FileType = checkFileType(file_path=fp)
          if(FileType == 1):
               result = VE.Scan_File_exe(file_path=fp, model_path=EXEmodelpath, quiet=quiet, aggressive=aggressive, verb=verb, outfile=outfile, no_ascii_art=no_ascii_art)
               all_results[fp] = result
          elif(FileType == 2):
     
               result = VP.ScanFile_pdf(file_path=fp, modelPath=PDFmodelpath, quiet=quiet, aggressive=aggressive, verbose=verb, output=outfile, no_ascii_art=no_ascii_art)
               all_results[fp] = result
     return all_results





def FileScan(filePath, EXEmodelpath=default_model_path_exe, PDFmodelpath=default_model_path_pdf, quiet=False, aggressive=False, verb=False, outfile='', no_ascii_art=False):
     fileType = checkFileType(file_path=filePath)     
     if(fileType == 1):
          return VE.Scan_File_exe(file_path=filePath, model_path=EXEmodelpath, quiet=quiet, aggressive=aggressive, verb=verb, outfile=outfile, no_ascii_art=no_ascii_art)
     elif(fileType == 2):
          return VP.ScanFile_pdf(file_path=filePath, modelPath=PDFmodelpath, quiet=quiet, aggressive=aggressive, verbose=verb, output=outfile, no_ascii_art=no_ascii_art)
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
               if(re.findall(os.path.split(file_path)[1] , line)):
                    continue
               modified.append(line)
          with open(os.path.join(current_directory, 'Config', 'config.txt'), 'w') as f:
               f.write('\n'.join(modified))
     all_jobs = re.findall('TaskName:.*(Vigil_Anti_\d+)', run(['schtasks', '/query', '/fo', 'LIST'], capture_output=True, text=True).stdout)
     if(all_jobs):
          for job in all_jobs:
               run([ 'schtasks', '/delete', '/tn' ,job, '/f'])
     



def create_script(file_path, folder_scan):
     name = re.sub("[^\w]", '_', rf"{file_path}")
     if(folder_scan):
          script_contents = f'cd /d "{current_directory}"\npython "Vigil_Anti.py" "{file_path}" -q -c -f -o {os.path.join(current_directory, "Config",f"Output_{name}.txt")}'
     else:
          script_contents = f'cd /d "{current_directory}"\npython "Vigil_Anti.py" "{file_path}" -q -c -o {os.path.join(current_directory,"Config", f"Output_{name}.txt")}'
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
          run([f'schtasks', '/create','/sc', time_span, '/mo' ,n, '/f', '/tn' ,f"Vigil_Anti_{i}" ,"/tr", str(create_script(file_path=file_path, folder_scan=folder_scan))])
          run(['schtasks' ,'/run', '/tn' ,f"Vigil_Anti_{i}"])

def CleanOutput(file_path, result, outfile):
     if (type(result) != dict):
          with open(outfile,'w') as f:
               f.write(f"{file_path}            {'Safe' if result == 0 else 'Malicious'}")
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