<h1 align="center">Vigil-Anti</h1>
<h2 align="center">Your pocket Antivirus</h2>
<p align="center">
  <img src="https://github.com/aymanreda56/Vigil-Anti/assets/58632281/79a141c7-6e1f-4cf7-838f-9793abdbdb99" alt="drawing" width="500" height="679"/>
</p>


A free open-source antivirus (antimalware to be more generic) for windows PE executables and office documents (PDF, DOCx), utilizing Machine Learning approaches as well as rule based heuristics to offer state-of-the art results and ensuring maximal security.
with a Very friendly GUI to ensure all different users have a nice experience

## Offered Features
* State-of-the art Precision and recall
* Maximal Security
* Real-time monitoring
* Scanning specific files or specific which you suspect for being a malware
* Giving a detailed report of the caught malwares and prompting the user to delete them accordingly
* Scheduling automated scans and specifying certain folders or files to keep an eye on them
* Having >99% f1 score for detecting PE and office documents malwares/viruses
* Running in the background, you don't have to keep Vigil-Anti open at all times
* Sending notifications to notify the user if Vigil-Anti caught any malware
* Friendly GUI
* Detailed and heavily maintained CLI for our fellow developers with some cool ascii art to stare into
* Ready-to-use python libraries, just import and use the functions, very easy to integrate to other projects (eg: fellow antiviruses)
* No Database used, nor requiring internet access, hence very minimal size and lightweight activity.

## Requirements
* python version > 3.7
* Windows [Vista, 7, 8, 10, 11] (required for the GUI only, CLI supports multiplatforms)

## How to Run?
### For your Granny (GUI)
* Just double click on `Vigil-Anti.bat` to setup everything and run the GUI
* To Scan a suspicious file, just click "Scan File"
  
https://github.com/aymanreda56/Vigil-Anti/assets/58632281/1117a9d8-c2bc-44e0-a873-0ea030678611

* To scan a suspicious folder, just click "Scan Folder", then wait for Vigil-Anti to finish scanning and delete the threats from the report menu

https://github.com/aymanreda56/Vigil-Anti/assets/58632281/07189bf5-eb8e-49cd-aeb2-dab3dad43fd8

* To Schedule or unschedule automated scans, just click "Configure Scans", then choose the file or folder you want to scan automatically, then specify the intended interval either every n minutes or every n days and click "Apply" !
  


https://github.com/aymanreda56/Vigil-Anti/assets/58632281/33ff03ee-4a09-4130-bfd1-d0a60324489b



### For fellow developers (CLI)
| Shorthand  | Long  | Usage  |
|---|---|---|
| path  | __  | The target path you want to scan, whether it is a file or a folder (in this case, specify -f)  |
| -h  | --help  | Display the help menu  |
| -f  | --folder-scan  | Folder scan, to recursively scan a passed folder for malwares  |
| -v  | --verbose  | Display Verbose output  |
| -q  | --quiet  | Silence all prints  |
| __  | --no-ascii-art  | Turns off the ascii art from displaying  |
| -m  | --model  | Specifies the used model, Default = RF (you don't really want to change this)  |
| -o  | --output  | Writes output to the specified file  |
| -a  | --aggressive  | Aggressive scan, Try all the models and display all outputs (Experimental, might not work properly)  |
| -sm  | --schedule-minutes  | Schedule this folder for scanning every <n> minutes, You can remove this folder from the Schedulers by entering -1  |
| -sd  | --schedule-days  | Schedule this folder for scanning every <n> days, You can remove this folder from the Schedulers by entering -1  |
| -c  | --clean-output  | Display very minimal output at the end of the output file (you might opt for this besides --output)  |
| -N  | --notify  | to enable notifications (default= False)  |

### For fellow developers (Library)
<p align="center">
  <img src="https://github.com/aymanreda56/Vigil-Anti/assets/58632281/70db44eb-10d2-4732-8d41-cb9745a77068" alt="drawing"/>
</p>


## Use case scenarios
* A company recruiter recieving hundreds of CVs, one of which can be malicious. the recruiter should set Vigil-Anti to scan all those PDFs
* My little brother likes to download pirated games which contain some crypto miners or perhaps a malicious ransomware, Vigil-Anti can help him out before it is too late!
* Some medical devices host Windows OS on them, which are very vulnerable to outsider malwares causing the OS to fail, which in some cases may be fatal, so SoC analysts might just run Vigil-Anti to monitor the sensitive software infrastructure.
* Your jumpy uncle always complains about his pc being so slow, blaming it on present malwares. You can just help him out with Vigil-Anti and save the day! your uncle will see you as a hero :)

## Technicalities
### Scanning PE executables
### Scanning PDFs

## Contributions

## Future plans (Todos)

## Donations


