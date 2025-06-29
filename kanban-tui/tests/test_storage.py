import json
import os
from unittest.mock import patch
from pathlib import Path

from storage import load_board, save_board

# Define a mock board structure for testing
MOCK_BOARD = {
    "columns": [
        {
            "title": "Test Column",
            "cards": [
                {"label": "Test Card", "description": "A test card"}
            ]
        }
    ]
}

# Define a path for a temporary test file
TEST_BOARD_PATH = "./test_board.json"

@patch('storage.DATA_FILE', Path(TEST_BOARD_PATH))
def test_save_and_load_board():
    """Tests that saving and loading a board works correctly."""
    try:
        # 1. Save the mock board
        save_board(MOCK_BOARD)

        # 2. Check if the file was created and has the correct content
        assert os.path.exists(TEST_BOARD_PATH)
        with open(TEST_BOARD_PATH, 'r') as f:
            content = json.load(f)
        assert content == MOCK_BOARD

        # 3. Load the board and check if it matches
        loaded = load_board()
        assert loaded == MOCK_BOARD

    finally:
        # 4. Clean up the test file
        if os.path.exists(TEST_BOARD_PATH):
            os.remove(TEST_BOARD_PATH)
