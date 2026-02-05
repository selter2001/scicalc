# Architecture Patterns: Python Scientific Calculator with CustomTkinter

**Domain:** Desktop GUI Calculator Application
**Researched:** 2026-02-05
**Confidence:** HIGH (verified with official CustomTkinter docs and MVC pattern analysis)

## Executive Summary

Python GUI calculator apps with CustomTkinter should follow a **class-based Model-View-Controller (MVC) architecture** with clear separation between calculation logic, UI presentation, and control flow. The recommended structure uses multiple Python modules organized by responsibility, with `.grid()` geometry management for scalable layouts. Based on ecosystem analysis, successful implementations separate business logic (model), UI components (view), and event coordination (controller) into distinct modules, avoiding the common anti-pattern of monolithic single-file applications with global variables.

---

## Recommended Architecture

### High-Level Pattern: MVC with Modular Components

```
┌─────────────────────────────────────────────────────────────┐
│                        Main Application                      │
│                   (app.py or main.py)                        │
│              Initializes and coordinates MVC                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              ├───────────────┬──────────────┐
                              ▼               ▼              ▼
                    ┌─────────────┐  ┌──────────────┐  ┌─────────┐
                    │    MODEL    │  │     VIEW     │  │  CTRL   │
                    │  (logic/)   │  │    (ui/)     │  │(ctrl/)  │
                    │             │  │              │  │         │
                    │ Calculator  │  │ MainWindow   │  │Calculator│
                    │ Engine      │  │ ButtonPanel  │  │Controller│
                    │ History Mgr │  │ HistoryPanel │  │         │
                    │ Evaluator   │  │ DisplayField │  │         │
                    └─────────────┘  └──────────────┘  └─────────┘
                          │                 │                │
                          └─────────────────┴────────────────┘
                                      │
                              ┌───────▼────────┐
                              │  Data Storage  │
                              │ (history.json) │
                              └────────────────┘
```

---

## Component Boundaries

### 1. Model Layer (Business Logic)

| Component | Responsibility | Communicates With | File Location |
|-----------|---------------|-------------------|---------------|
| **CalculatorEngine** | Performs mathematical operations; evaluates expressions using Python's `eval()` or safer alternatives | Controller only | `logic/calculator.py` |
| **HistoryManager** | Stores, retrieves, and manages calculation history; handles JSON persistence | Controller only | `logic/history.py` |
| **Evaluator** | Safely evaluates mathematical expressions; handles error cases (division by zero, invalid syntax) | CalculatorEngine | `logic/evaluator.py` |
| **ScientificFunctions** | Provides scientific operations (sin, cos, tan, log, sqrt, etc.) via `math` module | CalculatorEngine | `logic/scientific.py` |

**Key Principles:**
- No UI dependencies (no `import customtkinter` in model layer)
- Pure Python functions and classes
- Returns results or raises exceptions - never updates UI directly
- Fully testable with unit tests

### 2. View Layer (User Interface)

| Component | Responsibility | Communicates With | File Location |
|-----------|---------------|-------------------|---------------|
| **MainWindow** | Root window inheriting from `customtkinter.CTk`; manages overall layout and theme | All UI components | `ui/main_window.py` |
| **DisplayField** | Shows current input and results; single `CTkEntry` or `CTkLabel` widget | Controller (receives updates) | `ui/display.py` |
| **ButtonPanel** | Grid of calculator buttons (numbers, operators, functions); mode-aware (basic/scientific) | Controller (emits clicks) | `ui/buttons.py` |
| **HistoryPanel** | Sidebar with `CTkScrollableFrame` showing calculation history; supports double-click recall | Controller (receives history, emits selections) | `ui/history.py` |
| **ModeToggle** | Switch/button to toggle between basic and scientific modes | Controller (emits mode changes) | `ui/mode_toggle.py` |

**Key Principles:**
- Inherits from `customtkinter.CTk` (main) or `customtkinter.CTkFrame` (components)
- Uses `.grid()` geometry manager (never `.place()`)
- Exposes public methods: `setDisplayText()`, `getDisplayText()`, `updateHistory()`, etc.
- Emits user actions via callback functions passed from controller
- No business logic (no mathematical calculations in UI code)

### 3. Controller Layer (Coordination)

