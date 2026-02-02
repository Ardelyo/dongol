#!/usr/bin/env python3
"""
DONGOL Setup Script
Easy installation and configuration
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path


DONGOL_ASCII = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   ██████   ██████  ███    ██  ██████   ██████               ║
║   ██   ██ ██    ██ ████   ██ ██       ██    ██              ║
║   ██   ██ ██    ██ ██ ██  ██ ██   ███ ██    ██              ║
║   ██   ██ ██    ██ ██  ██ ██ ██    ██ ██    ██              ║
║   ██████   ██████  ██   ████  ██████   ██████               ║
║                                                               ║
║   Distributed Orchestration for Navigating Goals            ║
║   and Operational Logic                                       ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
"""


def print_banner():
    print(DONGOL_ASCII)


def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ Python 3.9+ is required")
        sys.exit(1)
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")


def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-e", "."],
            check=True,
            cwd=Path(__file__).parent
        )
        print("✓ Dependencies installed")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        sys.exit(1)


def create_config():
    """Create default configuration"""
    print("\n⚙️  Setting up configuration...")
    
    config_dir = Path.home() / ".dongol"
    config_file = config_dir / "config.yaml"
    data_dir = config_dir / "data"
    
    # Create directories
    config_dir.mkdir(exist_ok=True)
    data_dir.mkdir(exist_ok=True)
    
    # Copy default config if doesn't exist
    default_config = Path(__file__).parent / "config" / "default.yaml"
    if default_config.exists() and not config_file.exists():
        shutil.copy(default_config, config_file)
        print(f"✓ Created config at {config_file}")
    else:
        print(f"✓ Config already exists at {config_file}")
    
    return config_dir


def setup_shell_integration():
    """Setup shell integration"""
    print("\n🐚 Setting up shell integration...")
    
    shell = os.environ.get('SHELL', '').split('/')[-1]
    home = Path.home()
    
    if shell == 'bash':
        rc_file = home / '.bashrc'
    elif shell == 'zsh':
        rc_file = home / '.zshrc'
    elif 'powershell' in shell.lower() or os.name == 'nt':
        # PowerShell
        print("  Add to your PowerShell profile:")
        print("  Import-Module dongol")
        return
    else:
        print(f"  ⚠️  Unknown shell: {shell}")
        return
    
    # Add completion and alias
    completion_line = '\n# DONGOL integration\neval "$(_DONGOL_COMPLETE=bash_source dongol)"\nalias dong="dongol"\n'
    
    if rc_file.exists():
        content = rc_file.read_text()
        if 'DONGOL' not in content:
            with open(rc_file, 'a') as f:
                f.write(completion_line)
            print(f"✓ Added to {rc_file}")
        else:
            print(f"✓ Already configured in {rc_file}")
    
    print("  💡 Restart your shell or run: source ~/.bashrc")


def verify_installation():
    """Verify the installation"""
    print("\n🔍 Verifying installation...")
    
    try:
        # Try importing
        sys.path.insert(0, str(Path(__file__).parent))
        from core.engine import DongolEngine
        print("✓ Core engine import successful")
        
        # Check CLI
        result = subprocess.run(
            [sys.executable, "-m", "cli.main", "--help"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent
        )
        if result.returncode == 0:
            print("✓ CLI is working")
        else:
            print("⚠️  CLI check failed")
        
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        sys.exit(1)


def print_usage():
    """Print usage information"""
    print("""
╔═══════════════════════════════════════════════════════════════╗
║                    🎉 Setup Complete! 🎉                      ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  Quick Start:                                                 ║
║                                                               ║
║    dongol think "Your question here"                         ║
║    dongol status                                             ║
║    dongol --help                                             ║
║                                                               ║
║  Python API:                                                  ║
║                                                               ║
║    from dongol import DongolEngine                           ║
║    engine = await DongolEngine.create()                      ║
║    task = await engine.create_task("Hello", "World")         ║
║                                                               ║
║  Documentation:                                               ║
║    https://docs.dongol.io                                    ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
""")


def main():
    """Main setup function"""
    print_banner()
    
    print("Setting up DONGOL - Universal Task Management System")
    print("=" * 60)
    
    # Run setup steps
    check_python_version()
    install_dependencies()
    config_dir = create_config()
    setup_shell_integration()
    verify_installation()
    
    print_usage()
    
    print(f"\nConfig directory: {config_dir}")
    print("Happy parallel thinking! 🧠")


if __name__ == "__main__":
    main()
