param(
  [Parameter(Mandatory=$true)][string]$PromptFile,
  [Parameter(Mandatory=$true)][string]$OutFile,
  [switch]$First,
  [string]$SessionId = "659f8ca6-433f-4f5e-b723-c07e3b724c9f"
)

$ErrorActionPreference = "Continue"
$plugin   = "C:\Users\marko\IdeaProjects\personal_products\superfunk\plugin"
$scratch  = "C:\Users\marko\AppData\Local\Temp\claude\C--sf-bookmark-cli-trial\0edd8014-45df-432c-b235-29619e935b2e\scratchpad"
$settings = Join-Path $scratch "trial-settings.json"

Set-Location "C:\sf-bookmark-cli-trial"

if ($First) { $sessArg = @("--session-id", $SessionId) } else { $sessArg = @("--resume", $SessionId) }

$prompt = Get-Content -Raw -Path $PromptFile

$jsonl = "$env:USERPROFILE\.claude\projects\C--sf-bookmark-cli-trial\$SessionId.jsonl"
$extract = Join-Path $scratch "extract_turn.py"
$before = 0
if (Test-Path $jsonl) { $before = [int](python $extract $jsonl 0 --count) }

$sw = [System.Diagnostics.Stopwatch]::StartNew()
$prompt | & claude -p --plugin-dir $plugin --settings $settings --dangerously-skip-permissions @sessArg |
    Out-File -FilePath $OutFile -Encoding utf8
$sw.Stop()

Add-Content -Path $OutFile -Encoding utf8 -Value "`n`n===TURN_META=== exit=$LASTEXITCODE elapsed=$([int]$sw.Elapsed.TotalSeconds)s"

# claude -p prints only the FINAL assistant message. Capture every assistant
# text block from this turn so intermediate answers are not mistaken for drops.
$allFile = [System.IO.Path]::ChangeExtension($OutFile, ".all.txt")
if (Test-Path $jsonl) { python $extract $jsonl $before | Out-File -FilePath $allFile -Encoding utf8 }

Write-Output "DONE exit=$LASTEXITCODE elapsed=$([int]$sw.Elapsed.TotalSeconds)s out=$OutFile all=$allFile"
