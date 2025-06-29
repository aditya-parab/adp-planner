#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

REPO_DIR="$(dirname "$(realpath "$0")")"
APP_DIR="$REPO_DIR/kanban-tui"
COMMAND_NAME="planner"
INSTALL_PATH="/usr/local/bin/$COMMAND_NAME"

echo "Setting up adp-planner..."

# 1. Install Python dependencies
echo "Installing Python dependencies..."
pip install -e "$REPO_DIR"

# 2. Create the planner command script
echo "Creating the '$COMMAND_NAME' command script..."
cat << EOF > "$REPO_DIR/$COMMAND_NAME"
#!/bin/bash
python3 "$APP_DIR/main.py"
EOF

# 3. Make the script executable
echo "Making the '$COMMAND_NAME' script executable..."
chmod +x "$REPO_DIR/$COMMAND_NAME"

# 4. Move the script to /usr/local/bin
echo "Moving '$COMMAND_NAME' to $INSTALL_PATH (requires sudo)..."
sudo mv "$REPO_DIR/$COMMAND_NAME" "$INSTALL_PATH"

echo "Setup complete! You can now run 'adp-planner' by typing '$COMMAND_NAME' in your terminal."
