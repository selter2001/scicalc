# Phase 3: Advanced Modes & History - Research

**Researched:** 2026-02-05
**Domain:** CustomTkinter GUI enhancements (keyboard bindings, clipboard operations, scrollable history UI, angle mode display)
**Confidence:** MEDIUM

## Summary

Phase 3 adds three major feature areas to the existing MVC calculator: (1) **Angle mode UI/UX** - displaying current DEG/RAD mode with toggle button, (2) **History panel** - scrollable list of past calculations with click-to-recall, and (3) **Keyboard shortcuts** - full keyboard navigation including Ctrl+C/V clipboard operations.

The existing codebase already has angle mode logic fully implemented in SafeEvaluator (degrees/radians/gradians conversion with `set_angle_mode()`), so this phase focuses on **exposing that functionality to users** through UI and integrating keyboard event handling into the CustomTkinter window.

**Primary recommendation:** Use CustomTkinter's CTkScrollableFrame for history panel, bind keyboard events at window level using `<Return>`, `<Escape>`, `<BackSpace>` key names, and use tkinter's built-in `clipboard_get()` and `clipboard_append()` methods for copy/paste. Store history as a list of dict entries with expression and result.

## Standard Stack

The established libraries/tools for this domain:

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| CustomTkinter | Latest (5.2+) | GUI framework | Already in use, provides CTkScrollableFrame for history |
| tkinter (stdlib) | Python 3.x | Event binding & clipboard | Built-in, no dependencies, standard for desktop Python apps |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| N/A | - | - | All functionality available in existing stack |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| CTkScrollableFrame | Custom Canvas+Scrollbar | More complexity, worse maintainability, no benefit |
| tkinter clipboard | pyperclip | External dependency, no significant advantage for simple text |
| Window-level bindings | Widget-level bindings | Harder to manage focus, more code duplication |

**Installation:**
```bash
# No new dependencies needed - all features available in existing stack
# CustomTkinter already installed from Phase 2
```

## Architecture Patterns

### Recommended Project Structure
```
src/calculator/
├── ui/
│   ├── calculator_window.py    # Add keyboard bindings here
│   ├── display.py              # Add angle mode indicator
│   ├── button_panel.py         # Existing
│   └── history_panel.py        # NEW: Scrollable history widget
├── controller/
│   └── calculator_controller.py # Add history state, keyboard handlers, angle mode control
└── logic/
    └── calculator.py           # Angle mode passthrough already exists
```

### Pattern 1: Window-Level Keyboard Binding
**What:** Bind keyboard events to the root window (CTk instance) rather than individual widgets
**When to use:** For global shortcuts that should work regardless of focus (numbers, operators, Enter, Escape, Backspace)
**Example:**
```python
# In CalculatorWindow.__init__()
# Source: Verified from multiple tkinter event binding sources
self.bind("<Return>", lambda event: self._handle_enter())
self.bind("<Escape>", lambda event: self._handle_escape())
self.bind("<BackSpace>", lambda event: self._handle_backspace())

# For Ctrl shortcuts, use Control modifier
self.bind("<Control-c>", lambda event: self._handle_copy())
self.bind("<Control-v>", lambda event: self._handle_paste())

# For number and operator keys, bind individual characters
for char in "0123456789+-*/().":
    self.bind(char, lambda event, c=char: self._handle_char(c))
```

**Key names reference:**
- Enter key: `<Return>` (not `<Enter>`)
- Escape key: `<Escape>`
- Backspace: `<BackSpace>` (capital S)
- Control modifier: `<Control-key>` or `<Control-Key-key>`

### Pattern 2: CTkScrollableFrame for History
**What:** Use CustomTkinter's built-in scrollable frame widget for displaying calculation history
**When to use:** When you need a scrollable list of widgets (history entries)
**Example:**
```python
# Source: CustomTkinter official documentation
import customtkinter as ctk

class HistoryPanel(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.history_entries = []

    def add_entry(self, expression, result):
        """Add a calculation to history."""
        # Create clickable label for the entry
        entry_text = f"{expression} = {result}"
        label = ctk.CTkLabel(self, text=entry_text, cursor="hand2")
        label.bind("<Button-1>", lambda e: self.on_entry_click(result))
        label.pack(pady=2, fill="x")
        self.history_entries.append(label)

    def clear_history(self):
        """Remove all history entries."""
        for label in self.history_entries:
            label.destroy()
        self.history_entries.clear()
```