| Component | Responsibility | Communicates With | File Location |
|-----------|---------------|-------------------|---------------|
| **CalculatorController** | Connects Model and View; handles button click events; orchestrates data flow | Model layer, View layer | `controller/calculator_controller.py` |
| **EventHandlers** | Maps user events to model operations; updates view with results | Controller | `controller/handlers.py` |

**Key Principles:**
- Receives Model and View as constructor parameters
- Implements signal-slot pattern (connect button callbacks to handler methods)
- Translates user actions → model operations → view updates
- Handles error states from model and displays them in view

### 4. Configuration & Constants

| Component | Responsibility | File Location |
|-----------|---------------|---------------|
| **AppConfig** | Window dimensions, button sizes, grid layout specs | `config/constants.py` |
| **ThemeConfig** | Dark theme colors, CustomTkinter theme selection ("dark-blue"), appearance mode ("dark") | `config/theme.py` |
| **LocaleConfig** | Polish UI text strings (button labels, error messages) | `config/locale.py` |

---

## Data Flow

### Primary Flow: User Performs Calculation

```
1. User clicks button "7"
   └─> View (ButtonPanel) calls controller.on_button_click("7")

2. Controller receives event
   └─> Controller.on_button_click("7")
       └─> Updates internal state (current_input += "7")
       └─> Calls View.setDisplayText(current_input)

3. User clicks "+" button
   └─> View calls controller.on_button_click("+")
   └─> Controller appends "+" to current_input
   └─> View updates display

4. User clicks "3" then "=" button
   └─> View calls controller.on_button_click("=")
   └─> Controller calls Model.CalculatorEngine.evaluate("7+3")
   └─> Model returns result: 10.0 or raises error
   └─> Controller checks result:
       ├─> SUCCESS: Calls View.setDisplayText("10.0")
       │           Calls Model.HistoryManager.save("7+3", 10.0)
       │           Calls View.HistoryPanel.updateHistory([...])
       └─> ERROR:   Calls View.setDisplayText("ERROR: Division by zero")
```

### Secondary Flow: Mode Toggle (Basic ↔ Scientific)

```
1. User clicks mode toggle button
   └─> View (ModeToggle) calls controller.on_mode_toggle("scientific")

2. Controller receives mode change
   └─> Controller updates internal state (current_mode = "scientific")
   └─> Controller calls View.ButtonPanel.show_scientific_buttons()
   └─> View re-renders button grid with scientific functions (sin, cos, log, etc.)
```

### Tertiary Flow: History Recall

```
1. User double-clicks history item "7+3 = 10.0"
   └─> View (HistoryPanel) calls controller.on_history_select("7+3")

2. Controller receives history selection
   └─> Controller calls View.setDisplayText("7+3")
   └─> User can now modify or re-evaluate
```

---

## File/Module Structure Recommendation

```
scientific_calculator/
├── main.py                          # Entry point: initializes app, runs main loop
├── requirements.txt                 # Dependencies: customtkinter
├── README.md                        # Project documentation
│
├── config/                          # Configuration and constants
│   ├── __init__.py
│   ├── constants.py                 # Window size, button dimensions, grid specs
│   ├── theme.py                     # Dark theme configuration
│   └── locale.py                    # Polish UI strings
│
├── logic/                           # Model layer (business logic)
│   ├── __init__.py
│   ├── calculator.py                # CalculatorEngine class
│   ├── evaluator.py                 # Safe expression evaluation
│   ├── history.py                   # HistoryManager class (JSON I/O)
│   └── scientific.py                # ScientificFunctions (math module wrapper)
│
├── ui/                              # View layer (CustomTkinter UI)
│   ├── __init__.py
│   ├── main_window.py               # MainWindow(CTk) - root window
│   ├── display.py                   # DisplayField(CTkFrame) - result display
│   ├── buttons.py                   # ButtonPanel(CTkFrame) - number/operator buttons
│   ├── history.py                   # HistoryPanel(CTkScrollableFrame) - sidebar
│   └── mode_toggle.py               # ModeToggle(CTkFrame) - basic/scientific switch
│
├── controller/                      # Controller layer (MVC coordination)
│   ├── __init__.py
│   ├── calculator_controller.py     # CalculatorController class
│   └── handlers.py                  # Event handler helper functions
│
├── data/                            # Runtime data storage
│   └── history.json                 # Persistent calculation history
│
└── tests/                           # Unit tests (pytest)
    ├── __init__.py
    ├── test_calculator.py           # Tests for CalculatorEngine
    ├── test_evaluator.py            # Tests for Evaluator (edge cases)
    ├── test_history.py              # Tests for HistoryManager (JSON I/O)
    └── test_scientific.py           # Tests for ScientificFunctions
```

