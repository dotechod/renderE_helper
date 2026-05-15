#!/bin/bash
cd "$(dirname"$0")"
VENV_DIR=".venv"
if [[ ! -t 0 ]]; then
    gnome-terminal -- zsh -c "$0; read" || \
    konsole -e zsh -c "$0; read" || \
    xterm -e zsh -c "$0; read"
    exit
fi

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
else
    echo "Virtual environment already exists."
fi
source .venv/bin/activate
pip install -r requirements.txt
python main.py
