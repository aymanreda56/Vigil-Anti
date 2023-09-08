import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import re
import pickle
from subprocess import run, DEVNULL, STDOUT




def prettyPrint_DF (df):
    for col in df.columns:
        print(f"----------------------------- COL: {col} --------------------------------")
        try:
            print(f"{str(col)} min:  {df[col].min()}           max: {df[col].max()}")
            print(f"Unique values are: {df[col].unique()}")
                
        except:
            print(f"ERRROR in col: {col}")
            print(f"Has nans: {df[col].hasnans}")
        
        print(f"\n\nColumn Type: {df[col].dtype}\n\n\n\n")



def Cleanse_DataFrame(df):
    df.dropna(inplace=True)


    # isEncrypted
    df = df.drop(df[df['isEncrypted'] == 2].index)
    df = df.drop(df[df['isEncrypted'] == 3].index)
    df = df.drop(df[df['isEncrypted'] == 4].index)

    # pdfsize
    df["pdfsize"] = df["pdfsize"].astype(int)


    # text
    df = df.drop(df[df['text'] == '0'].index)

    # pages
    df['pages'] = df['pages'].astype(int)

    # images
    df['images'] = df['images'].astype(int)

    # metadata size
    df["metadata size"] = df["metadata size"].astype(int)

    # header
    df['header_regex_boolean'] = df.header
    regex_pattern = '^\\t%PDF-\d\.\d$'
    # Apply regex pattern to each column
    df['header_regex_boolean'] = df['header_regex_boolean'].apply(lambda x: True if re.findall(regex_pattern,str(x)) else False)
    df['header_regex_boolean'] = df['header_regex_boolean'].astype(bool)


    df['PDF_Version'] = df.header
    regex_pattern = '^\\t%PDF-(\d\.\d)$'
    # Apply regex pattern to each column
    df['PDF_Version'] = df['PDF_Version'].apply(lambda x: re.findall(regex_pattern,str(x))[0] if re.findall(regex_pattern,str(x)) else '-1')
    df['PDF_Version'] = df['PDF_Version'].astype(float)
    
    


    # obj
    df['obj_temp'] = df.obj
    regex_pattern = '[a-zA-Z]'
    # Apply regex pattern to each column
    df['obj_temp'] = df['obj_temp'].apply(lambda x: '-1' if re.findall(regex_pattern,str(x)) else re.findall('-?\d+',str(x))[0])
    df['obj_temp'] = df['obj_temp'].astype(int)
    df.obj = df['obj_temp']
    df.drop("obj_temp", axis=1, inplace=True)


    # endobj
    df['endobj_temp'] = df.endobj
    regex_pattern = '[a-zA-Z]'
    # Apply regex pattern to each column
    df['endobj_temp'] = df['endobj_temp'].apply(lambda x: '-1' if re.findall(regex_pattern,str(x)) else re.findall('-?\d+',str(x))[0])
    df['endobj_temp'] = df['endobj_temp'].astype(int)
    df.endobj = df['endobj_temp']
    df.drop("endobj_temp", axis=1, inplace=True)
    
    

    # stream
    df['stream'] = df['stream'].astype(int)

    # endstream
    df['endstream_temp'] = df.endstream
    regex_pattern = '[a-z\)A-Z\(]'
    # Apply regex pattern to each column
    df['endstream_temp'] = df['endstream_temp'].apply(lambda x: '-1' if re.findall(regex_pattern,str(x)) else re.findall('-?\d+',str(x))[0])
    df['endstream_temp'] = df['endstream_temp'].astype(int)
    df.endstream = df['endstream_temp']
    df.drop("endstream_temp", axis=1, inplace=True)

    # title characters
    df["title characters"] = df["title characters"].astype(int)

    # Colors
    df["Colors"] = df["Colors"].astype(int)


    # xref
    df['xref_temp'] = df.xref
    regex_pattern = '[a-z\)A-Z\(]'
    # Apply regex pattern to each column
    df['xref_temp'] = df['xref_temp'].apply(lambda x: '-1' if re.findall(regex_pattern,str(x)) else re.findall('-?\d+',str(x))[0])
    df['xref_temp'] = df['xref_temp'].astype(int)
    df.xref = df['xref_temp']
    df.drop("xref_temp", axis=1, inplace=True)

    # startxref
    df['startxref_temp'] = df.startxref
    regex_pattern = '[a-z\)A-Z\(]'
    # Apply regex pattern to each column
    df['startxref_temp'] = df['startxref_temp'].apply(lambda x: '-1' if re.findall(regex_pattern,str(x)) else re.findall('-?\d+',str(x))[0])
    df['startxref_temp'] = df['startxref_temp'].astype(int)
    df.startxref = df['startxref_temp']
    df.drop("startxref_temp", axis=1, inplace=True)


    # trailer
    df['trailer'] = df['trailer'].astype(int)

    # xref Length
    df["xref Length"] = df["xref Length"].astype(int)

    # pageno
    df['pageno_temp'] = df.pageno
    regex_pattern = '[a-z\)A-Z\(]'
    # Apply regex pattern to each column
    df['pageno_temp'] = df['pageno_temp'].apply(lambda x: '-1' if re.findall(regex_pattern,str(x)) else re.findall('-?\d+',str(x))[0])
    df['pageno_temp'] = df['pageno_temp'].astype(int)
    df.pageno = df['pageno_temp']
    df.drop("pageno_temp", axis=1, inplace=True)



    # encrypt
    df['encrypt_temp'] = df.encrypt
    regex_pattern = '[10\-]'
    # Apply regex pattern to each column
    df['encrypt_temp'] = df['encrypt_temp'].apply(lambda x: re.findall('-?\d+',str(x))[0] if re.findall(regex_pattern,str(x)) else '-1')
    df['encrypt_temp'] = df['encrypt_temp'].astype(int)
    df.encrypt = df['encrypt_temp']
    df.drop("encrypt_temp", axis=1, inplace=True)


    # ObjStm
    df["ObjStm"] = df["ObjStm"].astype(int)

    #JS
    df['JS_temp'] = df.JS
    regex_pattern = '[a-z\)A-Z\(]'
    # Apply regex pattern to each column
    df['JS_temp'] = df['JS_temp'].apply(lambda x: '-1' if re.findall(regex_pattern,str(x)) else re.findall('-?\d+',str(x))[0])
    df['JS_temp'] = df['JS_temp'].astype(int)
    df.JS = df['JS_temp']
    df.drop("JS_temp", axis=1, inplace=True)

    # Javascript
    df['Javascript_temp'] = df.Javascript
    regex_pattern = '[^0-9\-]'
    # Apply regex pattern to each column
    df['Javascript_temp'] = df['Javascript_temp'].apply(lambda x: '-1' if re.findall(regex_pattern,str(x)) else re.findall('-?\d+',str(x))[0])
    df['Javascript_temp'] = df['Javascript_temp'].astype(int)
    df.Javascript = df['Javascript_temp']
    df.drop("Javascript_temp", axis=1, inplace=True)

    # AA
    df['AA_temp'] = df.AA
    regex_pattern = '[^0-9\-]'
    # Apply regex pattern to each column
    df['AA_temp'] = df['AA_temp'].apply(lambda x: '-1' if re.findall(regex_pattern,str(x)) else re.findall('-?\d+',str(x))[0])
    df['AA_temp'] = df['AA_temp'].astype(int)
    df.AA = df['AA_temp']
    df.drop("AA_temp", axis=1, inplace=True)

    # OpenAction
    df['OpenAction_temp'] = df.OpenAction
    regex_pattern = '[10\-]'
    # Apply regex pattern to each column
    df['OpenAction_temp'] = df['OpenAction_temp'].apply(lambda x: re.findall('-?\d+',str(x))[0] if re.findall(regex_pattern,str(x)) else '-1')
    df['OpenAction_temp'] = df['OpenAction_temp'].astype(int)
    df.OpenAction = df['OpenAction_temp']
    df.drop("OpenAction_temp", axis=1, inplace=True)

    # Acroform
    df['Acroform_temp'] = df.Acroform
    regex_pattern = '[^0-9\-]'
    # Apply regex pattern to each column
    df['Acroform_temp'] = df['Acroform_temp'].apply(lambda x: '-1' if re.findall(regex_pattern,str(x)) else re.findall('-?\d+',str(x))[0])
    df['Acroform_temp'] = df['Acroform_temp'].astype(int)
    df.Acroform = df['Acroform_temp']
    df.drop("Acroform_temp", axis=1, inplace=True)



    # JBIG2Decode
    df['JBIG2Decode_temp'] = df.JBIG2Decode
    regex_pattern = '[^0-9\-]'
    # Apply regex pattern to each column
    df['JBIG2Decode_temp'] = df['JBIG2Decode_temp'].apply(lambda x: '-1' if re.findall(regex_pattern,str(x)) else re.findall('-?\d+',str(x))[0])
    df['JBIG2Decode_temp'] = df['JBIG2Decode_temp'].astype(int)
    df.JBIG2Decode = df['JBIG2Decode_temp']
    df.drop("JBIG2Decode_temp", axis=1, inplace=True)

    # RichMedia
    df['RichMedia_temp'] = df.RichMedia
    regex_pattern = '[10\-]'
    # Apply regex pattern to each column
    df['RichMedia_temp'] = df['RichMedia_temp'].apply(lambda x: re.findall('-?\d+',str(x))[0] if re.findall(regex_pattern,str(x)) else '-1')
    df['RichMedia_temp'] = df['RichMedia_temp'].astype(int)
    df.RichMedia = df['RichMedia_temp']
    df.drop("RichMedia_temp", axis=1, inplace=True)


    # launch
    df['launch_temp'] = df.launch
    regex_pattern = '[a-z)(A-Z_-]'
    # Apply regex pattern to each column
    df['launch_temp'] = df['launch_temp'].apply(lambda x: "-1" if re.findall(regex_pattern,str(x)) else str(x))
    df['launch_temp'] = df['launch_temp'].astype(int)
    df.launch = df['launch_temp']
    df.drop("launch_temp", axis=1, inplace=True)

    # EmbeddedFile
    df['EmbeddedFile_temp'] = df.EmbeddedFile
    regex_pattern = '[^0-9\-]'
    # Apply regex pattern to each column
    df['EmbeddedFile_temp'] = df['EmbeddedFile_temp'].apply(lambda x: '-1' if re.findall(regex_pattern,str(x)) else re.findall('-?\d+',str(x))[0])
    df['EmbeddedFile_temp'] = df['EmbeddedFile_temp'].astype(int)
    df.EmbeddedFile = df['EmbeddedFile_temp']
    df.drop("EmbeddedFile_temp", axis=1, inplace=True)


    #XFA
    df['XFA_temp'] = df.XFA
    regex_pattern = '[10\-]'
    # Apply regex pattern to each column
    df['XFA_temp'] = df['XFA_temp'].apply(lambda x: re.findall('-?\d+',str(x))[0] if re.findall(regex_pattern,str(x)) else '-1')
    df['XFA_temp'] = df['XFA_temp'].astype(int)
    df.XFA = df['XFA_temp']
    df.drop("XFA_temp", axis=1, inplace=True)


    # Class
    df.loc[df["Class"] == "Malicious", "Class"] = 1
    df.loc[df["Class"] == "Benign", "Class"] = 0
    df["Class"] = df["Class"].astype(bool)


    # Drop the file name column
    df.drop("Fine name", axis=1, inplace=True)


    # Drop the header column, it is useless now
    df.drop ('header', axis=1, inplace=True)
    

    return df
    

