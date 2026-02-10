# OneDrive Document Scanner — Copy to Reference Folder
#
# Scans two OneDrive directories for engineering-relevant documents
# and copies them to stru-engineer/reference/ with folder structure preserved.
#
# Usage: Right-click this file → "Run with PowerShell"
#    Or: Open PowerShell, navigate to script location, run: .\scan-onedrive.ps1
#
# To do a dry run first (see what would be copied without copying):
#    .\scan-onedrive.ps1 -DryRun

param(
    [switch]$DryRun
)

# ──────────────────────────────────────────────────────────────
# CONFIGURATION — Edit these paths if needed
# ──────────────────────────────────────────────────────────────

$OneDrivePaths = @(
    "C:\Users\Ray\OneDrive - rl.tennal",
    "C:\Users\Ray\OneDrive - rl.tennal (1)"
)

# Destination: reference folder inside the stru-engineer repo
# Adjust this path to match where your local clone lives
$RepoRoot = Split-Path -Parent $PSScriptRoot
# If the script is in the repo root, use $PSScriptRoot instead:
# $RepoRoot = $PSScriptRoot

$DestinationRoot = Join-Path $RepoRoot "reference"

# File extensions to copy (case-insensitive)
$Extensions = @(
    # Documents
    "*.doc", "*.docx", "*.odt",
    # Spreadsheets
    "*.xls", "*.xlsx", "*.xlsm", "*.csv", "*.ods",
    # CAD files
    "*.dwg", "*.dxf",
    # PDF
    "*.pdf",
    # Text / Markup
    "*.txt", "*.md", "*.rtf",
    # Engineering / Math
    "*.mcdx", "*.xmcd",        # MathCAD
    "*.rvt", "*.rfa",           # Revit
    "*.r3d", "*.rfl",           # RISA
    "*.e2k", "*.s2k", "*.sdb", # ETABS / SAP2000
    # Images (structural photos, sketches)
    "*.jpg", "*.jpeg", "*.png", "*.tif", "*.tiff", "*.bmp",
    # Email archives
    "*.msg", "*.eml"
)

# Skip these folder names (case-insensitive)
$ExcludeFolders = @(
    ".git",
    "node_modules",
    "__pycache__",
    ".Trash*",
    "Recycle*"
)

# Maximum file size to copy (500 MB — skip huge files)
$MaxFileSizeMB = 500

# ──────────────────────────────────────────────────────────────
# SCRIPT LOGIC
# ──────────────────────────────────────────────────────────────

$ErrorActionPreference = "Continue"
$startTime = Get-Date

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  RaBuilt OneDrive Document Scanner" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($DryRun) {
    Write-Host "  *** DRY RUN MODE — No files will be copied ***" -ForegroundColor Yellow
    Write-Host ""
}

# Validate source paths
foreach ($src in $OneDrivePaths) {
    if (-not (Test-Path $src)) {
        Write-Host "WARNING: Source path not found: $src" -ForegroundColor Red
        Write-Host "  Skipping this OneDrive location." -ForegroundColor Red
        Write-Host ""
    }
}

# Create destination root
if (-not $DryRun) {
    if (-not (Test-Path $DestinationRoot)) {
        New-Item -ItemType Directory -Path $DestinationRoot -Force | Out-Null
        Write-Host "Created destination: $DestinationRoot" -ForegroundColor Green
    }
}

# Counters
$totalFiles = 0
$totalCopied = 0
$totalSkipped = 0
$totalErrors = 0
$totalSizeBytes = 0
$skippedLargeFiles = @()
$errorFiles = @()

# Build exclude pattern for Where-Object
function Test-ExcludedPath {
    param([string]$Path)
    foreach ($exclude in $ExcludeFolders) {
        if ($Path -match [regex]::Escape($exclude)) {
            return $true
        }
    }
    return $false
}

