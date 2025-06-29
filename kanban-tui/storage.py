import json
from pathlib import Path
from typing import Dict, Any

# The path to the file where the board data will be stored.
DATA_FILE = Path.home() / ".adp_planner_board.json"

def get_default_data() -> Dict[str, Any]:
    """Returns the default structure for a new board."""
    return {
        "columns": [
            {"title": "Input Queue", "cards": []},
            {"title": "In Progress", "cards": []},
            {"title": "Done", "cards": []},
        ]
    }

def load_board() -> Dict[str, Any]:
    """
    Loads the board data from the JSON file.
    If the file doesn't exist, it creates a default board.
    """
    if not DATA_FILE.exists():
        board_data = get_default_data()
        save_board(board_data)
        return board_data
    
    with DATA_FILE.open("r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            # If the file is corrupted or empty, return default data
            return get_default_data()

def save_board(data: Dict[str, Any]) -> None:
    """Saves the entire board data to the JSON file."""
    with DATA_FILE.open("w") as f:
        json.dump(data, f, indent=4)
