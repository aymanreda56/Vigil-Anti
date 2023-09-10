import lief
import os
import re
from pprint import pprint
import statistics
from tqdm import tqdm
import pandas as pd
import numpy as np
import pickle

DOS_Header_Fields = [
'Magic',
'Used Bytes In The LastPage',
'File Size In Pages',
'Number Of Relocation',
'Header Size In Paragraphs',
'Minimum Extra Paragraphs',
'Maximum Extra Paragraphs',
'Initial Relative SS',
'Initial SP',
'Checksum',
'Initial IP',
'Initial Relative CS',
'Address Of Relocation Table',
'Overlay Number',
'OEM id',
'OEM info',
'Address Of New Exe Header']


Header_Fields = [
'Signature',
'Machine',
'Number Of Sections',
'Pointer To Symbol Table',
'Number Of Symbols',
'Size Of Optional Header',
'Characteristics',
'Time Date Stamp'
]


def RemoveBlankLines_From_dictionary(input_dict:dict):
    for k,v in input_dict.items():
        newValue = []
        for line in v:
            if line != '':
                newValue.append(line)
        input_dict[k] = newValue
    return input_dict





def Parse_Lief_Binary_to_Dict (binary_file, Verbose_Output=False):

    AllHeaders=[]

    Dictionaries_Of_All_Fields = {}

    splitted_binary_file = re.split("\n", str(binary_file))
    #print(splitted_binary_file)
    for i, line in enumerate(splitted_binary_file):
        if(i < len(splitted_binary_file)-1):
            if re.findall("=+", splitted_binary_file[i+1]):
                AllHeaders.append(line)
                continue
        
        if(re.findall("=+", line)):
            continue
        currentHeader = AllHeaders[-1]
        if (currentHeader in Dictionaries_Of_All_Fields.keys()):
            Dictionaries_Of_All_Fields[currentHeader].append(line)
        else:
            Dictionaries_Of_All_Fields[currentHeader] = []
            Dictionaries_Of_All_Fields[currentHeader].append(line)

    Dictionaries_Of_All_Fields = RemoveBlankLines_From_dictionary(Dictionaries_Of_All_Fields)
    if(Verbose_Output): pprint(Dictionaries_Of_All_Fields)

    for header, arrayOfLines in Dictionaries_Of_All_Fields.items():
        smallDict = {}
        for line in arrayOfLines:
            
            arrOfValues = re.split(":", line)
            try:
                if(len(arrOfValues) > 2):
                    if(Verbose_Output): print(f"THERE IS AN ERROR:      {arrOfValues} IN:     {header}")
                else:
                    smallDict[arrOfValues[0]] = arrOfValues[1]
            except:
                if(Verbose_Output): print(f"ERRRORRRR:     {line} IN:        {header}")
        
        Dictionaries_Of_All_Fields[header] = smallDict
        if(Verbose_Output): pprint(Dictionaries_Of_All_Fields)
    #print(AllHeaders)


    if(Verbose_Output): pprint(Dictionaries_Of_All_Fields)


    return Dictionaries_Of_All_Fields






def Interpret_Histogram(list_of_bytes:list, additional_name):
    try:
        zero_bytes = list_of_bytes[0]
        full_bytes = list_of_bytes[-1]
        mean_of_bytes = sum(list_of_bytes) / len(list_of_bytes)
        standard_dev = statistics.pstdev(list_of_bytes)
        total_bytes = sum(list_of_bytes)
        mean_of_first_tertile = statistics.mean(list_of_bytes[0:85])
        mean_of_second_tertile = statistics.mean(list_of_bytes[85:170])
        mean_of_third_tertile = statistics.mean(list_of_bytes[170:])

        return_dict = {f'zero_bytes_{additional_name}': zero_bytes, f'full_bytes_{additional_name}': full_bytes, f'mean_of_bytes_{additional_name}': mean_of_bytes, f'standard_dev_{additional_name}': standard_dev, f'total_bytes_{additional_name}': total_bytes, f'mean_of_first_tertile_{additional_name}': mean_of_first_tertile, f'mean_of_second_tertile_{additional_name}': mean_of_second_tertile, f'mean_of_third_tertile_{additional_name}': mean_of_third_tertile}
    except:
        print(f"Error inside Interpret_Histogram()")
    return return_dict

