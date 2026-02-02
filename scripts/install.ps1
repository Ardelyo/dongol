# DONGOL Universal Installation Script for Windows
# Made in Indonesia 🇮🇩
# Supports: Windows 10/11 with PowerShell 5.1+

$ErrorActionPreference = "Stop"

$DongolAscii = @"
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   ██████   ██████  ███    ██  ██████   ██████               ║
║   ██   ██ ██    ██ ████   ██ ██       ██    ██              ║
║   ██   ██ ██    ██ ██ ██  ██ ██   ███ ██    ██              ║
║   ██   ██ ██    ██ ██  ██ ██ ██    ██ ██    ██              ║
║   ██████   ██████  ██   ████  ██████   ██████               ║
║                                                               ║
║              Made in Indonesia                               ║
║       Created by Ardellio Satria Anindito                    ║
║       SMA Kartika XIX-1 Bandung                              ║
╚═══════════════════════════════════════════════════════════════╝
"@

function Write-ColorOutput {
    param([string]$Message, [string]$Color = "White")
    Write-Host $Message -ForegroundColor $Color
}

function Test-CommandExists {
    param([string]$Command)
    $null = Get-Command $Command -ErrorAction SilentlyContinue
    return $?
}

function Get-PythonVersion {
    try {
        $version = python --version 2>&1
        if ($version -match "Python (\d+)\.(\d+)") {
            return [int]$matches[1], [int]$matches[2]
        }
    } catch {
        return 0, 0
    }
    return 0, 0
}

function Install-Dongol {
    Write-ColorOutput $DongolAscii "Cyan"
    
    Write-ColorOutput "`nInstalling DONGOL..." "Green"
    Write-ColorOutput "Made in Indonesia by Ardellio Satria Anindito (SMA Kartika XIX-1 Bandung)`n" "Yellow"
    
    # Check Python
    Write-ColorOutput "Checking Python installation..." "Yellow"
    $major, $minor = Get-PythonVersion
    
    if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 9)) {
        Write-ColorOutput "Python 3.9+ is required. Found: $major.$minor" "Red"
        Write-ColorOutput "Download from: https://python.org/downloads" "Yellow"
        exit 1
    }
    Write-ColorOutput "Python $major.$minor detected" "Green"
    
    # Check pip
    if (-not (Test-CommandExists "pip")) {
        Write-ColorOutput "pip not found. Installing..." "Yellow"
        python -m ensurepip --upgrade
    }
    Write-ColorOutput "pip detected" "Green"
    
    # Installation directory
    $InstallDir = "$env:LOCALAPPDATA\dongol"
    $ConfigDir = "$env:USERPROFILE\.dongol"
    
    # Create directories
    New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
    New-Item -ItemType Directory -Force -Path "$ConfigDir\data" | Out-Null
    
    # Install DONGOL
    Write-ColorOutput "`nInstalling DONGOL from PyPI..." "Yellow"
    
    try {
        pip install dongol[all] --quiet
        Write-ColorOutput "DONGOL installed successfully" "Green"
    } catch {
        Write-ColorOutput "PyPI install failed. Installing from source..." "Yellow"
        
        $TempDir = [System.IO.Path]::GetTempPath() + [System.Guid]::NewGuid().ToString()
        New-Item -ItemType Directory -Force -Path $TempDir | Out-Null
        
        git clone --depth 1 https://github.com/dongol-org/dongol.git $TempDir 2>$null
        
        if ($?) {
            Set-Location $TempDir
            pip install -e ".[all]" --quiet
        } else {
            Write-ColorOutput "Installation failed. Please check your internet connection." "Red"
            exit 1
        }
        
        # Cleanup
        Set-Location $env:USERPROFILE
        Remove-Item -Recurse -Force $TempDir -ErrorAction SilentlyContinue
    }
    
    # Create config
    Write-ColorOutput "`nCreating configuration..." "Yellow"
    
    $ConfigContent = @"
# DONGOL Configuration
# Made in Indonesia
# Created by Ardellio Satria Anindito

engine:
  max_workers: 4
  use_processes: false

chunking:
  max_chunk_size: 1000
  overlap_ratio: 0.1

storage:
  backend: sqlite
  path: $env:USERPROFILE\.dongol\data

logging:
  level: info

i18n:
  default_language: id
"@
    
    $configPath = "$ConfigDir\config.yaml"
    $ConfigContent | Out-File -FilePath $configPath -Encoding UTF8
    Write-ColorOutput "Configuration created at $configPath" "Green"
    
    # Create PowerShell profile
    $ProfileDir = Split-Path $PROFILE -Parent
    if (-not (Test-Path $ProfileDir)) {
        New-Item -ItemType Directory -Force -Path $ProfileDir | Out-Null
    }
    
    $AliasLine = @"

# DONGOL - Made in Indonesia
function dongol { python -m dongol.cli `$args }
function dong { dongol `$args }
Set-Alias -Name dong -Value dongol

# Completion
if (Get-Command Register-ArgumentCompleter -ErrorAction SilentlyContinue) {
    Register-ArgumentCompleter -CommandName dongol,dong -ScriptBlock {
        param(`$wordToComplete, `$commandAst, `$cursorPosition)
        @('think', 'chunk', 'run', 'status', 'analyze') | Where-Object { `$_ -like "`$wordToComplete*" }
    }
}
"@
    
    if (-not (Test-Path $PROFILE) -or (Get-Content $PROFILE -Raw) -notlike "*DONGOL*") {
        $AliasLine | Out-File -FilePath $PROFILE -Append -Encoding UTF8
        Write-ColorOutput "PowerShell aliases added" "Green"
    }
    
    # Add to PATH
    $UserPath = [Environment]::GetEnvironmentVariable("PATH", "User")
    if ($UserPath -notlike "*$InstallDir*") {
        [Environment]::SetEnvironmentVariable("PATH", "$UserPath;$InstallDir", "User")
        Write-ColorOutput "Added to PATH" "Green"
    }
    
    # Success message
    Write-ColorOutput @"

╔═══════════════════════════════════════════════════════════════╗
║                    Installation Complete!                     ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  DONGOL has been installed successfully!                      ║
║                                                               ║
║  Made in Indonesia by:                                        ║
║  Ardellio Satria Anindito                                     ║
║  SMA Kartika XIX-1 Bandung                                    ║
║                                                               ║
║  Quick start:                                                 ║
║    dongol --help                                              ║
║    dongol status                                              ║
║    dongol think "Hello World" --parallel                     ║
║                                                               ║
║  Documentation: https://docs.dongol.io                      ║
║  Community: https://discord.gg/dongol                        ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
"@ "Green"
    
    Write-ColorOutput "`nPlease restart your PowerShell to use DONGOL`n" "Yellow"
}

# Run installation
Install-Dongol
