#!/bin/bash
# DONGOL Universal Installation Script
# Made in Indonesia 🇮🇩
# Supports: Linux, macOS, Windows (WSL)

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                                                               ║"
echo "║   ██████   ██████  ███    ██  ██████   ██████               ║"
echo "║   ██   ██ ██    ██ ████   ██ ██       ██    ██              ║"
echo "║   ██   ██ ██    ██ ██ ██  ██ ██   ███ ██    ██              ║"
echo "║   ██   ██ ██    ██ ██  ██ ██ ██    ██ ██    ██              ║"
echo "║   ██████   ██████  ██   ████  ██████   ██████               ║"
echo "║                                                               ║"
echo "║              Made in Indonesia 🇮🇩                             ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

DONGOL_VERSION="0.1.0"
INSTALL_DIR="$HOME/.local/bin"
CONFIG_DIR="$HOME/.dongol"

# Detect OS
OS="$(uname -s)"
ARCH="$(uname -m)"

echo -e "${GREEN}Installing DONGOL v${DONGOL_VERSION}...${NC}"
echo "Detected: $OS $ARCH"

# Check Python
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
        echo -e "${GREEN}✓ Python found: $PYTHON_VERSION${NC}"
        
        # Check version >= 3.9
        PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
        PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
        
        if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 9 ]); then
            echo -e "${RED}✗ Python 3.9+ required${NC}"
            exit 1
        fi
    else
        echo -e "${RED}✗ Python 3 not found. Please install Python 3.9+${NC}"
        exit 1
    fi
}

# Check pip
check_pip() {
    if command -v pip3 &> /dev/null; then
        echo -e "${GREEN}✓ pip found${NC}"
    else
        echo -e "${YELLOW}⚠ pip not found. Installing...${NC}"
        python3 -m ensurepip --upgrade
    fi
}

# Install DONGOL
install_dongol() {
    echo -e "${BLUE}Installing DONGOL...${NC}"
    
    # Create directories
    mkdir -p "$INSTALL_DIR"
    mkdir -p "$CONFIG_DIR"
    
    # Download latest release
    if command -v curl &> /dev/null; then
        DOWNLOAD_CMD="curl -fsSL"
    elif command -v wget &> /dev/null; then
        DOWNLOAD_CMD="wget -qO-"
    else
        echo -e "${RED}✗ curl or wget required${NC}"
        exit 1
    fi
    
    # Clone repository
    TEMP_DIR=$(mktemp -d)
    cd "$TEMP_DIR"
    
    echo "Downloading DONGOL..."
    git clone --depth 1 https://github.com/dongol-org/dongol.git 2>/dev/null || {
        echo -e "${YELLOW}⚠ Git clone failed. Using pip instead...${NC}"
        pip3 install dongol
        return
    }
    
    cd dongol
    pip3 install -e ".[all]" --user
    
    # Cleanup
    cd "$HOME"
    rm -rf "$TEMP_DIR"
}

# Setup shell integration
setup_shell() {
    echo -e "${BLUE}Setting up shell integration...${NC}"
    
    SHELL_CONFIG=""
    if [ "$SHELL" = "/bin/bash" ]; then
        SHELL_CONFIG="$HOME/.bashrc"
    elif [ "$SHELL" = "/bin/zsh" ]; then
        SHELL_CONFIG="$HOME/.zshrc"
    fi
    
    if [ -n "$SHELL_CONFIG" ]; then
        echo "" >> "$SHELL_CONFIG"
        echo "# DONGOL" >> "$SHELL_CONFIG"
        echo 'eval "$(_DONGOL_COMPLETE=bash_source dongol)"' >> "$SHELL_CONFIG"
        echo "alias dong='dongol'" >> "$SHELL_CONFIG"
        echo -e "${GREEN}✓ Shell integration added to $SHELL_CONFIG${NC}"
    fi
}

# Create config
create_config() {
    echo -e "${BLUE}Creating default configuration...${NC}"
    
    cat > "$CONFIG_DIR/config.yaml" << 'EOF'
# DONGOL Configuration
# Dibuat di Indonesia 🇮🇩

engine:
  max_workers: 4
  use_processes: false

chunking:
  max_chunk_size: 1000
  overlap_ratio: 0.1

storage:
  backend: sqlite
  path: ~/.dongol/data

logging:
  level: info
  
i18n:
  default_language: id  # id, en, jp
EOF
    
    echo -e "${GREEN}✓ Config created at $CONFIG_DIR/config.yaml${NC}"
}

# Main installation
main() {
    echo ""
    check_python
    check_pip
    install_dongol
    setup_shell
    create_config
    
    echo ""
    echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}              Installation Complete!${NC}"
    echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo "DONGOL v${DONGOL_VERSION} has been installed successfully!"
    echo ""
    echo "Made in Indonesia 🇮🇩 by Ardellio Satria Anindito"
    echo "SMA Kartika XIX-1 Bandung"
    echo ""
    echo "Quick start:"
    echo "  dongol --help"
    echo "  dongol status"
    echo "  dongol think 'Hello World' --parallel"
    echo ""
    echo "Documentation: https://docs.dongol.io"
    echo "Community: https://discord.gg/dongol"
    echo ""
    echo -e "${YELLOW}Please restart your terminal or run: source $SHELL_CONFIG${NC}"
    echo ""
}

# Run
main