### Key Files Explained

**`main.py`** (Entry Point)
```python
import customtkinter as ctk
from ui.main_window import MainWindow
from logic.calculator import CalculatorEngine
from logic.history import HistoryManager
from controller.calculator_controller import CalculatorController
from config.theme import setup_theme

def main():
    setup_theme()  # Set dark mode and theme

    # Initialize MVC components
    model = CalculatorEngine()
    history = HistoryManager()
    view = MainWindow()
    controller = CalculatorController(model, history, view)

    view.mainloop()

if __name__ == "__main__":
    main()
```

**`config/theme.py`** (Dark Theme Setup)
```python
import customtkinter as ctk

def setup_theme():
    ctk.set_appearance_mode("dark")  # Force dark mode
    ctk.set_default_color_theme("dark-blue")  # Use dark-blue theme
```

**`logic/calculator.py`** (Model - No UI Dependencies)
```python
from logic.evaluator import SafeEvaluator
from logic.scientific import ScientificFunctions

class CalculatorEngine:
    def __init__(self):
        self.evaluator = SafeEvaluator()
        self.scientific = ScientificFunctions()

    def evaluate(self, expression: str) -> float:
        """Evaluate math expression. Raises ValueError on error."""
        return self.evaluator.eval(expression)

    def sin(self, value: float) -> float:
        return self.scientific.sin(value)
    # ... other methods
```

**`ui/main_window.py`** (View - Inherits from CTk)
```python
import customtkinter as ctk
from ui.display import DisplayField
from ui.buttons import ButtonPanel
from ui.history import HistoryPanel

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Kalkulator Naukowy")
        self.geometry("800x600")

        # Grid layout: main area (left) + history (right)
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)

        self.display = DisplayField(self)
        self.display.grid(row=0, column=0, sticky="ew")

        self.buttons = ButtonPanel(self)
        self.buttons.grid(row=1, column=0, sticky="nsew")

        self.history_panel = HistoryPanel(self)
        self.history_panel.grid(row=0, column=1, rowspan=2, sticky="ns")
```

**`controller/calculator_controller.py`** (Controller - MVC Glue)
```python
class CalculatorController:
    def __init__(self, model, history, view):
        self.model = model
        self.history = history
        self.view = view
        self._current_input = ""

        # Connect view events to controller handlers
        self.view.buttons.set_button_callback(self.on_button_click)
        self.view.history_panel.set_select_callback(self.on_history_select)

    def on_button_click(self, button_value: str):
        if button_value == "=":
            self._evaluate()
        elif button_value == "C":
            self._clear()
        else:
            self._append_to_input(button_value)

    def _evaluate(self):
        try:
            result = self.model.evaluate(self._current_input)
            self.view.display.set_text(str(result))
            self.history.save(self._current_input, result)
            self._refresh_history()
        except ValueError as e:
            self.view.display.set_text(f"BŁĄD: {e}")

    # ... other methods
```

---

## Suggested Build Order (Dependencies)

Build components in this order to minimize dependency issues and enable incremental testing:

### Phase 1: Foundation (Core Infrastructure)
**Priority: Build first - everything depends on these**

1. **Configuration modules** (`config/`)
   - `constants.py` - Define window size, button dimensions, colors
   - `theme.py` - Set up dark theme with CustomTkinter
   - `locale.py` - Polish UI strings

   **Why first:** No dependencies; needed by all other components

2. **Basic Model - Evaluator** (`logic/evaluator.py`)
   - Safe expression evaluation (basic arithmetic only)
   - Error handling for division by zero, invalid syntax

   **Why second:** Pure Python, no dependencies; enables testing calculation logic immediately

### Phase 2: Core Calculation Logic (Model Layer)
**Priority: Build second - enables end-to-end basic calculator**