**CTkScrollableFrame key parameters:**
- `width`, `height`: Inner frame dimensions
- `orientation`: "vertical" (default) or "horizontal"
- `corner_radius`: Border curvature (0 for seamless)
- `fg_color`: Background color ("transparent" to inherit parent)

### Pattern 3: Clipboard Operations
**What:** Use tkinter's built-in clipboard methods available on any widget
**When to use:** For copy (Ctrl+C) and paste (Ctrl+V) functionality
**Example:**
```python
# Source: Tkinter universal widget methods documentation
def copy_to_clipboard(self, text):
    """Copy text to system clipboard."""
    self.clipboard_clear()
    self.clipboard_append(text)
    # Note: On X11 (Linux), clipboard may be cleared when app exits
    # unless a clipboard manager (like Klipper) is running

def paste_from_clipboard(self):
    """Get text from system clipboard."""
    try:
        return self.clipboard_get()
    except tk.TclError:
        # Clipboard is empty or contains non-text data
        return None
```

### Pattern 4: History Data Structure
**What:** Store history as a list of dicts with expression and result
**When to use:** When you need to track calculation history for display and recall
**Example:**
```python
# In CalculatorController
class CalculatorController:
    def __init__(self, ...):
        self.history = []  # List of {"expression": str, "result": str}
        self.max_history = 100  # Limit to prevent unbounded growth

    def _calculate(self):
        # ... existing calculation logic ...
        if result["success"]:
            # Add to history
            self.history.append({
                "expression": self.expression,
                "result": result["result"]
            })
            # Limit history size
            if len(self.history) > self.max_history:
                self.history.pop(0)
            # Update history panel
            self.view.add_history_entry(self.expression, result["result"])
```

### Pattern 5: Angle Mode Toggle and Display
**What:** Add UI element (segmented button or label) to show current angle mode and allow toggling
**When to use:** When trigonometric functions need angle mode awareness
**Example:**
```python
# In DisplayPanel or CalculatorWindow
self.angle_mode_btn = ctk.CTkSegmentedButton(
    self,
    values=["DEG", "RAD"],
    command=self._on_angle_mode_change
)
self.angle_mode_btn.set("DEG")  # Default

def _on_angle_mode_change(self, value):
    """Update engine angle mode when user toggles."""
    mode = "degrees" if value == "DEG" else "radians"
    if self.mode_callback:
        self.mode_callback(mode)
```

**Note:** Existing codebase uses constants `ANGLE_MODE_DEGREES`, `ANGLE_MODE_RADIANS`, `ANGLE_MODE_GRADIANS` - use these for consistency.

### Anti-Patterns to Avoid
- **Don't bind keyboard events to individual buttons:** Leads to focus management nightmares and duplicate code
- **Don't implement custom scrolling:** CTkScrollableFrame handles all scrolling logic correctly
- **Don't store clipboard references:** Clipboard is global system resource, always read fresh on paste
- **Don't bind Enter key as `<Enter>`:** Correct key name is `<Return>` in tkinter
- **Don't use widget-specific focus for global shortcuts:** Keyboard events require focus - bind at window level for global access

## Don't Hand-Roll

Problems that look simple but have existing solutions:

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Scrollable list widget | Custom Canvas + Scrollbar + scroll handling | CTkScrollableFrame | Handles mouse wheel, keyboard nav, dynamic sizing, and platform differences |
| Clipboard access | OS-specific clipboard libraries | tkinter clipboard_get/append/clear | Cross-platform, built-in, no dependencies |
| Keyboard event parsing | Custom key code lookup tables | tkinter bind with key name strings | Standardized, handles modifiers, cross-platform |
| History persistence | Custom file I/O or database | In-memory list (for now) | Requirements don't specify persistence, YAGNI principle |
| Focus management for shortcuts | Manual focus tracking | Window-level bindings | Events propagate from focused widget up to window |

**Key insight:** CustomTkinter and tkinter already handle all the low-level complexity of GUI events, scrolling, and clipboard operations. The framework deals with platform differences (Windows, macOS, Linux) automatically.

## Common Pitfalls

