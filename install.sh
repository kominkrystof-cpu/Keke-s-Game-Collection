#!/bin/bash
# Installation script for Keke's Game Collection

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="$HOME/.local/bin"
ALIAS_NAME="kekegames"

echo "Installing Keke's Game Collection..."

# Create install directory if it doesn't exist
mkdir -p "$INSTALL_DIR"

# Create launcher script
cat > "$INSTALL_DIR/$ALIAS_NAME" << EOF
#!/bin/bash
cd "$SCRIPT_DIR"
python3 main.py
EOF

# Make launcher executable
chmod +x "$INSTALL_DIR/$ALIAS_NAME"

# Check if INSTALL_DIR is in PATH
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo ""
    echo "⚠️  WARNING: $INSTALL_DIR is not in your PATH"
    echo ""
    echo "Add the following to your ~/.bashrc or ~/.zshrc:"
    echo "  export PATH=\"\$PATH:$INSTALL_DIR\""
    echo ""
    echo "Then run: source ~/.bashrc  (or source ~/.zshrc)"
else
    echo "✓ Installation complete!"
    echo "Run '$ALIAS_NAME' from anywhere to launch the game collection."
fi
