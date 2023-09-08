from helpers import *
import os
import re
import numpy as np
import sys
from tqdm import tqdm


columns = ['pages', 'obj', 'endobj', 'stream', 'endstream', 'xref', 'trailer', 'startxref', 'encrypt', 'ObjStm', 'JS', 'Javascript', 'AA', 'OpenAction', 'Acroform', 'JBIG2Decode', 'RichMedia', 'launch', 'EmbeddedFile', 'XFA', 'Colors', 'header_regex_boolean', 'PDF_Version']


TEST_FOLDER_PATH = sys.argv[1]
MODEL_PATH = sys.argv[2]
path_to_script_folder = os.path.join(os.getcwd(), 'PDFid')

if(not (os.path.exists(TEST_FOLDER_PATH))):
    print(f"Path does not exist: {TEST_FOLDER_PATH}")
    exit()


all_preds = []
for file in tqdm(os.listdir(TEST_FOLDER_PATH)):
    file_path = os.path.join(TEST_FOLDER_PATH, file)
    feature_df = Extract_Features(file_path, path_to_script_folder)
    if(not(type(feature_df) == int and feature_df ==1)):
        feature_df = reorder_df(feature_df, [], columns)

        all_preds.append(test_on_file(feature_df, MODEL_PATH)[0])
    else:
        all_preds.append(1)

print(f"From all the {len(os.listdir(TEST_FOLDER_PATH))} Files, I detected {sum(all_preds)} as being malwares")