### Pitfall 1: Keyboard Events Not Firing
**What goes wrong:** Bound keyboard events never trigger, shortcuts don't work
**Why it happens:** Keyboard events only go to widgets with focus. If focus is on a widget that doesn't have the binding, event never reaches your handler.
**How to avoid:**
- Bind global shortcuts at window level (on the CTk instance)
- Window is at the top of the focus hierarchy, receives events from all child widgets
- Verify with `bind_all()` if window-level doesn't work
**Warning signs:** Events work when clicking window background but not when clicking buttons/display

### Pitfall 2: Control-C Binding Conflicts
**What goes wrong:** Ctrl+C doesn't copy, or triggers both default and custom behavior
**Why it happens:** Some widgets (Entry, Text) have built-in Ctrl+C support. Custom bindings may conflict or get ignored.
**How to avoid:**
- Use `bind()` not `bind_all()` to avoid overriding widget defaults
- Test that built-in copy still works in Entry widgets
- For custom copy behavior, bind at window level and check if focused widget is Entry/Text
**Warning signs:** Copy works in some contexts but not others

### Pitfall 3: Lambda Closure Bug in Loops
**What goes wrong:** All bound events call the same function with the same (wrong) parameter
**Why it happens:** Late binding in Python lambdas - all lambdas share the same loop variable reference
**How to avoid:**
```python
# WRONG - all bindings will use final value of char
for char in "0123456789":
    self.bind(char, lambda e: self._handle_char(char))

# CORRECT - use default parameter to capture current value
for char in "0123456789":
    self.bind(char, lambda e, c=char: self._handle_char(c))
```
**Warning signs:** All number keys insert "9" (or whatever the last loop value was)

### Pitfall 4: Clipboard Empty/Non-Text Error Handling
**What goes wrong:** App crashes when user presses Ctrl+V with empty clipboard or non-text clipboard content
**Why it happens:** `clipboard_get()` raises `TclError` if clipboard is empty or contains non-text data (images, files)
**How to avoid:**
```python
def paste_from_clipboard(self):
    try:
        return self.clipboard_get()
    except tk.TclError:
        return None  # Clipboard empty or non-text
```
**Warning signs:** App crashes with TclError when testing paste without copying first

### Pitfall 5: Clipboard Persistence on Linux/X11
**What goes wrong:** Copied text disappears after app closes (Linux only)
**Why it happens:** On X11, clipboard is owned by the app that set it. When app exits, clipboard may be cleared unless a clipboard manager (Klipper, etc.) is running.
**How to avoid:**
- Document this as known platform behavior (not a bug)
- Most modern Linux desktops have clipboard managers
- Consider brief update_idletasks() after clipboard_append() to give clipboard manager time to grab content
**Warning signs:** Users report copy doesn't work (but it does while app is running)

### Pitfall 6: Key Name Case Sensitivity
**What goes wrong:** Binding `<return>` or `<backspace>` doesn't work
**Why it happens:** Special key names are case-sensitive in tkinter - must match exact capitalization
**How to avoid:** Use correct key names from documentation:
- `<Return>` (not return, Enter, or enter)
- `<BackSpace>` (not backspace or Backspace)
- `<Escape>` (not escape or ESC)
**Warning signs:** Binding code looks correct but events never fire

### Pitfall 7: CTkScrollableFrame Widget Layering
**What goes wrong:** Widgets added to scrollable frame don't scroll or don't appear
**Why it happens:** Need to add widgets to the frame itself, and frame needs proper size configuration
**How to avoid:**
```python
# In custom CTkScrollableFrame subclass
class HistoryPanel(ctk.CTkScrollableFrame):
    def add_entry(self, text):
        label = ctk.CTkLabel(self, text=text)  # Use 'self' as parent
        label.pack()  # pack/grid on the frame
```
**Warning signs:** History entries don't appear, or appear but don't scroll

### Pitfall 8: Unbounded History Growth
**What goes wrong:** Memory usage grows indefinitely as calculations accumulate
**Why it happens:** No limit on history list size, both in data structure and UI widgets
**How to avoid:**
- Set max_history limit (e.g., 100 entries)
- Pop oldest entry when limit reached
- Call `.destroy()` on oldest widget before removing from list
**Warning signs:** App gets slower over time, memory usage increases

## Code Examples

Verified patterns from official sources:

