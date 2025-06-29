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
*   Install the necessary Python dependencies.
*   Create a `planner` command that you can run from any terminal location.

To run the installation script:

```bash
chmod +x install.sh
sudo ./install.sh
```

**Important:** The `sudo` command is required because the script moves the `planner` command to a system-wide directory (`/usr/local/bin/`). You will be prompted for your system password.

### 3. Run the Application

After completing the setup, you can open `adp-planner` from any terminal by simply typing:

```bash
planner
```

Enjoy managing your tasks with adp-planner!