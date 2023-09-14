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

def Folder_Scan(folder, EXEmodelpath=default_model_path_exe, PDFmodelpath=default_model_path_pdf, quiet=False, aggressive=False, verb=False, outfile=''):
     folder_path = pathlib.Path(folder)
     allFile_paths= list(folder_path.glob('*'))
     all_results = {}
     for fp in allFile_paths:
          FileType = checkFileType(file_path=fp)
          if(FileType == 1):
               result = VE.Scan_File_exe(file_path=fp, model_path=EXEmodelpath, quiet=quiet, aggressive=aggressive, verb=verb, outfile=outfile)
               all_results[fp] = result
          elif(FileType == 2):
               print("here")
               result = VP.ScanFile_pdf(file_path=fp, modelPath=PDFmodelpath, quiet=quiet, aggressive=aggressive, verbose=verb, output=outfile)
               all_results[fp] = result
     return all_results

def FileScan(filePath, EXEmodelpath=default_model_path_exe, PDFmodelpath=default_model_path_pdf, quiet=False, aggressive=False, verb=False, outfile=''):
     fileType = checkFileType(file_path=filePath)     
     if(fileType == 1):
          print("here")
          return VE.Scan_File_exe(file_path=filePath, model_path=EXEmodelpath, quiet=quiet, aggressive=aggressive, verb=verb, outfile=outfile)
     elif(fileType == 2):
          print("here")
          return VP.ScanFile_pdf(file_path=filePath, modelPath=PDFmodelpath, quiet=quiet, aggressive=aggressive, verbose=verb, output=outfile)
     elif(fileType == 0):
          print(f"File is not a windows PE nor PDF, wait for other modules for Vigil-Anti to support it")
          return -1
     else:
          print(f"File is Corrupt, delete it if you suspect it!")
          return -1
