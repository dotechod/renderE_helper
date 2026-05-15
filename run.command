#!/bin/zsh
cd "$(dirname "$0")"
VENV_DIR=".venv"
REPO_URL="https://github.com/dotechod/renderE_helper.git" # Replace with your helper app repo URL if different

# 1. Relaunch in a visual terminal if running in the background
if [[ ! -t 0 ]]; then
    gnome-terminal -- zsh -c "$0; read" || \
    konsole -e zsh -c "$0; read" || \
    xterm -e zsh -c "$0; read"
    exit
fi

# 2. Handle Git Updates for the Root Directory
if [ ! -d ".git" ]; then
    echo "Initializing and pulling Helper App from Git..."
    git init
    git remote add origin "$REPO_URL"
    git fetch
    # This pulls the files into the current directory without making a subfolder
    git checkout -t origin/master --force 
else
    echo "Checking for Helper App updates..."
    # Clean up any local changes that might block a pull, then update
    git pull origin master
fi

# 3. Handle Python Virtual Environment Setup
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
else
    echo "Virtual environment already exists."
fi

# 4. Activate VENV and Sync Dependencies
source "$VENV_DIR/bin/activate"

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

# Sync renderE's own requirements too if the folder exists
if [ -f "renderE/requirements.txt" ]; then
    pip install -r "renderE/requirements.txt"
fi

# 5. Launch the Application
if [ -f "main.py" ]; then
    echo "Launching renderE Helper..."
    python main.py
else
    echo "Error: main.py not found!"
fi