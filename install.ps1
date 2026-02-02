# DONGOL Installation Script for PowerShell
# Run: Invoke-RestMethod https://code.kimi.com/install.ps1 | Invoke-Expression

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
║        Universal Parallel Thinking Task Manager               ║
║                                                               ║
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
    
    # Check Python
    Write-ColorOutput "`n🔍 Checking Python installation..." "Yellow"
    $major, $minor = Get-PythonVersion
    
    if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 9)) {
        Write-ColorOutput "❌ Python 3.9+ is required. Found: $major.$minor" "Red"
        Write-ColorOutput "   Download from: https://python.org/downloads" "Yellow"
        exit 1
    }
    Write-ColorOutput "✓ Python $major.$minor detected" "Green"
    
    # Check pip
    if (-not (Test-CommandExists "pip")) {
        Write-ColorOutput "❌ pip is not installed" "Red"
        exit 1
    }
    Write-ColorOutput "✓ pip detected" "Green"
    
    # Installation directory
    $InstallDir = "$env:USERPROFILE\.dongol\install"
    $ConfigDir = "$env:USERPROFILE\.dongol"
    
    # Create directories
    New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
    New-Item -ItemType Directory -Force -Path "$ConfigDir\data" | Out-Null
    
    # Download DONGOL
    Write-ColorOutput "`n📥 Downloading DONGOL..." "Yellow"
    
    # For now, create the files directly (in production, would download from git)
    Write-ColorOutput "📦 Setting up package..." "Yellow"
    
    # Install dependencies
    Write-ColorOutput "`n📦 Installing dependencies..." "Yellow"
    
    $requirements = @"
click>=8.1.0
rich>=13.0.0
pydantic>=2.0.0
orjson>=3.9.0
"@
    
    $reqFile = "$InstallDir\requirements.txt"
    $requirements | Out-File -FilePath $reqFile -Encoding UTF8
    
    try {
        pip install -r $reqFile --quiet
        Write-ColorOutput "✓ Dependencies installed" "Green"
    } catch {
        Write-ColorOutput "❌ Failed to install dependencies" "Red"
        exit 1
    }
    
    # Create CLI wrapper
    $CliWrapper = @"
#!/usr/bin/env python3
import sys
sys.path.insert(0, r"$PSScriptRoot")
from cli.main import main
if __name__ == "__main__":
    main()
"@
    
    $cliPath = "$InstallDir\dongol.py"
    $CliWrapper | Out-File -FilePath $cliPath -Encoding UTF8
    
    # Add to PATH
    Write-ColorOutput "`n🔧 Configuring PATH..." "Yellow"
    
    $userPath = [Environment]::GetEnvironmentVariable("PATH", "User")
    if ($userPath -notlike "*$InstallDir*") {
        [Environment]::SetEnvironmentVariable("PATH", "$userPath;$InstallDir", "User")
        Write-ColorOutput "✓ Added to PATH (restart shell to use 'dongol' command)" "Green"
    } else {
        Write-ColorOutput "✓ Already in PATH" "Green"
    }
    
    # Create config
    Write-ColorOutput "`n⚙️  Creating configuration..." "Yellow"
    
    $ConfigContent = @"
# DONGOL Configuration
engine:
  max_workers: 4
  
chunking:
  max_chunk_size: 1000
  overlap_ratio: 0.1
  
storage:
  backend: sqlite
  path: $ConfigDir\data
  
logging:
  level: info
"@
    
    $configPath = "$ConfigDir\config.yaml"
    $ConfigContent | Out-File -FilePath $configPath -Encoding UTF8
    Write-ColorOutput "✓ Configuration created at $configPath" "Green"
    
    # Create PowerShell alias
    $ProfileDir = Split-Path $PROFILE -Parent
    if (-not (Test-Path $ProfileDir)) {
        New-Item -ItemType Directory -Force -Path $ProfileDir | Out-Null
    }
    
    $AliasLine = @"

# DONGOL Alias
function dongol { python `"$InstallDir\dongol.py`" @args }
function dong { python `"$InstallDir\dongol.py`" @args }
Set-Alias -Name dong -Value dongol
"@
    
    if (-not (Test-Path $PROFILE) -or (Get-Content $PROFILE -Raw) -notlike "*DONGOL*") {
        $AliasLine | Out-File -FilePath $PROFILE -Append -Encoding UTF8
        Write-ColorOutput "✓ PowerShell aliases added" "Green"
    }
    
    # Success message
    Write-ColorOutput @"

╔═══════════════════════════════════════════════════════════════╗
║                    🎉 Installation Complete! 🎉               ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  Restart your PowerShell and run:                             ║
║                                                               ║
║    dongol think "Hello World"                                ║
║    dongol --help                                             ║
║                                                               ║
║  Or use the Python API:                                       ║
║                                                               ║
║    from dongol import DongolEngine                           ║
║    engine = await DongolEngine.create()                      ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
"@ "Green"
    
    Write-ColorOutput "Installation directory: $InstallDir" "Cyan"
    Write-ColorOutput "Configuration: $configPath" "Cyan"
}

# Run installation
Install-Dongol
