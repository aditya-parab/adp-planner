# adp-planner

A personal planner and Kanban board application designed for the terminal. Built with Python and the Textual framework, this application allows you to manage your tasks and workflows directly from your command line interface.

## Features

*   **Intuitive Interface**: Clean and responsive terminal UI.
*   **Task Management**: Add, edit, and delete cards (tasks).
*   **Column Organization**: Create, rename, and delete columns to categorize your workflow stages.
*   **Local Data Persistence**: All your board data is automatically saved and loaded to a user-specific file (`~/.adp_planner_board.json`), ensuring your data is private and separate from the project's code.
*   **Card Details**: View and edit extended details for each card.
*   **Keyboard Navigation**: Move cards between columns using arrow keys.
*   **Customizable**: Easily modify the look and feel through CSS.

## Prerequisites

Before installing, ensure you have:
*   **Python 3.8 or higher** installed on your system
*   **sudo access** for installing the global command

## Installation and Setup

Follow these steps to get your `adp-planner` up and running:

### 1. Clone the Repository

First, clone this repository to your local machine:

```bash
git clone https://github.com/YOUR_USERNAME/adp-planner.git
cd adp-planner
```

### 2. Run the Installation Script

This project includes an `install.sh` script to automate the setup process. This script will:
*   Create a virtual environment to isolate dependencies
*   Install the necessary Python dependencies (Textual framework)
*   Create a `planner` command that you can run from any terminal location

To run the installation script:

```bash
chmod +x install.sh
sudo ./install.sh
```

**Important Notes:**
*   The `sudo` command is required because the script installs the `planner` command to `/usr/local/bin/` for system-wide access
*   The script creates a virtual environment (`.venv`) in the project directory to manage dependencies safely
*   This approach respects modern Python environment management policies and avoids conflicts with system packages

### 3. Run the Application

After completing the setup, you can open `adp-planner` from any terminal by simply typing:

```bash
planner
```

## Troubleshooting

### Virtual Environment
If you encounter issues with the installation:
*   The virtual environment is created in `.venv/` within the project directory
*   Dependencies are installed only within this isolated environment
*   The global `planner` command automatically activates this environment when run

### Alternative Installation Methods

If the standard installation doesn't work for your system, you can try:

#### Using pipx (Recommended for some systems)
```bash
# Install pipx if you don't have it
brew install pipx  # On macOS
# or
pip install --user pipx  # On other systems

# Install the application
cd kanban-tui
pipx install .
```

#### Manual Virtual Environment Setup
```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install textual==3.3.0

# Run directly
python3 kanban-tui/main.py
```

## Development

To contribute to the project or run it in development mode:

1. Clone the repository
2. Create a virtual environment: `python3 -m venv .venv`
3. Activate it: `source .venv/bin/activate`
4. Install dependencies: `pip install textual==3.3.0`
5. Run the app: `python3 kanban-tui/main.py`

Enjoy managing your tasks with adp-planner!