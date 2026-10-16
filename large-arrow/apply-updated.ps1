[CmdletBinding()]
param([ValidateSet('all','astra','sol')][string]$Character='astra',[ValidateSet(32,48,64,72,96,128,256)][int]$Size=72)
$ErrorActionPreference='Stop'
& (Join-Path $PSScriptRoot 'install.ps1') -Character $Character -Size $Size -Apply
& (Join-Path $PSScriptRoot 'keeper.ps1') -Action Install