3. **CalculatorEngine** (`logic/calculator.py`)
   - Basic operations (+, -, *, /)
   - Uses Evaluator from Phase 1

   **Blockers:** Requires `logic/evaluator.py`

4. **Basic Display** (`ui/display.py`)
   - Simple CTkEntry or CTkLabel showing current input/result
   - Methods: `set_text()`, `get_text()`, `clear()`

   **Blockers:** Requires `config/theme.py`

5. **Basic ButtonPanel** (`ui/buttons.py`)
   - Grid of number buttons (0-9) and basic operators (+, -, *, /, =, C)
   - Uses `.grid()` geometry manager

   **Blockers:** Requires `config/constants.py` for button sizes

6. **Minimal MainWindow** (`ui/main_window.py`)
   - CTk window with Display + ButtonPanel only (no history yet)
   - Grid layout with single column

   **Blockers:** Requires `ui/display.py`, `ui/buttons.py`

7. **Basic Controller** (`controller/calculator_controller.py`)
   - Connects button clicks → model evaluation → display update
   - No history, no scientific functions yet

   **Blockers:** Requires Model (calculator.py), View (main_window.py)

8. **Entry Point** (`main.py`)
   - Initialize MVC components
   - Run main loop

   **Blockers:** Requires all above components

**Deliverable:** Working basic calculator (4 operations, display, error handling)

### Phase 3: History Feature
**Priority: Build third - enhances UX without affecting core calculation**

9. **HistoryManager** (`logic/history.py`)
   - Save/load calculations to JSON
   - Methods: `save(expression, result)`, `load_all()`, `clear()`

   **Blockers:** None (independent)

10. **HistoryPanel** (`ui/history.py`)
    - CTkScrollableFrame with list of past calculations
    - Double-click to recall expression

    **Blockers:** Requires `config/theme.py`

11. **Integrate History into Controller**
    - Update `calculator_controller.py` to save results
    - Handle history recall events

    **Blockers:** Requires HistoryManager, HistoryPanel

12. **Update MainWindow for History**
    - Add HistoryPanel to grid (right column)
    - Adjust grid weights (3:1 ratio main:history)

    **Blockers:** Requires HistoryPanel

**Deliverable:** Calculator with persistent history sidebar

### Phase 4: Scientific Mode
**Priority: Build fourth - major feature expansion**

13. **ScientificFunctions** (`logic/scientific.py`)
    - Wrapper around Python `math` module
    - Functions: sin, cos, tan, log, ln, sqrt, pow, factorial, etc.

    **Blockers:** None (independent)

14. **Extend CalculatorEngine**
    - Integrate ScientificFunctions
    - Methods for each scientific operation

    **Blockers:** Requires ScientificFunctions

15. **Scientific ButtonPanel Extension**
    - Add method `show_scientific_buttons()` to ButtonPanel
    - Expand grid with scientific function buttons (sin, cos, log, etc.)
    - Hide/show based on mode

    **Blockers:** Requires config/constants.py update

16. **ModeToggle Component** (`ui/mode_toggle.py`)
    - CTkSwitch or CTkSegmentedButton ("Podstawowy" / "Naukowy")
    - Emits mode change events

    **Blockers:** Requires config/locale.py

17. **Controller Mode Management**
    - Add mode state tracking
    - Handle mode toggle events
    - Show/hide scientific buttons via ButtonPanel

    **Blockers:** Requires ModeToggle, extended ButtonPanel

18. **MainWindow Mode Integration**
    - Add ModeToggle to layout (top or sidebar)
    - Adjust window size for scientific mode

    **Blockers:** Requires ModeToggle

**Deliverable:** Dual-mode calculator (basic/scientific) with toggle

### Phase 5: Polish & Testing
**Priority: Build last - quality assurance**

19. **Unit Tests** (`tests/`)
    - `test_calculator.py` - Test all operations
    - `test_evaluator.py` - Test edge cases (division by zero, syntax errors)
    - `test_history.py` - Test JSON persistence
    - `test_scientific.py` - Test scientific functions

    **Blockers:** Requires all model components

20. **UI Refinements**
    - Polish translations in `config/locale.py`
    - Fine-tune dark theme colors
    - Responsive window resizing

    **Blockers:** Requires complete UI

