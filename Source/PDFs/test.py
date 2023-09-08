import os
import re
import pandas as pd
import numpy as np
from subprocess import run
import sys

from helpers import *


TARGET_PDF_PATH = sys.argv[1]

PATH_TO_PDFID_SCRIPT = os.path.join(sys.argv[2], 'pdfid.py')

LOCAL_PATH = os.getcwd()

OUTPUT_LOG_FILE_PATH = os.path.join(LOCAL_PATH, 'feature_output.txt')


if(os.path.exists(OUTPUT_LOG_FILE_PATH)):
    os.remove(OUTPUT_LOG_FILE_PATH)

run(['python', PATH_TO_PDFID_SCRIPT, TARGET_PDF_PATH, '-o', OUTPUT_LOG_FILE_PATH])



output_df = PDFid_Log_File_Parser(OUTPUT_LOG_FILE_PATH)

print (output_df)