def extract_subfields_from_fields(dic, name_of_field, normalize_names=False,delete_field= False):
    try:
        if(type(dic[name_of_field]) != dict):
            print(f"the value of the input field in the passed dictionary, is not a dictionary")
        for k,v in dic[name_of_field].items():
            if(normalize_names):
                new_field_name = f"{name_of_field}_{k}"
                dic[new_field_name] = v
            else:
                dic[k] = v
        if(delete_field):
            del dic[name_of_field]
    except:
        print(f"Error inside extract_subfields_from_fields()")

    return dic



def handle_data_directories_field(dic:dict):
    try:
        list_of_dicts = dic["datadirectories"]
        for d in list_of_dicts:
            new_small_dict = {}
            name_of_new_field = d['name']
            new_small_dict[f"{name_of_new_field}_size"] = d['size']
            new_small_dict[f"{name_of_new_field}_virtual_address"] = d['virtual_address']
            dic.update(new_small_dict)
        
        del dic['datadirectories']
    except:
        print(f"Error inside handle_data_directories_field()")
    return dic


def handle_section_names (ds_obj: dict, Common_section_names, delete_field = False):
    try:
        new_small_dic = {}
        for dic_elm in ds_obj['section']['sections']:
            name_of_section = dic_elm['name']
            if(not(name_of_section in Common_section_names)):
                name_of_section = "UNKNOWN_SECTION"
            
            new_small_dic[f"{name_of_section}_size"] = dic_elm['size']
            new_small_dic[f"{name_of_section}_entropy"] = dic_elm['entropy']
            new_small_dic[f"{name_of_section}_vsize"] = dic_elm['vsize']
            new_small_dic[f"{name_of_section}_props_len"] = len(dic_elm['props'])
        
        ds_obj.update(new_small_dic)
        if(delete_field):
            del ds_obj['section']
    except:
        print(f"Error inside handle_section_names()")
    return ds_obj


def handle_DLL_imports (dic:dict, delete_field=False):
    try:
        with open(os.path.join(os.getcwd(), 'assets', 'suspicious_imports.txt'), 'r') as f:
            suspicious_DLL_list = f.readlines()
        
        suspicious_DLL_list = [re.sub(r'\n', '', i) for i in suspicious_DLL_list]

        import_DLL_dict = dic['imports']
        DLL_list = list(import_DLL_dict.keys())
        num_of_DLLs = len(DLL_list)
        number_of_imported_funcs = 0
        for elm in DLL_list:
            re.sub('\.dll', '', elm)
            number_of_imported_funcs += len(import_DLL_dict[elm])
            for dll in suspicious_DLL_list:
                matches = re.findall(elm, ''.join(dll), re.IGNORECASE)
                if(matches):
                    dic[f'{dll}'] = True

                    number_of_funcs_in_DLL=len(import_DLL_dict[elm])
                    dic[f"{dll}_num_funcs"] = number_of_funcs_in_DLL
        
        dic['number_of_DLLs'] = num_of_DLLs
        dic["total_num_of_imported_funcs"] = number_of_imported_funcs
        if(delete_field):
            del dic['imports']
    except:
        print(f"Error inside handle_DLL_imports()")
    return dic


def flatten_strings_printable_distribution(dic:dict, delete_field=False):
    try:
        distribution = dic['strings_printabledist']
        for i, val in enumerate(distribution):
            dic[f'strings_printabledist_{i}'] = val
        
        if(delete_field):
            del dic['strings_printabledist']
    except:
        print(f"Error inside flatten_strings_printable_distribution()")
    return dic


def reorder_df (input_df, ordered_df, ready_columns=False, fill_value=np.nan):
    if(ready_columns):
        return input_df.reindex(columns=ready_columns, fill_value=fill_value)
    else:    
        feature_columns = list(ordered_df.columns)
        if(feature_columns.contains("label")):
            feature_columns.pop(feature_columns.index("label"))
        return input_df.reindex(columns=ordered_df[feature_columns].columns, fill_value=fill_value)


