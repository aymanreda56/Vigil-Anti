import lief
import os
import re
from pprint import pprint

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