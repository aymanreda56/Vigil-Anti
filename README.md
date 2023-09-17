<h1 align="center">Vigil-Anti</h1>
<h2 align="center">Your pocket Antivirus</h2>
<p align="center">
  <img src="https://github.com/aymanreda56/Vigil-Anti/blob/main/icons/gh_logo.png" alt="drawing" width="500" height="679"/>
</p>


<div align="center">

  <a href="">![GitHub commit activity (branch)](https://img.shields.io/github/commit-activity/w/aymanreda56/Vigil-Anti)</a>
  <a href="">![CII Best Practices Level](https://img.shields.io/cii/level/1?style=plastic)</a>
  <a href="">![GitHub Release Date - Published_At](https://img.shields.io/github/release-date/aymanreda56/Vigil-Anti?style=plastic)</a>
  <a href="">![GitHub language count](https://img.shields.io/github/languages/count/aymanreda56/Vigil-Anti)</a>

</div>

A free open-source antivirus (antimalware to be more generic) for windows PE executables and office documents (PDF, DOCx), utilizing Machine Learning approaches as well as rule based heuristics to offer state-of-the art results and ensuring maximal security.
with a Very friendly GUI to ensure all different users have a nice experience. Get your copy from [releases](https://github.com/aymanreda56/Vigil-Anti/releases/)!

## Offered Features :rocket:
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

## Requirements :eyes:
* python version > 3.7
* Windows [Vista, 7, 8, 10, 11] (required for the GUI only, CLI supports multiplatforms)

## How to Run?
### For your Granny (GUI) :older_woman:
* Download the binaries from the [release page](https://github.com/aymanreda56/Vigil-Anti/releases/)
* Just double click on `Vigil-Anti.bat` to setup everything and run the GUI
* To Scan a suspicious file, just click `Scan File`


https://github.com/aymanreda56/Vigil-Anti/assets/58632281/5e1972cd-07a5-4e11-b696-6993d1a867e5



* To scan a suspicious folder, just click `Scan Folder`, then wait for Vigil-Anti to finish scanning and delete the threats from the report menu


https://github.com/aymanreda56/Vigil-Anti/assets/58632281/05df4f04-33b3-4824-87c3-218b44089b5d



* To Schedule or unschedule automated scans, just click `Configure Scans`, then choose the file or folder you want to scan automatically, then specify the intended interval either every n minutes or every n days and click `Apply` !
  

https://github.com/aymanreda56/Vigil-Anti/assets/58632281/e615628b-5bc3-4fa5-9736-04a68de9990c




### For fellow developers (CLI) :computer:
You run the CLI like this:
```
python Vigil_Anti.py <filepath> <options>
```
#### Available options

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

Also you can watch this short demo on the cool CLI from [here](https://youtu.be/TOcYXyd2R94?si=Uhsy7Ab0vqh1Tzzl)

### For fellow developers (Library) 👨🏻‍🎓
<p align="center">
  <img src="https://github.com/aymanreda56/Vigil-Anti/blob/main/icons/library.png" alt="drawing"/>
</p>


## Use case scenarios :clapper:
* A company recruiter recieving hundreds of CVs, one of which can be malicious. the recruiter should set Vigil-Anti to scan all those PDFs
* My little brother likes to download pirated games which contain some crypto miners or perhaps a malicious ransomware, Vigil-Anti can help him out before it is too late!
* Some medical devices host Windows OS on them, which are very vulnerable to outsider malwares causing the OS to fail, which in some cases may be fatal, so SoC analysts might just run Vigil-Anti to monitor the sensitive software infrastructure.
* Your jumpy uncle always complains about his pc being so slow, blaming it on present malwares. You can just help him out with Vigil-Anti and save the day! your uncle will see you as a hero :)

## Technicalities :wrench:
### Scanning PE executables
Vigil-Anti used LIEF python package to parse executables and gain metadata.
from those metadata we extract some useful features totalling 310 features!!
some of the features are Byte entropy, Byte histogram, number of printable static strings, usage of packers, indications of encryption and/or obfuscation, imported modules and DLL names, all the IO operations and windows API function calls and a lot more!

those features are used to train a Random Forest classifier with 100 Decision tree estimators, no limit for the levels of each tree.

finally achieving a test score of 96% on [VirusShare](https://virusshare.com/torrents) Datasets which is considered highly competitive to the other state-of-the-art tools
### Scanning PDFs
There were a lot of papers claiming that it is very enough to decide whether a PDF is malicious or not by only analyzing its metadata.
So I grabbed a bunch of useful features, most of which are numerical features extracted after parsing the PDF referring to the [PDF structure](https://en.wikipedia.org/wiki/PDF)
A dataset is then used to train a Random Forest with 300 estimators and achieved 99.7% f1 score which is clearly impressive!!

## Contributions 🤝🏼
1. One should issue an issue first, describing the problem he solves, or the new module you are adding
2. Then just PR
3. I will review it and try to integrate your module
4. If you are implementing a completely new module, you don't have to integrate it, just PR and I will work it out in the integrated code

## Future plans (Todos) :pray:
* Support Web formats (HTML, css)
* Support source code malwares (not binaries)
* Support interpretted language malwares, specifically JS ones that gets loaded at client-side
* Photo scanner
* More real-time UX: scan any file just after the user clicks on the file, but hold the file from executing until the scan is finished

## Donations :money_with_wings:
Welp this is a Free Open-Source Software, I don't get paid for this 🤷🏻‍♂️; this project is 100% out of sheer motivation and having fun.
if you want to help, just leave a kind review or hope that I don't get drafted for military services 🥺.

