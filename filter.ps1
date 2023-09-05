$rootPath= $args[0]
$targtPath = $args[1]
$filterExt = $args[2]



<#
Hello, this script is just a filtering script that filters files in a given directory by their true type
it basically runs exiftool on every file and copies the intended files in the destination path

REQUIREMENTS:
you should have exiftool installed on your system or this script will just scream in pain

Arguments:
1) rootPath: is the path of the folder containing the malware files
2) targetPath: is the path of the destination folder in which you wish to put the filtered files
3) filterExt: is the type of files you are searching for

how to run?

.\filter.ps1 "D:\hackSF\V_Dataset" "D:\hackSF\filtered_dataset" "jpg"
    ^script^    ^^^rootPath^^^^       ^^^^DestinationPath^^^^  ^Filter^
#>

$filterExt_lower = $filterExt.ToLower()
$filterExt_upper = $filterExt.ToUpper()
Write-Host $filterExt_lower
Write-Host $filterExt_upper

$count_of_all_files = Get-ChildItem $rootPath | Measure-Object
$count_of_all_files = $count_of_all_files.Count


$allFiles = Get-ChildItem $rootPath

$origLoc = Get-Location
Set-Location $rootPath
$count = 0
foreach ($file in $allFiles)
{
    $A = exiftool ".\$file"
    #Write-Host $A

    $m = $A -match "File Type.*$filterExt"
    #Write-Host $m
    if($m)
    {
        #Write-Host $Matches
        Copy-Item -Path "$rootPath/$file" -Destination "$targtPath/$count"
    }
    $count += 1
    Write-Host "$count / $count_of_all_files"
}
Set-Location $origLoc