### Binding Keyboard Events
```python
# Source: Tkinter event binding documentation
class CalculatorWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        # Bind keyboard shortcuts at window level
        self._bind_keyboard_shortcuts()

    def _bind_keyboard_shortcuts(self):
        """Bind all keyboard shortcuts."""
        # Enter = equals
        self.bind("<Return>", lambda e: self.on_key_enter())

        # Escape = clear
        self.bind("<Escape>", lambda e: self.on_key_escape())

        # Backspace = delete last char
        self.bind("<BackSpace>", lambda e: self.on_key_backspace())

        # Ctrl+C = copy result
        self.bind("<Control-c>", lambda e: self.on_key_copy())

        # Ctrl+V = paste
        self.bind("<Control-v>", lambda e: self.on_key_paste())

        # Numbers and operators (avoid lambda closure bug)
        for char in "0123456789+-*/().":
            self.bind(char, lambda e, c=char: self.on_key_char(c))

    def on_key_enter(self):
        """Handle Enter key press."""
        if self.button_callback:
            self.button_callback("=")

    # ... other key handlers ...
```

### Clipboard Operations
```python
# Source: Tkinter clipboard methods documentation
def handle_copy(self):
    """Copy current result to clipboard."""
    result_text = self.display.get_result()

    # Clear and append in sequence
    self.clipboard_clear()
    self.clipboard_append(result_text)

    # Optional: Show visual feedback
    # self.show_copy_confirmation()

def handle_paste(self):
    """Paste clipboard content to expression."""
    try:
        clipboard_text = self.clipboard_get()
        if clipboard_text and self.button_callback:
            # Validate it's a number before pasting
            try:
                float(clipboard_text)  # Check if numeric
                self.button_callback(clipboard_text)
            except ValueError:
                pass  # Ignore non-numeric clipboard content
    except tk.TclError:
        # Clipboard empty or non-text - ignore silently
        pass
```

### CTkScrollableFrame for History
```python
# Source: CustomTkinter CTkScrollableFrame documentation
import customtkinter as ctk

class HistoryPanel(ctk.CTkScrollableFrame):
    """Scrollable history panel showing past calculations."""

    def __init__(self, master, width=250, **kwargs):
        super().__init__(master, width=width, **kwargs)

        self.history_entries = []
        self.recall_callback = None

        # Header
        header = ctk.CTkLabel(
            self,
            text="Historia",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        header.pack(pady=(0, 10), anchor="w")

    def set_recall_callback(self, callback):
        """Set callback for when history entry is clicked."""
        self.recall_callback = callback

    def add_entry(self, expression, result):
        """Add a calculation to history."""
        entry_frame = ctk.CTkFrame(self, fg_color="transparent")
        entry_frame.pack(fill="x", pady=2)

        # Expression and result on one line
        text = f"{expression} = {result}"
        label = ctk.CTkLabel(
            entry_frame,
            text=text,
            cursor="hand2",
            anchor="w"
        )
        label.pack(fill="x", padx=5)

        # Make clickable
        label.bind("<Button-1>", lambda e: self._on_entry_click(result))

        self.history_entries.append(entry_frame)

    def _on_entry_click(self, result):
        """Handle click on history entry."""
        if self.recall_callback:
            self.recall_callback(result)

    def clear_history(self):
        """Remove all history entries."""
        for entry in self.history_entries:
            entry.destroy()
        self.history_entries.clear()
```

