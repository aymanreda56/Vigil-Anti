### ooh there are LOT of nested features, let's put a very broad skeleton
### initial broad features are:
* md5 and sha256 which are very useless
* appeared (just a date)
* label (0 for benign, 1 for malicious, -1 for unlabeled)
* avclass (this is the classification of the antivirus)
* histogram (this is the histogram of bytes, each byte can have values from 0 to 255, so this field contains the histogram distribution of each value)
* byteentropy (the measure of entropy of each byte value, to predict the presence of obfuscation, encryption, packing, etc.)
* strings (a dictionary)
* general (a dictionary)
* header (a big dictionary)
* section (a very big dictionary)
* imports (a very big dictionary)
* exports (a list)
* datadirectories (a list)
  


### I will try to dump down all the features as dumbo bumbo
* histogram
* byteentropy
* numstrings
* avlength
* printabledist (represents the distribution of printable characters in the PE file. Printable characters are ASCII characters that have a code between 32 and 126, inclusive. They include letters, digits, punctuation, and symbols. The printables_dist field is a 16-dimensional vector that divides the range of printable characters into 16 bins and counts the frequency of each bin in the PE file. This feature can capture some information about the text content or strings embedded in the PE file, which may be useful for malware detection, it is a list of 96 elements)
* printables
* entropy
* paths
* urls
* registry
* MZ
* size
* vsize
* has_debug
* exports
* imports
* has_relocations
* has_resources
* has_signature
* has_tls
* symbols
* machine
* characteristics
* subsystem
* dll_characteristics
* major_image_version
* magic
* minor_image_version
* major_linker_version
* minor_linker_version
* major_operating_system_version
* minor_operating_system_version
* major_subsystem_version
* minor_subsystem_version
* sizeof_code
* sizeof_headers
* sizeof_heap_commit





### I am thinking of adding new features (mean byte size, number of zero bytes, number of 255 bytes, SD of bytes, sum of bytes, others) instead of the histogram

### my hypothesis is that the 0 bytes and the 255 bytes are somewhat indicative
### also the higher the total byte entropy, the more indicative that the file might be encrypted is.
### for the printabledist features, I will just leave the list as it is , it is very indicative
### I couldn't filter all the possible acceptable section names, as the cpu can just accepts a very lot of different secion names
### so I just saved the most common section names and anything else will just be flagged with "UNKNOWN"

<br>

### Same problem with DLL imports, there are numerous different DLLs
### and I cannot really filter all of them, so I will just grab the most common DLLs that are associated with most malwares
### and another feature which will be the number of imported DLLs

### I added some important features, 1) number of imported functions for each of the famous suspicious DLLs 2) total number of imported functions from all DLLs used inside the PE



### Finally, I finished the EDA

### now let's just use a RF classifier and it got 86!! while only using 700 data points :)