def Remove_Complex_Features(df):
    complex_features = ['isEncrypted'
        , 'embedded files'
        , 'text'
        , 'pdfsize' 
        , 'metadata size' 
        , 'xref Length'
        , 'title characters' 
        , 'images'  
        , 'pageno'
    ]

    df.drop(complex_features, axis=1, inplace=True)
    return df




def PDFid_Log_File_Parser(file):
    contents = []
    try:
        if(os.path.exists(file)):
            with open(file, 'r') as f:
                contents = f.readlines()
        else:
            print(f"ERRRRROR in Parsing the log file {file}: FILE NOT FOUND")
            return -1
    except:
        print(f"ERRRRROR in Parsing the log file {file}")
        return -1

    #discard the last blank line
    contents.pop()
    
    

    # delete the first line
    contents.pop(0)

    output_dictionary = {}

    # From the first line containing "PDF header" we will extract its value directly so as not to cause any troubles in the future
    try:
        output_dictionary['header'] = re.findall( "%PDF\-\d\.\d?", contents[0])[0]
        contents.pop(0) #remove this line after we took what we need from it
    except:
        print(f"ERRRRROR in Parsing the log file {file}\nThe First line which contains the PDF header is corrupt: {contents[0]}")
        Check_Corrupted_File (file, '', 1, contents[0])
        output_dictionary['header'] = -1
        contents.pop(0) #remove this line after we took what we need from it
        #return -1
    
    # From the last line, we want to read the Colors field without causing any troubles in the future
    try:
        output_dictionary['Colors'] = re.findall( "\s\s\s\s+(\d+)", contents[-1])[0]
        contents.pop() #remove this last line after we took what we need from it
    except:
        print(f"ERRRRROR in Parsing the log file {file}\nThe Last line which contains Colors field is corrupt: {contents}")
        if(contents ==[]):
            Check_Corrupted_File (file, '', 2, '')
        return -1
    

    # Now parse the rest of the fields normally
    for line in contents:
        lin_cpy = line
        if(re.findall("\(.*\)", lin_cpy)):
            lin_cpy = re.sub('\(.*\)', '', lin_cpy)
        matches = re.findall("\w+", lin_cpy)
        if(len(matches) == 2):
            output_dictionary[matches[0]] = matches[1]
        else:
            print(f"ERRRRROR in Parsing the log file {file}\nMultiple matches in regex in the same line, required to exactly have 2 elements\n the line: {line}\n matches: {matches}")
            return -1
    

    #Renaming the keys
    output_dictionary['pages'] = output_dictionary['Page']
    del output_dictionary["Page"]
    output_dictionary['encrypt'] = output_dictionary['Encrypt']
    del output_dictionary["Encrypt"]
    output_dictionary['Acroform'] = output_dictionary['AcroForm']
    del output_dictionary["AcroForm"]
    output_dictionary['launch'] = output_dictionary['Launch']
    del output_dictionary["Launch"]
    output_dictionary['Javascript'] = output_dictionary['JavaScript']
    del output_dictionary["JavaScript"]

    # Deleting the URI field becuase we didn't train on it (We Don't have URI field in our dataset)
    del output_dictionary["URI"]


    # Fix the header entry
    try:
        if output_dictionary['header'] != -1 or output_dictionary['header'] != '-1':
            output_dictionary['PDF_Version'] = re.findall('\d\.\d?', output_dictionary['header'])[0]
            output_dictionary['header_regex_boolean'] = True
        
        else:
            output_dictionary['PDF_Version'] = -1.0
            output_dictionary['header_regex_boolean'] = False
    except:
        output_dictionary['PDF_Version'] = -1.0
        output_dictionary['header_regex_boolean'] = False
    
    del(output_dictionary['header'])


    # Finally, construct the dataframe and return it
    output_df = pd.DataFrame.from_dict(output_dictionary, orient='index').transpose()

    # for my OCD...
    output_df['PDF_Version'] = output_df['PDF_Version'].astype(float)
    output_df['header_regex_boolean'] = output_df['header_regex_boolean'].astype(bool)

    return output_df