**Deliverable:** Tested, polished, production-ready calculator

---

## Dependency Graph

```
Constants/Theme/Locale (Phase 1)
        │
        ├─────────────────────────────┬──────────────────┐
        ▼                             ▼                  ▼
   Evaluator (Phase 2)          Display (Phase 2)   ButtonPanel (Phase 2)
        │                             │                  │
        ▼                             └──────┬───────────┘
CalculatorEngine (Phase 2)                   │
        │                                    ▼
        │                            MainWindow (Phase 2)
        │                                    │
        └────────────────┬───────────────────┘
                         ▼
              CalculatorController (Phase 2)
                         │
                         ▼
                    main.py (Phase 2)
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
  HistoryManager    HistoryPanel   ScientificFunctions
   (Phase 3)        (Phase 3)        (Phase 4)
        │                │                │
        └────────┬───────┴────────────────┘
                 ▼
          Full Integration
           (Phase 4-5)
```

---

## Patterns to Follow

### Pattern 1: Class-Based Component Inheritance
**What:** All UI components inherit from `customtkinter.CTk` (main window) or `customtkinter.CTkFrame` (sub-components)

**When:** Every UI module

**Example:**
```python
import customtkinter as ctk

class ButtonPanel(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_buttons()

    def _create_buttons(self):
        # Use .grid() to arrange buttons
        pass
```

**Benefits:**
- Clear, readable code
- Expandable architecture
- Avoids global variables

### Pattern 2: Grid-Based Layout (Never Place)
**What:** Use `.grid()` geometry manager for all layouts. Avoid `.place()` entirely.

**When:** All widget positioning

**Example:**
```python
# Good: Grid layout
self.display.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
self.buttons.grid(row=1, column=0, sticky="nsew")

# Bad: Absolute positioning
self.display.place(x=10, y=10, width=300, height=50)  # NEVER DO THIS
```

**Benefits:**
- Automatic alignment and padding
- Responsive to window resizing
- Easy to insert new widgets without recalculating positions

### Pattern 3: Public Interface Methods for Views
**What:** Views expose public methods for controller to update state. Never let controller access private attributes.

**When:** All View components

**Example:**
```python
# View (display.py)
class DisplayField(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self._entry = ctk.CTkEntry(self, font=("Arial", 24))
        self._entry.grid(row=0, column=0, sticky="ew")

    # Public interface
    def set_text(self, text: str):
        self._entry.delete(0, tk.END)
        self._entry.insert(0, text)

    def get_text(self) -> str:
        return self._entry.get()

# Controller (calculator_controller.py)
def _evaluate(self):
    expression = self.view.display.get_text()  # Use public method
    result = self.model.evaluate(expression)
    self.view.display.set_text(str(result))   # Use public method
```

