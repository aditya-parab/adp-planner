# Kanban TUI Project Overview

This document outlines the architecture and key components of the Kanban Terminal User Interface (TUI) application.

## Core Components

*   **`main.py`**: The application's entry point. It initializes and runs the `KanbanApp`.
*   **`board.py`**: Contains the main application logic and UI components, including `KanbanApp`, `Column`, `Card`, and `AddCardScreen`.
*   **`storage.py`**: Handles saving and loading the Kanban board data to/from a JSON file (`board_data.json`).
*   **`board.css`**: Defines the visual styles for the `textual` widgets used in the application.

## Data Persistence

The application automatically saves the current state of the Kanban board to `board_data.json` whenever changes are made (e.g., adding a card). When the application starts, it attempts to load the board from this file. If the file doesn't exist, a default board structure with "Input Queue", "In Progress", and "Done" columns is created.

## Design Considerations

### Flexible Column Layout and Scrolling

To ensure a robust and user-friendly experience, the Kanban board's layout is designed to adapt to a varying number of columns and cards. Initially, columns had a fixed percentage width, which caused overflow issues when more than three columns were present, leading to content being cut off.

To address this, the `Column` styling in `board.css` was modified to remove the explicit `width` property. This change allows the `textual` layout engine to dynamically size columns based on available space and the number of columns. Furthermore, the `Horizontal` container, which holds the columns, has been configured with `width: auto;` to ensure it expands horizontally to encompass all its child `Column` elements. The `align: center middle` property was removed from the `Horizontal` container to prevent it from interfering with the horizontal scrolling behavior. To further refine the horizontal scrolling and column presentation, the following CSS properties were adjusted:

*   **`white-space: nowrap;` (removed from `Horizontal`)**: This property was initially added to prevent columns from wrapping, but it was found to be an invalid CSS property in Textual. The desired behavior of preventing wrapping is now implicitly handled by Textual's layout engine when `min-width` is applied to columns and `overflow-x: scroll` is on the parent container.
*   **`min-width: 30w;` (changed from `width: 25w;`) to `Column`**: This property now sets a minimum width for each column, ensuring they have enough space initially to prevent them from appearing squashed. This allows columns to dynamically adjust their width to fit the screen when there are fewer columns, while still enabling horizontal scrolling when the total width of columns exceeds the terminal size.

This refined design ensures that:

*   **Dynamic Sizing:** Columns will adjust their width to fit the screen, making efficient use of space and ensuring all columns are always visible within the terminal window.

### Robust Column and Card Initialization

A key design principle for the UI components, particularly `Column` and `Card` widgets, is to ensure they are properly initialized and mounted within the `textual` application's lifecycle.

The `Column` widget is designed to receive its initial `cards_data` directly during its instantiation (`__init__` method). This data is then used within the `Column`'s `on_mount` method to dynamically create and attach `Card` widgets to its `VerticalScroll` container. This approach guarantees that the `VerticalScroll` widget is fully mounted and ready to accept child widgets before any `Card` instances are added, preventing potential `MountError` issues.

Furthermore, when new columns are added dynamically (e.g., via the `action_add_column` method), they are instantiated with an empty list (`[]`) for `cards_data`. This consistent initialization pattern ensures that new columns are always created in a valid state, ready to accept cards, and avoids `TypeError` issues related to missing arguments. This design promotes predictable behavior and simplifies the logic for managing UI components and their associated data.

### Royal Navy Blue Color Scheme

The application's visual theme has been updated to a "Royal Navy Blue" color scheme. This was achieved by defining a new set of CSS variables in `board.css` within the `:root` selector. These variables (`--primary`, `--secondary`, `--background`, `--surface`, `--text`, `--panel-darken-1`, `--accent`) are then used throughout the stylesheet to apply a consistent blue-centric palette. To ensure these variables are correctly parsed and applied across the application, the `:root` block has been strategically placed at the very top of `board.css`. This guarantees that the color definitions are available before any other CSS rules attempt to use them, preventing parsing errors and ensuring the intended visual theme is consistently rendered.

### PST Time Display

To enhance the utility of the application, the current time in Pacific Standard Time (PST) is now displayed in the footer. This feature is implemented in `board.py` by:

1.  Importing `datetime` and `ZoneInfo` for time and timezone handling.
2.  Adding a `Static` widget with the ID `time-display` to the `KanbanApp`'s `compose` method, specifically within the `Footer`.
3.  Implementing an `update_time` method that fetches the current UTC time, converts it to `America/Los_Angeles` (PST) timezone, and formats it.
4.  Calling `update_time` on `on_mount` and setting up a `set_interval` to refresh the time every second. This ensures the time display is always current and relevant to the user's context.

### Column and Card Interactivity & Detail View

To enhance user interaction and control, the Kanban board now supports column focusing, card dragging, and improved column management, along with a new card detail view.

*   **Column Focusability**: The `Column` class now includes `can_focus = True`, enabling users to select and interact directly with columns. This is crucial for actions like deleting or renaming columns, as these operations often target the currently focused column.
*   **Card Drag-and-Drop**: Cards (`Card` class) are now draggable, implemented by setting `can_drag = True`. The drag-and-drop functionality is managed within the `KanbanApp` through `on_mouse_down`, `on_mouse_move`, and `on_mouse_up` event handlers. When a card is dragged and dropped into a different column, the application:
    *   Updates the underlying `board_data` structure to reflect the card's new column.
    *   Rebuilds the entire board to ensure the UI accurately reflects the data state.
    *   Persists the changes to `board_data.json`.
    This allows for intuitive reorganization of cards across the board.
*   **Card Movement with Arrow Keys**: Cards can also be moved between columns using the left and right arrow keys. This functionality updates the `board_data` and rebuilds the board, similar to drag-and-drop, ensuring data consistency and UI accuracy.
*   **Delete Column Functionality**: The `action_delete_column` method now correctly identifies the focused column and removes it from both the UI and the `board_data`, ensuring persistence.
*   **Rename Column Functionality**: The `action_rename_column` method now correctly identifies the focused column and allows users to rename it via a dialog, updating both the UI and the `board_data`, ensuring persistence.
*   **Card Detail View**:
    *   **Extended Card Data**: Cards now include an additional `details` field to store more comprehensive information. This field is integrated into the card data structure and handled during saving and loading.
    *   **Enhanced Add/Edit Dialog**: The `AddCardScreen` now features a `TextArea` for entering multi-line details when adding or editing a card.
    *   **`CardDetailScreen`**: A new modal screen (`CardDetailScreen`) has been implemented to display the full title, description, and details of a selected card in a read-only format.
    *   **Triggers**: The `CardDetailScreen` can be accessed by:
        *   Pressing the `i` key when a card is focused.
        *   Double-clicking on a card with the mouse.

These enhancements significantly improve the usability and interactivity of the Kanban TUI application, providing a more fluid and efficient workflow for managing tasks and viewing detailed card information.


