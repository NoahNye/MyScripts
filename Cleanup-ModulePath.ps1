<#
    Author: Bryan Dady (@bcdady)
    Version: 0.1.0
    Version History: 2016-10-23
    Purpose:
        Funciton to add/merge new path into $Env:PSMODULEPATH
        Remove any/all duplicate separators (e.g. ;;)
        Sort and remove any/all duplicate entries
        Replace any/all static path entries to well known directory paths with their variable 
#>

Write-Output -InputObject 'Scanning PSModulePath'

# backup current path, just in case
$Env:PSMODULEPATH_BACKUP = $Env:PSMODULEPATH
$PSMODULEPATH     = $Env:PSMODULEPATH

if ($PSEdition -eq 'Core')
{
    # Use colon character for non-Windows / PS-Core
    $separator = ':'
}
else
{
    # Use semicolon for Windows
    $separator = ';'
}
# Remove any/all duplicate separator character
$PSMODULEPATH = ($PSMODULEPATH).Replace("$separator$separator",$separator)
# sort and remove any/all duplicate entries
$PSMODULEPATH = ($PSMODULEPATH -split $separator | Sort-Object -Unique) # -join $separator

# cleanup all but newest version subdir from modules root directories 
 $PSMODULEPATH | ForEach-Object {
    if ($PSItem -notmatch 'system32')
    {
        Get-ChildItem -Path $PSItem -Directory -Exclude .hg,.git* -ErrorAction Ignore | ForEach-Object {
            #$props = @{
                #Folder = $PSItem.Name
                #"Module folder: $($PSItem.Name)"
                $SubDirCount = (Get-ChildItem -Path $PSItem -Directory | Where-Object {$PSItem.Name -match '\d\.+'} | Measure-Object).Count
                #"$PSItem - $SubDirCount"
                Write-Verbose -Message "Retaining module $($PSItem.Name) $(Get-ChildItem -Path $PSItem -Directory | Where-Object {$PSItem.Name -match '\d\.+'} | Sort-Object -Descending -Property Name | Select-Object -first 1)" 
                if ($SubDirCount -gt 1)
                {
                    #$CleanupCount = ($SubDirCount - 1)
                    (Get-ChildItem -Path $PSItem -Directory) | Where-Object {$PSItem.Name -match '\d\.+'} | Sort-Object -Descending -Property Name | Select-Object -last ($SubDirCount - 1) | ForEach-Object { 
                            Write-Output -InputObject " # # # Removing: $($PSItem.Name) # # #" -Verbose
                            Remove-Item -Path $PSItem.FullName -Recurse -Force
                        }
                }
            #}
            #New-Object PSObject -Property $props
        }
    } #| Select-Object Folder,Count
}
