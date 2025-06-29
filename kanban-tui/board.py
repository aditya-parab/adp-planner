from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Header, Footer, Button, Input, Static, TextArea
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import Screen, ModalScreen
from textual.events import MouseDown, MouseMove, MouseUp

from storage import load_board, save_board, DATA_FILE, get_default_data


class Card(Static):
    """A draggable card widget."""
    can_focus = True
    can_drag = True

    def __init__(self, label: str, description: str, details: str = "") -> None:
        self.label = label
        self.description = description
        self.details = details
        super().__init__(label)

    def render(self) -> str:
        """Render the card with label and description."""
        return f"{self.label}\n[dim]{self.description}[/dim]"

    def on_mouse_down(self, event: MouseDown) -> None:
        self.app.set_focus(self)
        self.app.start_dragging(self, event)

    def on_mouse_move(self, event: MouseMove) -> None:
        self.app.drag_move(event)

    def on_mouse_up(self, event: MouseUp) -> None:
        self.app.end_dragging(event)

class Column(Vertical):
    """A column in the Kanban board."""
    can_focus = True
    def __init__(self, title: str, cards_data: list) -> None:
        super().__init__()
        self.title = title
        self.cards_data = cards_data
        self.card_list_widget = VerticalScroll(classes="card-list")

    def compose(self) -> ComposeResult:
        yield Static(self.title, classes="column-title")
        yield self.card_list_widget

    def on_mount(self) -> None:
        """Called when the column is mounted, adds cards to the column."""
        for card_data in self.cards_data:
            card = Card(label=card_data["label"], description=card_data.get("description", ""), details=card_data.get("details", ""))
            self.card_list_widget.mount(card)

    def add_card_widget(self, card: Card) -> None:
        """Adds a card widget to this column."""
        self.card_list_widget.mount(card)

