# isolate_build.ps1 - v1.0 Surgical Build Engine
param(
    [Parameter(Mandatory=$true)]
    [string]$TargetFile
)

$ErrorActionPreference = "Stop"

# Ensure docs/preview exists
if (-not (Test-Path "../../docs/preview")) {
    New-Item -ItemType Directory -Path "../../docs/preview" -Force
}

$BaseName = [System.IO.Path]::GetFileNameWithoutExtension($TargetFile)
$TempMain = "../../main_isolate.tex"

Write-Host ">>> Isolating target: $TargetFile" -ForegroundColor Cyan

# Construct the standalone wrapper
$Wrapper = @"
\documentclass[11pt,a4paper]{report}

% Load Preamble
\input{Preamble/packages.tex}
\input{Preamble/config.tex}
\input{Preamble/fonts.tex}
\input{Preamble/pagestyle.tex}
\input{Preamble/sectionoptions.tex}
\input{Preamble/macro.tex}

\begin{document}
\input{$TargetFile}
\end{document}
"@

$Wrapper | Out-File -FilePath $TempMain -Encoding utf8

# Compile
Write-Host ">>> Compiling Isolated Artifact..." -ForegroundColor Yellow
$xelatexCmd = "xelatex -interaction=nonstopmode -halt-on-error main_isolate.tex"
Invoke-Expression $xelatexCmd
Invoke-Expression $xelatexCmd # Twice for references if any

# Clean up and move
Copy-Item "main_isolate.pdf" "../../docs/preview/$($BaseName)_preview.pdf" -Force
Remove-Item "main_isolate.*" -ErrorAction SilentlyContinue

Write-Host ">>> Isolation Complete! Preview saved to docs/preview/$($BaseName)_preview.pdf" -ForegroundColor Green