**Benefits:**
- Encapsulation (controller doesn't know about `_entry` widget)
- Easy to change UI implementation without affecting controller

### Pattern 4: Callback Functions for Events
**What:** Views accept callback functions from controller. When user events occur, view calls the callback.

**When:** All user interactions (button clicks, mode toggles, history selections)

**Example:**
```python
# View (buttons.py)
class ButtonPanel(ctk.CTkFrame):
    def set_button_callback(self, callback_fn):
        self._callback = callback_fn

    def _on_button_click(self, value):
        if self._callback:
            self._callback(value)  # Notify controller

# Controller
controller = CalculatorController(model, history, view)
view.buttons.set_button_callback(controller.on_button_click)
```

**Benefits:**
- Loose coupling (view doesn't know about controller implementation)
- Follows observer pattern

### Pattern 5: Tuple Colors for Dark/Light Mode
**What:** Use tuple colors `(light_color, dark_color)` for widgets that might support theme switching in the future.

**When:** Custom widget colors

**Example:**
```python
# config/theme.py
BUTTON_COLOR = ("#3B8ED0", "#1F6AA5")  # (light mode, dark mode)
ERROR_COLOR = ("#FF5555", "#FF0000")

# ui/buttons.py
button = ctk.CTkButton(
    self,
    text="=",
    fg_color=BUTTON_COLOR,
    command=lambda: self._on_button_click("=")
)
```

**Benefits:**
- Future-proof if light mode is added later
- Consistent with CustomTkinter conventions

### Pattern 6: Separate Configuration from Code
**What:** All magic numbers (window size, button dimensions, grid specs) in `config/constants.py`

**When:** Any hardcoded value

**Example:**
```python
# config/constants.py
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BUTTON_WIDTH = 80
BUTTON_HEIGHT = 60
HISTORY_WIDTH = 200

# ui/main_window.py
from config.constants import WINDOW_WIDTH, WINDOW_HEIGHT

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
```

**Benefits:**
- Single source of truth
- Easy to adjust layout without hunting through code

---

## Anti-Patterns to Avoid

### Anti-Pattern 1: Monolithic Single-File Application
**What:** Writing entire calculator in one `main.py` file with global variables

**Example (BAD):**
```python
# main.py (1000+ lines)
import customtkinter as ctk

current_input = ""  # Global variable
history_list = []   # Global variable

def button_click(value):
    global current_input
    current_input += value
    display.configure(text=current_input)

def evaluate():
    global current_input, history_list
    result = eval(current_input)  # Unsafe!
    history_list.append(result)
    current_input = str(result)

app = ctk.CTk()
display = ctk.CTkLabel(app, text="0")
# ... 500 more lines of UI code mixed with logic ...
app.mainloop()
```

**Why bad:**
- Impossible to test individual components
- No separation of concerns
- Global state causes bugs
- Cannot reuse components
- Violates "suitable for public GitHub" requirement

**Instead:** Use MVC structure with separate modules as shown in recommended architecture

### Anti-Pattern 2: Using `.place()` Geometry Manager
**What:** Absolute positioning with `.place(x, y, width, height)`

**Why bad:**
- Blocks app extensibility (inserting new widget requires repositioning everything)
- Inconsistent padding
- Not responsive to window resizing
- Official CustomTkinter docs explicitly warn against this

**Instead:** Use `.grid()` for scalable layouts

### Anti-Pattern 3: UI Logic in Model Layer
**What:** Model classes importing `customtkinter` or updating widgets directly

**Example (BAD):**
```python
# logic/calculator.py (BAD!)
import customtkinter as ctk

class CalculatorEngine:
    def __init__(self, display_widget):
        self.display = display_widget  # MODEL SHOULD NOT KNOW ABOUT VIEW!

    def add(self, a, b):
        result = a + b
        self.display.configure(text=str(result))  # MODEL UPDATING VIEW DIRECTLY!
        return result
```

**Why bad:**
- Cannot test model without UI
- Violates separation of concerns
- Model becomes coupled to CustomTkinter (can't switch to PyQt5 later)

**Instead:** Model returns values or raises exceptions; Controller updates View

### Anti-Pattern 4: Using `eval()` Without Validation
**What:** Directly calling Python's `eval()` on user input

**Example (BAD):**
```python
def evaluate(expression: str):
    return eval(expression)  # SECURITY RISK!

# User could input: __import__('os').system('rm -rf /')
```

**Why bad:**
- Major security vulnerability (arbitrary code execution)
- Can crash app with invalid syntax
- No control over allowed operations

**Instead:** Use `ast.literal_eval()` or a safe expression parser with whitelisted operations

### Anti-Pattern 5: Storing Calculations in Memory Only
**What:** Keeping history in Python list without persistence

**Why bad:**
- History lost on app restart
- No way to analyze past calculations
- Poor user experience

**Instead:** Use JSON file (`data/history.json`) with `HistoryManager` class

### Anti-Pattern 6: Hardcoding UI Strings in Polish Throughout Code
**What:** Embedding Polish text directly in UI component files

**Example (BAD):**
```python
# ui/buttons.py
button = ctk.CTkButton(self, text="Wyczyść")  # Hardcoded Polish
```

**Why bad:**
- Difficult to change wording later
- Cannot internationalize (add English support)
- Violates DRY principle

**Instead:** Centralize all UI strings in `config/locale.py`:
```python
# config/locale.py
BUTTON_CLEAR = "Wyczyść"
BUTTON_EQUALS = "="
ERROR_DIVISION_BY_ZERO = "Błąd: Dzielenie przez zero"

# ui/buttons.py
from config.locale import BUTTON_CLEAR
button = ctk.CTkButton(self, text=BUTTON_CLEAR)
```

---

## Build Order Implications

### Critical Path: Model → View → Controller
You **must** build in this order:
1. Model components (no dependencies)
2. View components (depend on config, not model)
3. Controller (depends on both model and view)

**Rationale:** Controller is the glue between model and view. Building it first would require mocking both, wasting time.

### Incremental Deliverables
After each phase, you have a **working application**:
- **Phase 2:** Basic 4-function calculator (usable product)
- **Phase 3:** Calculator with persistent history (enhanced UX)
- **Phase 4:** Full scientific calculator (complete feature set)
- **Phase 5:** Tested, polished production build

**Rationale:** Incremental approach reduces risk. If you run out of time, you still have a working basic calculator from Phase 2.

### Testing as You Go
Write unit tests **immediately after** completing each model component:
- Finish `logic/evaluator.py` → Write `tests/test_evaluator.py`
- Finish `logic/calculator.py` → Write `tests/test_calculator.py`

**Rationale:** Easier to test fresh code while logic is in your head. Prevents "big bang" testing phase at the end where everything breaks at once.

### History as Optional Enhancement
HistoryManager is **fully independent**. You can skip Phase 3 entirely and jump to Phase 4 (scientific mode) if needed.

**Rationale:** History is a UX enhancement but not core functionality. Flexible build order allows adapting to timeline constraints.

### UI Refinement Happens Last
Polish UI (colors, spacing, translations) in **Phase 5 only**.

**Rationale:** Premature optimization. Get functionality working first, then make it pretty. Avoids wasting time tweaking UI for features that might change.

---

## Scalability Considerations

This architecture is designed for a **single-user desktop application**. No scalability concerns for cloud deployment or multi-user scenarios.

**Performance Notes:**
- JSON history file: Will slow down after ~10,000 entries. Consider SQLite if history grows beyond 5,000 calculations.
- `.grid()` layout: Scales well to 50+ buttons (scientific mode). No performance issues expected.
- `eval()` alternative: Use `ast` module or pyparsing for safe evaluation; slightly slower but negligible for user-paced input.

---

## Sources

### HIGH Confidence (Official Documentation & Verified Patterns)

**CustomTkinter Architecture:**
- [App structure and layout · TomSchimansky/CustomTkinter Wiki](https://github.com/TomSchimansky/CustomTkinter/wiki/App-structure-and-layout) - Official wiki on class-based structure and geometry managers
- [Color and Themes | CustomTkinter](https://customtkinter.tomschimansky.com/documentation/color/) - Official documentation on dark mode and theme configuration
- [Appearance Mode | CustomTkinter](https://customtkinter.tomschimansky.com/documentation/appearancemode/) - Official documentation on appearance mode settings

**MVC Pattern for Python GUI:**
- [Python and PyQt: Building a GUI Desktop Calculator – Real Python](https://realpython.com/python-pyqt-gui-calculator/) - Comprehensive MVC architecture tutorial (verified with PyQt, applicable to CustomTkinter)
- [An Example of Model View Controller Design Pattern with Tkinter Python](https://sukhbinder.wordpress.com/2014/12/25/an-example-of-model-view-controller-design-pattern-with-tkinter-python/) - Tkinter MVC pattern (direct ancestor of CustomTkinter)

**Python Project Structure:**
- [Structuring Your Project — The Hitchhiker's Guide to Python](https://docs.python-guide.org/writing/structure/) - Authoritative guide on Python module organization
- [Python Application Layouts: A Reference – Real Python](https://realpython.com/python-application-layouts/) - Best practices for file structure

### MEDIUM Confidence (Community Best Practices, Verified Examples)

**CustomTkinter Best Practices:**
- [Tkinter Best Practices: Optimizing Performance and Code Structure | by Tom | TomTalksPython | Medium](https://medium.com/tomtalkspython/tkinter-best-practices-optimizing-performance-and-code-structure-c49d1919fbb4) - Performance and code organization recommendations

**Calculator Implementation Examples:**
- [How to Make a Calculator with Tkinter in Python - The Python Code](https://thepythoncode.com/article/make-a-calculator-app-using-tkinter-in-python) - History panel implementation with JSON persistence
- [How to Make A Calculator App in Python CustomTkinter](https://python-hub.com/calculator-app-in-python-customtkinter/) - CustomTkinter calculator example

**Modular Design:**
- [How do I split up Python Tkinter code in multiple files?](https://www.tutorialspoint.com/how-do-i-split-up-python-tkinter-code-in-multiple-files) - Multi-file Tkinter structure
- [Python GUI broken into multiple files | Robotic Controls](https://robotic-controls.com/learn/python-guis/python-gui-broken-multiple-files) - Separation of concerns for GUI applications

**Scientific Calculator Features:**
- [Scientific GUI Calculator using Tkinter in Python - GeeksforGeeks](https://www.geeksforgeeks.org/python/scientific-gui-calculator-using-tkinter-in-python/) - Scientific function implementation patterns
- [GitHub - kostasthanos/Tkinter-Calculator: Scientific Calculator using Python's library Tkinter](https://github.com/kostasthanos/Tkinter-Calculator) - Mode toggle example

**Testing:**
- [How to Create Unit Tests in Python with pytest](https://oneuptime.com/blog/post/2026-01-25-unit-tests-pytest-python/view) - pytest for calculator logic testing
- [Python's unittest: Writing Unit Tests for Your Code – Real Python](https://realpython.com/python-unittest/) - unittest framework for component testing

### LOW Confidence (General Context, Not Directly Verified)

- Various GitHub repositories for calculator projects (code examples, not authoritative architecture guidance)
- Medium articles on MVC pattern (general concepts, not Python-specific verification)

---

## Confidence Assessment

| Area | Level | Reason |
|------|-------|--------|
| **MVC Architecture** | HIGH | Verified with Real Python tutorial and official Tkinter MVC examples; pattern is well-established for GUI calculators |
| **CustomTkinter Structure** | HIGH | Official wiki explicitly recommends class-based architecture and `.grid()` usage; direct quotes from maintainer |
| **File Organization** | HIGH | Hitchhiker's Guide to Python and Real Python are authoritative sources; widely adopted conventions |
| **Dark Theme Implementation** | HIGH | Official CustomTkinter documentation on color and appearance mode; straightforward API |
| **History Panel** | MEDIUM | Verified implementation example exists (thepythoncode.com) but not officially documented pattern |
| **Mode Toggle** | MEDIUM | Scientific calculator examples show approach but no official CustomTkinter pattern for multi-mode UIs |
| **Build Order** | MEDIUM | Derived from dependency analysis and incremental development best practices, not empirically verified |

---

## Notes for Roadmap Creation

### Phase Structure Recommendation
Based on component dependencies and incremental delivery, suggest **4-5 phases**:
1. **Setup & Basic Calculator** (Phases 1-2 combined)
2. **History Feature** (Phase 3)
3. **Scientific Mode** (Phase 4)
4. **Testing & Polish** (Phase 5)

### Likely Deep Research Needed
- **Phase 4 (Scientific Mode):** May need research into safe math expression parsing (alternatives to `eval()`)
- **Phase 5 (Testing):** May need research into GUI testing approaches for CustomTkinter (less mature than PyQt5)

### Standard Patterns (Low Research Risk)
- Phases 1-2 (Basic Calculator): Well-trodden path, unlikely to encounter surprises
- Phase 3 (History): JSON persistence is straightforward Python

### Critical Dependencies
- **CustomTkinter library:** Ensure compatible version (check PyPI for latest stable)
- **Python 3.8+:** CustomTkinter requires modern Python
- No external API dependencies or complex state management needed

---

## Open Questions

1. **Safe Expression Evaluation:** Should we use `ast.literal_eval()`, pyparsing, or a custom tokenizer for mathematical expressions? (Research during Phase 4)

2. **GUI Testing:** What's the best approach for automated testing of CustomTkinter UIs? pytest-qt doesn't support CustomTkinter. (Research during Phase 5)

3. **Degree/Radian Toggle:** Should angle mode be a global setting or per-function? (Design decision during Phase 4)

4. **History Export:** Should users be able to export history to CSV/PDF? (Feature scope decision - possibly post-MVP)

5. **Keyboard Shortcuts:** Should we support keyboard input (number keys, operators) in addition to button clicks? (Enhancement - possibly Phase 5)