### Angle Mode Toggle
```python
# Source: CustomTkinter segmented button documentation
# In DisplayPanel or CalculatorWindow
class DisplayPanel(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # ... existing display code ...

        # Angle mode toggle
        self.angle_mode_selector = ctk.CTkSegmentedButton(
            self,
            values=["DEG", "RAD"],
            width=120
        )
        self.angle_mode_selector.set("DEG")
        self.angle_mode_selector.grid(row=2, column=0, pady=(5, 0))

        self.angle_mode_callback = None

    def set_angle_mode_callback(self, callback):
        """Set callback for angle mode changes."""
        self.angle_mode_callback = callback
        self.angle_mode_selector.configure(command=self._on_angle_mode_change)

    def _on_angle_mode_change(self, value):
        """Handle angle mode toggle."""
        # Map UI value to engine constant
        mode_map = {
            "DEG": "degrees",  # ANGLE_MODE_DEGREES
            "RAD": "radians"   # ANGLE_MODE_RADIANS
        }
        if self.angle_mode_callback:
            self.angle_mode_callback(mode_map[value])
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Manual Canvas scrolling | CTkScrollableFrame | CustomTkinter 5.0+ | Simpler code, better UX, automatic platform handling |
| bind_all() for global shortcuts | Window-level bind() | Always recommended | Avoids conflicts with widget defaults |
| pyperclip for clipboard | tkinter clipboard methods | Always available | Removes external dependency |
| Static layouts only | Responsive grid with weights | Modern GUI design | Better multi-DPI, resizing support |

**Deprecated/outdated:**
- Manual scrollbar + canvas frame: CTkScrollableFrame replaces this pattern entirely
- `<Enter>` key name: Never worked, correct name is `<Return>`

## Open Questions

Things that couldn't be fully resolved:

1. **Should history persist across app sessions?**
   - What we know: Requirements don't mention persistence, no database/file I/O in current codebase
   - What's unclear: Whether this is a future requirement or intentionally session-only
   - Recommendation: Implement as in-memory list for now (YAGNI principle), easy to add file persistence later if needed

2. **Should Ctrl+C work when result is selected or always copy result?**
   - What we know: Windows Calculator copies selected text if any, otherwise copies result
   - What's unclear: Expected behavior for this calculator
   - Recommendation: Always copy current result (simpler), display is read-only anyway

3. **Should history panel be always visible or toggleable?**
   - What we know: Requirements say "side panel displays list" but don't specify toggle behavior
   - What's unclear: If panel should be collapsible/hideable
   - Recommendation: Always visible for MVP, can add toggle in future iteration if needed

4. **Maximum history limit?**
   - What we know: Need to prevent unbounded growth
   - What's unclear: What limit is appropriate
   - Recommendation: 100 entries (reasonable for typical use, ~10KB memory)

5. **Gradians support in UI?**
   - What we know: SafeEvaluator supports gradians (ANGLE_MODE_GRADIANS), but requirement only mentions DEG/RAD
   - What's unclear: Whether gradians toggle should be exposed
   - Recommendation: Only show DEG/RAD per requirements, easy to add GRAD as third option later

## Sources

### Primary (HIGH confidence)
- [CustomTkinter CTkScrollableFrame documentation](https://customtkinter.tomschimansky.com/documentation/widgets/scrollableframe/) - Official widget API
- [CustomTkinter CTkScrollableFrame wiki](https://github.com/TomSchimansky/CustomTkinter/wiki/CTkScrollableFrame) - Implementation examples
- [Tkinter key names reference](https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/key-names.html) - Complete key name list
- [Tkinter universal methods](https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/universal.html) - Clipboard and focus methods

### Secondary (MEDIUM confidence)
- [Tkinter Event Binding tutorial](https://www.pythontutorial.net/tkinter/tkinter-event-binding/) - Event binding patterns
- [Tkinter clipboard operations](https://www.tutorialspoint.com/copy-from-clipboard-using-python-and-tkinter) - Clipboard usage examples
- [Python tkinter documentation](https://docs.python.org/3/library/tkinter.html) - Official Python docs (clipboard methods mentioned but not detailed)
- [Tkinter keyboard binding best practices](https://www.goingthewongway.com/tkinter-keyboard-bindings-in-python/) - Common patterns and mistakes
- [Tkinter Mistakes Guide](https://tkinterbuilder.com/tkinter-mistakes-guide.html) - Pitfalls to avoid

### Tertiary (LOW confidence - WebSearch only)
- Calculator UI design patterns - General UX guidance, not implementation-specific
- Calculator history app examples - Various implementations, not authoritative

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - All libraries already in use or stdlib
- Architecture patterns: HIGH - Verified from official CustomTkinter and tkinter documentation
- Keyboard bindings: HIGH - Official tkinter event documentation with key names
- Clipboard operations: MEDIUM - Documented in universal methods, but error handling details from community sources
- History UI patterns: HIGH - Official CTkScrollableFrame documentation
- Pitfalls: MEDIUM - Mix of official docs and experienced developer guides

**Research date:** 2026-02-05
**Valid until:** ~60 days (CustomTkinter is stable, tkinter is stdlib, patterns unlikely to change)

**Notes for planner:**
- Existing codebase has MVC structure well-established - maintain separation
- Controller should hold history list and coordinate between model (angle mode) and view (keyboard, history panel)
- All angle mode logic exists in evaluator - only need UI exposure
- Phase 2 uses StringVar for reactive display - maintain this pattern for angle mode display
- Polish locale strings already exist - check if new strings needed for history/angle mode