def Preprocess_Features_into_dataframe(Feature_Dict):
    try:

        # Read the most common section names
        with open(os.path.join(os.getcwd(), 'assets', 'common_section_names.txt'), 'r') as f:
            Common_section_names = f.readlines()
        Common_section_names = [re.sub(r'\n', '', i) for i in Common_section_names]


        # add reduced features of byteentropy distribution
        Feature_Dict.update(Interpret_Histogram(Feature_Dict['byteentropy'], 'byteentropy'))

        # add reduced features of byte histogram distribution
        Feature_Dict.update(Interpret_Histogram(Feature_Dict['histogram'], 'bytehistogram'))

        # reduce strings field
        Feature_Dict = extract_subfields_from_fields(Feature_Dict, 'strings', normalize_names=True, delete_field=True)

        # flatten the strings printables distribution field
        Feature_Dict = flatten_strings_printable_distribution(Feature_Dict, delete_field=True)

        # reduce general field
        Feature_Dict = extract_subfields_from_fields(Feature_Dict, 'general', normalize_names=True, delete_field=True)

        # reduce header field
        Feature_Dict = extract_subfields_from_fields(Feature_Dict, 'header', normalize_names=True, delete_field=True)
        Feature_Dict = extract_subfields_from_fields(Feature_Dict, 'header_optional', normalize_names=False, delete_field=True)
        Feature_Dict = extract_subfields_from_fields(Feature_Dict, 'header_coff', normalize_names=False, delete_field=True)


        # handle data directories field
        Feature_Dict = handle_data_directories_field(Feature_Dict)


        # handle sections fields
        Feature_Dict = handle_section_names(Feature_Dict, Common_section_names, delete_field=True)

        # handle imports fields
        Feature_Dict = handle_DLL_imports(Feature_Dict, delete_field=False)

        # Remove the useless columns for now (they are not entirely useless but they will make the training process very complex for me :(( )
        useless_columns = ['sha256'
            ,'md5'
            ,'appeared'
            ,'avclass'
            ,'histogram'
            ,'byteentropy'
            ,'imports'
            ,'exports'
            ,'dll_characteristics'
            ,'characteristics']

        for useless_col in useless_columns:
            del Feature_Dict[useless_col]
        
    except:
        print(f"bruh")



    for k, v in Feature_Dict.items():
        if(type(v) != list):
            Feature_Dict[k] = [v]

    
    df = pd.DataFrame().from_dict(Feature_Dict, orient='index').transpose()

    # load our feature list in their correct order
    with open(os.path.join(os.getcwd(), 'assets', 'features.pkl'), 'rb') as f:
        feature_columns = pickle.load(f)
    
    df = reorder_df (df, pd.DataFrame(), feature_columns)
    
    df.fillna(0, inplace=True)
    
    with open(os.path.join(os.getcwd(), 'assets', 'suspicious_imports.txt'), 'r') as f:
        sus_imports = f.readlines()
    sus_imports = [re.sub(r'\n', '', i) for i in sus_imports]

    boolean_columns = sus_imports + []
    categorical_columns = ["subsystem", "magic", "machine"]

    for col in df.columns:
        if col in boolean_columns:
            df[col] = df[col].astype(bool)
            df[col].fillna(False)
            continue

        if col in categorical_columns:
            df[col].replace(0, 'UNKNOWN', inplace=True)
            continue
        df[col].fillna(0)
        df[col] = df[col].astype(np.int64)
        df[col].fillna(0)

    df = df.iloc[0:1, ]

    with open(os.path.join(os.getcwd(),'models','enc.pkl'), 'rb') as f:
        array_of_Label_Encoders = pickle.load(f)
    
    
    df_train_1 = df.copy()

    for i, col in enumerate(categorical_columns):
        try:
            df_train_1[col] = array_of_Label_Encoders[i].transform(df_train_1[col])
        except:
            print(f"ERROR during Label encoder, column {col} with value {df_train_1[col]}")
    

    df_train_1 = reorder_df (df_train_1, pd.DataFrame(), feature_columns)


    for col in feature_columns:
        if(col not in df.columns):
            df.drop(col, axis=1, inplace=True)

    return df_train_1





def Inference(df_train, model_path):

    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    pred = model.predict(df_train)
    return pred

