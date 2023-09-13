$FolderPath = $args[0]

$Retdec_Path = $args[1]

$Output_Path = $args[2]



$Orig_Path = Get-Location



if( $false -eq (Test-Path -Path $Output_Path))
{
    New-Item -Path $Output_Path -ItemType Directory
}


Set-Location $FolderPath

$AllFiles = Get-ChildItem $FolderPath

foreach( $file in $AllFiles)
{
    python "$Retdec_Path/retdec-decompiler.py" $file -k --backend-keep-library-funcs --backend-no-compound-operators --backend-no-opts --backend-strict-fpu-semantics --stop-after bin2llvmir -o "$FolderPath/$file"
}

$AllFiles = Get-ChildItem $FolderPath
foreach ($file in $AllFiles)
{
    $ext = $file.Extension
    if($ext -eq ".bc" -or $ext -eq ".json" -or $ext -eq ".conf.json" -or $ext -eq ".dsm")
    {
        Remove-Item $file
    }

    if($ext -eq ".ll")
    {
        Move-Item -Path $file -Destination "$Output_Path/$file"
    }
}


Set-Location $Orig_Path
