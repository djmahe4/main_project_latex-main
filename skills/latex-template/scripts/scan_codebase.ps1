# scan_codebase.ps1 - v3.0 Fast Estimation Logic
# Perform multi-language comment and mermaid extraction

param(
    [string]$ProjectRoot = ".."
)

$ErrorActionPreference = "SilentlyContinue"

# Define language-specific comment patterns
$RegexPatterns = @{
    "py"  = "^(\s*#.*)|(\s*\"\"\"[\s\S]*?\"\"\")"
    "c"   = "^(\s*//.*)|(\s*/\*[\s\S]*?\*/)"
    "cpp" = "^(\s*//.*)|(\s*/\*[\s\S]*?\*/)"
    "h"   = "^(\s*//.*)|(\s*/\*[\s\S]*?\*/)"
    "ino" = "^(\s*//.*)|(\s*/\*[\s\S]*?\*/)"
    "js"  = "^(\s*//.*)|(\s*/\*[\s\S]*?\*/)"
    "md"  = "```mermaid[\s\S]*?```"
    "sh"  = "^(\s*#.*)"
}

# Directories to ignore
$IgnoreDirs = ".git", "node_modules", "vendor", ".gemini", "Preamble", "frontmatter", "chapters", "examples", "docs", "assets", "skills"

# Results collection
$ExractedData = @()

Write-Host ">>> Starting Codebase Scan in: $ProjectRoot" -ForegroundColor Cyan

# Recursively find all files
$Files = Get-ChildItem -Path $ProjectRoot -Recurse -File | Where-Object { 
    $path = $_.FullName
    $ignore = $false
    foreach ($dir in $IgnoreDirs) {
        if ($path -like "*\$dir\*") { $ignore = $true; break }
    }
    $ignore -eq $false
}

foreach ($File in $Files) {
    $Ext = $File.Extension.TrimStart(".").ToLower()
    if ($RegexPatterns.ContainsKey($Ext)) {
        $Pattern = $RegexPatterns[$Ext]
        $Content = Get-Content -Path $File.FullName -Raw
        
        # Match all occurrences
        $Matches = [regex]::Matches($Content, $Pattern, [System.Text.RegularExpressions.RegexOptions]::Multiline)
        
        foreach ($Match in $Matches) {
            $Snippet = $Match.Value.Trim()
            if ($Snippet.Length -gt 10) { # Skip trivial comments
                $ExractedData += @{
                    file      = $File.FullName.Substring($ProjectRoot.Length).TrimStart("\")
                    line      = 0 # Line counting in regex is expensive in PS; AI can estimate from context
                    language  = $Ext
                    content   = $Snippet
                    type      = if ($Snippet -like "*mermaid*") { "diagram" } else { "comment" }
                }
            }
        }
    }
}

# Output to JSON
$OutputPath = Join-Path $PSScriptRoot "../../docs/extracted_meta.json"
$ExractedData | ConvertTo-Json -Depth 5 | Out-File -FilePath $OutputPath -Encoding utf8

Write-Host ">>> Extraction Complete. Found $($ExractedData.Count) insights." -ForegroundColor Green
Write-Host ">>> Metadata saved to: docs/extracted_meta.json" -ForegroundColor Yellow