class AddCardScreen(ModalScreen):
    """Screen with a dialog to add a new card."""

    def __init__(self, initial_title: str = "", initial_description: str = "", initial_details: str = "") -> None:
        super().__init__()
        self.initial_title = initial_title
        self.initial_description = initial_description
        self.initial_details = initial_details

    def compose(self) -> ComposeResult:
        yield Vertical(
            Static("Add/Edit Card", classes="dialog-title"),
            Input(placeholder="Title", id="title", value=self.initial_title),
            Input(placeholder="Description", id="description", value=self.initial_description),
            TextArea(id="details", text=self.initial_details, classes="details-textarea"),
            Horizontal(
                Button("Save", variant="primary", id="save"),
                Button("Cancel", id="cancel"),
                classes="dialog-buttons",
            ),
            classes="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            title = self.query_one("#title", Input).value
            description = self.query_one("#description", Input).value
            details = self.query_one("#details", TextArea).text
            if title:
                self.dismiss((title, description, details))
            else:
                self.dismiss(None)
        else:
            self.dismiss(None)


class AddColumnScreen(ModalScreen):
    """Screen with a dialog to add a new column."""

    def __init__(self, initial_title: str = "") -> None:
        super().__init__()
        self.initial_title = initial_title

    def compose(self) -> ComposeResult:
        yield Vertical(
            Static("Add New Column", classes="dialog-title"),
            Input(placeholder="Column Title", id="column_title", value=self.initial_title),
            Horizontal(
                Button("Save", variant="primary", id="save"),
                Button("Cancel", id="cancel"),
                classes="dialog-buttons",
            ),
            classes="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            column_title = self.query_one("#column_title", Input).value
            if column_title:
                self.dismiss(column_title)
            else:
                self.dismiss(None)
        else:
            self.dismiss(None)


class ConfirmScreen(ModalScreen):
    """Screen with a confirmation dialog."""

    def __init__(self, message: str) -> None:
        super().__init__()
        self.message = message

    def compose(self) -> ComposeResult:
        yield Vertical(
            Static(self.message, classes="dialog-title"),
            Horizontal(
                Button("Yes", variant="error", id="yes"),
                Button("No", id="no"),
                classes="dialog-buttons",
            ),
            classes="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(event.button.id == "yes")

class CardDetailScreen(ModalScreen):
    """Screen to display card details."""

    def __init__(self, card: Card) -> None:
        super().__init__()
        self.card = card

    def compose(self) -> ComposeResult:
        yield Vertical(
            Static(f"[bold]Title:[/] {self.card.label}"),
            Static(f"[bold]Description:[/] {self.card.description}"),
            Static("[bold]Details:[/]"),
            Static(self.card.details),
            Button("Close", id="close"),
            classes="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss()


class KanbanApp(App):
    """A simple Kanban board app for the terminal."""

    CSS_PATH = "board.css"

    def __init__(self):
        super().__init__()
        self._drag_card = None

    BINDINGS = [
        Binding(key="a", action="add_card", description="Add Card"),
        Binding(key="d", action="delete_card", description="Delete Card"),
        Binding(key="left", action="move_card_left", description="Move Card Left"),
        Binding(key="right", action="move_card_right", description="Move Card Right"),
        Binding(key="e", action="edit_card", description="Edit Card"),
        Binding(key="i", action="view_card_details", description="View Details"),
        Binding(key="c", action="add_column", description="Add Column"),
        Binding(key="x", action="delete_column", description="Delete Column"),
        Binding(key="r", action="rename_column", description="Rename Column"),
        Binding(key="ctrl+x", action="clear_board", description="Clear Board"),
        Binding(key="up", action="focus_up", description="Focus Up"),
        Binding(key="down", action="focus_down", description="Focus Down"),
        Binding(key="left", action="focus_left", description="Focus Left"),
        Binding(key="right", action="focus_right", description="Focus Right"),
        Binding(key="q", action="quit", description="Quit the app"),
    ]

    def on_mount(self) -> None:
        """Called when the app is first mounted."""
        self.board_data = load_board()

    def on_ready(self) -> None:
        """Called when the DOM is ready."""
        self.rebuild_board()

    def start_dragging(self, card: Card, event: MouseDown) -> None:
        self._drag_card = card
        self._drag_offset_x = event.x - card.offset.x
        self._drag_offset_y = event.y - card.offset.y
        card.add_class("dragging")

    def drag_move(self, event: MouseMove) -> None:
        if self._drag_card:
            self._drag_card.offset = (event.x - self._drag_offset_x, event.y - self._drag_offset_y)

    def end_dragging(self, event: MouseUp) -> None:
        if self._drag_card:
            self._drag_card.display = False
            target_column = None
            for column in self.query(Column):
                if column.region.contains(event.screen_x, event.screen_y):
                    target_column = column
                    break
            self._drag_card.display = True

            if target_column and target_column != self._drag_card.parent.parent:
                old_column_widget = self._drag_card.parent.parent
                old_column_index = list(self.query(Column)).index(old_column_widget)

                card_data_to_move = {
                    "label": self._drag_card.label,
                    "description": self._drag_card.description
                }

                self.board_data["columns"][old_column_index]["cards"] = [
                    card for card in self.board_data["columns"][old_column_index]["cards"]
                    if not (card["label"] == card_data_to_move["label"] and card.get("description", "") == card_data_to_move["description"])
                ]

                new_column_index = list(self.query(Column)).index(target_column)
                self.board_data["columns"][new_column_index]["cards"].append(card_data_to_move)

                save_board(self.board_data)
                self.rebuild_board()

            if self._drag_card:
                self._drag_card.remove_class("dragging")
                self._drag_card = None

    def rebuild_board(self):
        """Clears and rebuilds the board from the board_data."""
        board_container = self.query_one("#board-container")
        board_container.remove_children()

        for column_data in self.board_data["columns"]:
            column = Column(title=column_data["title"], cards_data=column_data["cards"])
            board_container.mount(column)

    def action_add_card(self) -> None:
        """Action to add a new card."""
        # Ensure there's at least one column before pushing the screen
        if not self.board_data["columns"]:
            from storage import get_default_data
            self.board_data = get_default_data()
            self.rebuild_board()

        def add_card_callback(data):
            if data:
                title, description, details = data
                new_card_data = {"label": title, "description": description, "details": details}
                
                # Add to data structure
                self.board_data["columns"][0]["cards"].append(new_card_data)
                
                # Add to UI
                new_card = Card(label=title, description=description)
                first_column = self.query(Column).first() # Use .first() to get the first column
                if first_column: # Ensure a column exists before adding the widget
                    first_column.add_card_widget(new_card)

                # Save the new state
                save_board(self.board_data)

        self.push_screen(AddCardScreen(), add_card_callback)

    def action_add_column(self) -> None:
        """Action to add a new column."""
        def add_column_callback(column_title):
            if column_title:
                new_column_data = {"title": column_title, "cards": []}
                self.board_data["columns"].append(new_column_data)
                
                # Add to UI
                new_column = Column(title=column_title, cards_data=[])
                self.query_one("#board-container").mount(new_column)

                # Save the new state
                save_board(self.board_data)

        self.push_screen(AddColumnScreen(), add_column_callback)

    def action_delete_card(self) -> None:
        """Action to delete the currently focused card."""
        if isinstance(self.focused, Card):
            card_to_delete = self.focused
            
            # Remove from UI
            card_to_delete.remove()

            # Remove from data structure
            for column_data in self.board_data["columns"]:
                column_data["cards"] = [
                    card for card in column_data["cards"]
                    if not (card["label"] == card_to_delete.label and card.get("description", "") == card_to_delete.description)
                ]
            
            # Save the new state
            save_board(self.board_data)

    def _move_card(self, direction: int) -> None:
        """Helper method to move the focused card left or right."""
        if isinstance(self.focused, Card):
            card_to_move = self.focused
            current_card_list_widget = card_to_move.parent
            current_column_widget = current_card_list_widget.parent

            all_columns = list(self.query(Column))
            current_column_index = all_columns.index(current_column_widget)
            
            target_column_index = current_column_index + direction

            if 0 <= target_column_index < len(all_columns):
                target_column_widget = all_columns[target_column_index]

                # Update data structure
                card_data_to_move = {
                    "label": card_to_move.label,
                    "description": card_to_move.description
                }

                # Remove from old column data
                self.board_data["columns"][current_column_index]["cards"] = [
                    card for card in self.board_data["columns"][current_column_index]["cards"]
                    if not (card["label"] == card_data_to_move["label"] and card.get("description", "") == card_data_to_move["description"])
                ]

                # Add to new column data
                self.board_data["columns"][target_column_index]["cards"].append(card_data_to_move)

                # Save the new state and rebuild the board
                save_board(self.board_data)
                self.rebuild_board()

                # Re-focus the moved card
                for column in self.query(Column):
                    for card in column.card_list_widget.children:
                        if card.label == card_data_to_move["label"] and card.description == card_data_to_move["description"]:
                            card.focus()
                            print(f"Focused card: {card.label}")
                            return

    def action_move_card_left(self) -> None:
        """Action to move the focused card to the left column."""
        self._move_card(-1)

    def action_move_card_right(self) -> None:
        """Action to move the focused card to the right column."""
        self._move_card(1)

    def action_edit_card(self) -> None:
        """Action to edit the currently focused card."""
        if isinstance(self.focused, Card):
            card_to_edit = self.focused

            def edit_card_callback(data):
                if data:
                    new_title, new_description, new_details = data
                    
                    # Update UI
                    card_to_edit.label = new_title
                    card_to_edit.description = new_description
                    card_to_edit.details = new_details
                    card_to_edit.refresh()

                    # Update data structure
                    for column_data in self.board_data["columns"]:
                        for card in column_data["cards"]:
                            if card["label"] == card_to_edit.label and card.get("description", "") == card_to_edit.description:
                                card["label"] = new_title
                                card["description"] = new_description
                                card["details"] = new_details
                                break
                        else:
                            continue
                        break

                    # Save the new state
                    save_board(self.board_data)

            self.push_screen(AddCardScreen(initial_title=card_to_edit.label, initial_description=card_to_edit.description, initial_details=card_to_edit.details), edit_card_callback)

    def action_view_card_details(self) -> None:
        """Action to view the details of the currently focused card."""
        if isinstance(self.focused, Card):
            self.push_screen(CardDetailScreen(self.focused))

    def action_delete_column(self) -> None:
        """Action to delete the currently focused column."""
        if isinstance(self.focused, Column):
            column_to_delete = self.focused
            
            all_columns = list(self.query(Column))
            current_column_index = all_columns.index(column_to_delete)

            # Remove from UI
            column_to_delete.remove()

            # Remove from data structure
            del self.board_data["columns"][current_column_index]
            
            # Save the new state
            save_board(self.board_data)

    def action_rename_column(self) -> None:
        """Action to rename the currently focused column."""
        if isinstance(self.focused, Column):
            column_to_rename = self.focused

            def rename_column_callback(new_title):
                if new_title:
                    # Update UI
                    column_to_rename.title = new_title
                    column_to_rename.query_one(".column-title").update(new_title)

                    # Update data structure
                    for column_data in self.board_data["columns"]:
                        if column_data["title"] == column_to_rename.title:
                            column_data["title"] = new_title
                            break

                    # Save the new state
                    save_board(self.board_data)

            self.push_screen(AddColumnScreen(initial_title=column_to_rename.title), rename_column_callback)

    def action_clear_board(self) -> None:
        """Action to clear all columns and cards from the board."""
        def clear_board_callback(confirmed: bool):
            if confirmed:
                self.board_data = get_default_data() # Reset to default empty board
                self.rebuild_board() # Clear UI and rebuild
                save_board(self.board_data) # Persist empty state

        self.push_screen(ConfirmScreen("Are you sure you want to clear the entire board?"), clear_board_callback)

    def action_focus_up(self) -> None:
        """Action to move focus to the card above."""
        if isinstance(self.focused, Card):
            current_card = self.focused
            current_card_list = current_card.parent
            cards_in_column = list(current_card_list.children)
            current_index = cards_in_column.index(current_card)
            if current_index > 0:
                cards_in_column[current_index - 1].focus()

    def action_focus_down(self) -> None:
        """Action to move focus to the card below."""
        if isinstance(self.focused, Card):
            current_card = self.focused
            current_card_list = current_card.parent
            cards_in_column = list(current_card_list.children)
            current_index = cards_in_column.index(current_card)
            if current_index < len(cards_in_column) - 1:
                cards_in_column[current_index + 1].focus()

    def action_focus_left(self) -> None:
        """Action to move focus to the first card in the left column."""
        if isinstance(self.focused, Card):
            current_card = self.focused
            current_card_list = current_card.parent
            current_column = current_card_list.parent
            
            all_columns = list(self.query(Column))
            current_column_index = all_columns.index(current_column)

            if current_column_index > 0:
                target_column = all_columns[current_column_index - 1]
                if target_column.card_list_widget.children:
                    target_column.card_list_widget.children[0].focus()
                else:
                    target_column.focus() # Focus the column if it's empty

    def action_focus_right(self) -> None:
        """Action to move focus to the first card in the right column."""
        if isinstance(self.focused, Card):
            current_card = self.focused
            current_card_list = current_card.parent
            current_column = current_card_list.parent

            all_columns = list(self.query(Column))
            current_column_index = all_columns.index(current_column)

            if current_column_index < len(all_columns) - 1:
                target_column = all_columns[target_column_index + 1]
                if target_column.card_list_widget.children:
                    target_column.card_list_widget.children[0].focus()
                else:
                    target_column.focus() # Focus the column if it's empty

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header(name="adp-planner")
        yield Horizontal(id="board-container")
        yield Footer() # Empty footer for now

if __name__ == "__main__":
    app = KanbanApp()
    app.run()