def Extract_Features(file_path, path_to_script_folder):
    TARGET_PDF_PATH = file_path

    PATH_TO_PDFID_SCRIPT = os.path.join(path_to_script_folder, 'pdfid.py')

    LOCAL_PATH = os.getcwd()

    OUTPUT_LOG_FILE_PATH = os.path.join(LOCAL_PATH, 'feature_output.txt')


    if(os.path.exists(OUTPUT_LOG_FILE_PATH)):
        os.remove(OUTPUT_LOG_FILE_PATH)

    run(['python', PATH_TO_PDFID_SCRIPT, TARGET_PDF_PATH, '-o', OUTPUT_LOG_FILE_PATH])#, stdout=DEVNULL, stderr=STDOUT)

    output_df = PDFid_Log_File_Parser(OUTPUT_LOG_FILE_PATH)
    if(type(output_df) == int):
        print(f"Error During File Parsing: {file_path} : File might be a malware, or is not a PDF aslan!!")
        os.remove(OUTPUT_LOG_FILE_PATH)
        return 1
    os.remove(OUTPUT_LOG_FILE_PATH)
    return output_df


def reorder_df (input_df, ordered_df, ready_columns=False):
    if(ready_columns):
        return input_df.reindex(columns=ready_columns)
    else:    
        feature_columns = list(ordered_df.columns)
        if(feature_columns.contains("Class")):
            feature_columns.pop(feature_columns.index("Class"))
        return input_df.reindex(columns=ordered_df[feature_columns].columns)    

def test_on_file(feature_df, model_file_path):
    with open(model_file_path, 'rb') as f:
        model = pickle.load(f)
    Pred = model.predict(feature_df)
    print(Pred)
    return Pred



def Check_Corrupted_File(file_path, path_to_script_folder, error_code, line):
    if(error_code == 1):
        print(f"\n PDF Header and version are corrupted")
        if re.findall("%PDF", line):
            print(f"\n I say it is malware")
            return 1
        else:
            print(f"\n It is not a PDF aslan ya ba4a !!")
            return 0
    
    elif(error_code == 2):
        print(f"File is empty, I couldn't extract any info from inside")
        return 1
    

