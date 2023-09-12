$rootPath= $args[0]
$targtPath = $args[1]




<#
Hello, this script is just a filtering script that filters files in a given directory by their true type
it basically runs exiftool on every file and copies the intended files in the destination path

REQUIREMENTS:
you should have exiftool installed on your system or this script will just scream in pain

Arguments:
1) rootPath: is the path of the folder containing the malware files
2) targetPath: is the path of the destination folder in which you wish to put the filtered files

how to run?

.\filter.ps1 "D:\hackSF\V_Dataset" "D:\hackSF\filtered_dataset"
    ^script^    ^^^rootPath^^^^       ^^^^DestinationPath^^^^
#>




if($false -eq (Test-Path -Path $targtPath))
{   
    New-Item -Path $targtPath -ItemType Directory
}
else {
    Remove-Item -Recurse $targtPath
    New-Item -Path $targtPath -ItemType Directory
}




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

    try{
                $m = $A -match "File Type (?!Extension).*: (\w+)"
                if($A -match "error")
                {
                    $n = $A -match "error"
                    $FileType = $n[0].split(":")
                }
                else {
                    $FileType = $m[0].split(":")
                }
                $FileType = $FileType[-1]
                $FileType = $FileType.replace(" ", "_")
                $FileType = $FileType.substring(1, $FileType.Length-1)
                
                if($FileType)
                {
                    $FileTypePath = Join-Path -Path $targtPath -ChildPath $FileType
                    if ($false -eq (Test-Path -Path $FileTypePath))
                    {
                        New-Item -Path $FileTypePath -ItemType Directory -ErrorAction SilentlyContinue > $null
                    }
                    Copy-Item -Path "$rootPath/$file" -Destination "$FileTypePath/$count"
                }
                $count += 1
                #Write-Host "$count / $count_of_all_files            -------->          $FileType"
                $percentage=($count/$count_of_all_files)*100
                Write-Progress -Activity "Splitting Files into Beautiful Folders" -Status "$percentage %" -PercentComplete $percentage
    }
    
    catch {
        $FileTypePath = Join-Path -Path $targtPath -ChildPath "I_Give_Up_I_Cannot_Understand_This_File_WAAAA2"
        if ($false -eq (Test-Path -Path $FileTypePath))
        {
            New-Item -Path $FileTypePath -ItemType Directory > $null
        }
            Copy-Item -Path "$rootPath/$file" -Destination "$FileTypePath/$count"
    }
}
Set-Location $origLoc
