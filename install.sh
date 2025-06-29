#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

REPO_DIR="$(dirname "$(realpath "$0")")"
APP_DIR="$REPO_DIR/kanban-tui"
COMMAND_NAME="planner"
INSTALL_PATH="/usr/local/bin/$COMMAND_NAME"
VENV_DIR="$REPO_DIR/.venv"

echo "Setting up adp-planner..."

# 1. Create virtual environment
echo "Creating virtual environment..."
python3 -m venv "$VENV_DIR"

# 2. Activate virtual environment and install dependencies
echo "Installing Python dependencies in virtual environment..."
source "$VENV_DIR/bin/activate"
pip install textual==3.3.0

# 3. Create the planner command script that uses the virtual environment
echo "Creating the '$COMMAND_NAME' command script..."
cat << EOF > "$REPO_DIR/$COMMAND_NAME"
#!/bin/bash
# Activate virtual environment and run the app
source "$VENV_DIR/bin/activate"
python3 "$APP_DIR/main.py"
EOF

# 4. Make the script executable
echo "Making the '$COMMAND_NAME' script executable..."
chmod +x "$REPO_DIR/$COMMAND_NAME"

# 5. Move the script to /usr/local/bin
echo "Moving '$COMMAND_NAME' to $INSTALL_PATH (requires sudo)..."
sudo mv "$REPO_DIR/$COMMAND_NAME" "$INSTALL_PATH"

echo "Setup complete! You can now run 'adp-planner' by typing '$COMMAND_NAME' in your terminal."
echo "The virtual environment is located at: $VENV_DIR"
