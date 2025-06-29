import pytest
from textual.app import App
from textual.widgets import Input, Button
from textual.screen import Screen
from unittest.mock import patch, MagicMock
from copy import deepcopy

from board import KanbanApp, Card, Column, AddCardScreen

# Mock initial board data for tests
MOCK_INITIAL_BOARD_DATA = {
    "columns": [
        {"title": "Input Queue", "cards": []},
        {"title": "In Progress", "cards": []},
        {"title": "Done", "cards": []},
    ]
}

@pytest.mark.asyncio
@patch('storage.load_board', return_value=deepcopy(MOCK_INITIAL_BOARD_DATA))
@patch('board.save_board')
async def test_add_card(mock_save_board, mock_load_board):
    """Test adding a new card via the UI."""
    async with KanbanApp().run_test() as driver:
        app = driver.app
        await app.query(Column).wait_for_ready() # Wait for the initial columns to be rendered

        # 1. Simulate pressing 'a' to open the Add Card dialog
        await driver.press("a")

        # Ensure the AddCardScreen is pushed
        assert isinstance(app.screen, AddCardScreen)

        # 2. Simulate typing title and description
        title_input = app.screen.query_one("#title", Input)
        description_input = app.screen.query_one("#description", Input)

        title_input.value = "New Card Title"
        description_input.value = "This is a new card description"

        # 3. Simulate clicking the Save button
        await driver.click("#save")

        # Ensure the dialog is dismissed and we are back to the main screen
        assert isinstance(app.screen, Screen)

        # 4. Assert that a new Card widget appears in the first Column
        first_column = app.query_one(Column)
        cards_in_column = first_column.query(Card)
        assert len(cards_in_column) == 1
        new_card = cards_in_column.first()
        assert new_card.label == "New Card Title"

        # 5. Assert that the board_data in the KanbanApp instance has been updated
        expected_board_data = {
            "columns": [
                {"title": "Input Queue", "cards": [
                    {"label": "New Card Title", "description": "This is a new card description"}
                ]},
                {"title": "In Progress", "cards": []},
                {"title": "Done", "cards": []},
            ]
        }
        assert app.board_data == expected_board_data

        # 6. Assert that save_board was called with the updated data
        mock_save_board.assert_called_once_with(expected_board_data)