# Process each OneDrive
foreach ($srcRoot in $OneDrivePaths) {
    if (-not (Test-Path $srcRoot)) { continue }

    # Determine label for destination subfolder
    $folderName = Split-Path $srcRoot -Leaf
    # Clean up the folder name for the destination
    $destLabel = $folderName -replace '[^\w\s\-\.]', '' -replace '\s+', '_'

    Write-Host "Scanning: $srcRoot" -ForegroundColor Cyan
    Write-Host "  → Destination subfolder: $destLabel" -ForegroundColor Gray
    Write-Host ""

    $destBase = Join-Path $DestinationRoot $destLabel

    # Find all matching files
    $files = @()
    foreach ($ext in $Extensions) {
        $found = Get-ChildItem -Path $srcRoot -Filter $ext -Recurse -File -ErrorAction SilentlyContinue |
            Where-Object { -not (Test-ExcludedPath $_.FullName) }
        $files += $found
    }

    # Remove duplicates (a file might match multiple patterns)
    $files = $files | Sort-Object FullName -Unique

    $sourceFileCount = $files.Count
    Write-Host "  Found $sourceFileCount matching files" -ForegroundColor White

    foreach ($file in $files) {
        $totalFiles++

        # Check file size
        $fileSizeMB = $file.Length / 1MB
        if ($fileSizeMB -gt $MaxFileSizeMB) {
            $skippedLargeFiles += [PSCustomObject]@{
                Path = $file.FullName
                SizeMB = [math]::Round($fileSizeMB, 1)
            }
            $totalSkipped++
            continue
        }

        # Calculate relative path from source root
        $relativePath = $file.FullName.Substring($srcRoot.Length).TrimStart('\', '/')
        $destPath = Join-Path $destBase $relativePath
        $destDir = Split-Path $destPath -Parent

        # Check if destination file exists and is same size + date (skip if identical)
        if (Test-Path $destPath) {
            $existingFile = Get-Item $destPath
            if ($existingFile.Length -eq $file.Length -and $existingFile.LastWriteTime -eq $file.LastWriteTime) {
                $totalSkipped++
                continue
            }
        }

        if ($DryRun) {
            Write-Host "  WOULD COPY: $relativePath ($([math]::Round($fileSizeMB, 1)) MB)" -ForegroundColor Gray
            $totalCopied++
            $totalSizeBytes += $file.Length
        }
        else {
            try {
                # Create directory structure
                if (-not (Test-Path $destDir)) {
                    New-Item -ItemType Directory -Path $destDir -Force | Out-Null
                }

                # Copy file preserving metadata
                Copy-Item -Path $file.FullName -Destination $destPath -Force
                $totalCopied++
                $totalSizeBytes += $file.Length

                # Progress indicator every 50 files
                if ($totalCopied % 50 -eq 0) {
                    Write-Host "  Copied $totalCopied files..." -ForegroundColor Gray
                }
            }
            catch {
                $totalErrors++
                $errorFiles += [PSCustomObject]@{
                    Path  = $file.FullName
                    Error = $_.Exception.Message
                }
                Write-Host "  ERROR: $($file.FullName) — $($_.Exception.Message)" -ForegroundColor Red
            }
        }
    }

    Write-Host ""
}

# ──────────────────────────────────────────────────────────────
# SUMMARY
# ──────────────────────────────────────────────────────────────

$elapsed = (Get-Date) - $startTime
$totalSizeMB = [math]::Round($totalSizeBytes / 1MB, 1)
$totalSizeGB = [math]::Round($totalSizeBytes / 1GB, 2)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  SCAN COMPLETE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Files found:      $totalFiles"
if ($DryRun) {
    Write-Host "  Would copy:       $totalCopied" -ForegroundColor Yellow
} else {
    Write-Host "  Files copied:     $totalCopied" -ForegroundColor Green
}
Write-Host "  Files skipped:    $totalSkipped (identical or too large)"
Write-Host "  Errors:           $totalErrors" -ForegroundColor $(if ($totalErrors -gt 0) { "Red" } else { "Gray" })
Write-Host ""
if ($totalSizeGB -ge 1) {
    Write-Host "  Total size:       $totalSizeGB GB"
} else {
    Write-Host "  Total size:       $totalSizeMB MB"
}
Write-Host "  Elapsed time:     $([math]::Round($elapsed.TotalSeconds, 1)) seconds"
Write-Host "  Destination:      $DestinationRoot"
Write-Host ""

# Report large files that were skipped
if ($skippedLargeFiles.Count -gt 0) {
    Write-Host "  Large files skipped (> $MaxFileSizeMB MB):" -ForegroundColor Yellow
    foreach ($lf in $skippedLargeFiles) {
        Write-Host "    $($lf.SizeMB) MB — $($lf.Path)" -ForegroundColor Yellow
    }
    Write-Host ""
}

# Report errors
if ($errorFiles.Count -gt 0) {
    Write-Host "  Files with errors:" -ForegroundColor Red
    foreach ($ef in $errorFiles) {
        Write-Host "    $($ef.Path)" -ForegroundColor Red
        Write-Host "      $($ef.Error)" -ForegroundColor DarkRed
    }
    Write-Host ""
}

# Generate file type summary
Write-Host "  File type breakdown:" -ForegroundColor Cyan
$typeBreakdown = @{}
foreach ($srcRoot in $OneDrivePaths) {
    if (-not (Test-Path $srcRoot)) { continue }
    foreach ($ext in $Extensions) {
        $found = Get-ChildItem -Path $srcRoot -Filter $ext -Recurse -File -ErrorAction SilentlyContinue
        foreach ($f in $found) {
            $fileExt = $f.Extension.ToLower()
            if (-not $typeBreakdown.ContainsKey($fileExt)) {
                $typeBreakdown[$fileExt] = @{ Count = 0; SizeBytes = 0 }
            }
            $typeBreakdown[$fileExt].Count++
            $typeBreakdown[$fileExt].SizeBytes += $f.Length
        }
    }
}

$typeBreakdown.GetEnumerator() | Sort-Object { $_.Value.Count } -Descending | ForEach-Object {
    $ext = $_.Key
    $count = $_.Value.Count
    $sizeMB = [math]::Round($_.Value.SizeBytes / 1MB, 1)
    Write-Host ("    {0,-10} {1,6} files  ({2,8} MB)" -f $ext, $count, $sizeMB) -ForegroundColor Gray
}

Write-Host ""
Write-Host "Done." -ForegroundColor Green

# Add reference/ to .gitignore if not already there
$gitignorePath = Join-Path $RepoRoot ".gitignore"
$gitignoreEntry = "reference/"
if (Test-Path $gitignorePath) {
    $content = Get-Content $gitignorePath -Raw
    if ($content -notmatch [regex]::Escape($gitignoreEntry)) {
        Add-Content -Path $gitignorePath -Value "`n$gitignoreEntry"
        Write-Host "Added 'reference/' to .gitignore" -ForegroundColor Green
    }
} else {
    Set-Content -Path $gitignorePath -Value "$gitignoreEntry`n"
    Write-Host "Created .gitignore with 'reference/' entry" -ForegroundColor Green
}
