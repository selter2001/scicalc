---
phase: 02-scientific-functions-basic-gui
plan: 02
subsystem: ui
tags: [customtkinter, gui, mvc, tkinter, dark-theme, responsive-layout]

# Dependency graph
requires:
  - phase: 02-01
    provides: Scientific calculation engine with CalculatorEngine API (calculate, set_angle_mode)
  - phase: 01-02
    provides: Decimal precision, error handling, Polish locale system
provides:
  - CustomTkinter GUI with dark theme and responsive grid layout
  - MVC controller pattern connecting UI to calculation engine
  - DisplayPanel showing expression and result with StringVar updates
  - ButtonPanel with basic/scientific mode switching and rounded buttons
  - Polish interface with button labels and window title
  - Controller with LABEL_TO_TOKEN mapping for scientific buttons
affects: [03-enhanced-ui-keyboard, 03-enhanced-ui-history, 04-deployment]

# Tech tracking
tech-stack:
  added: [customtkinter>=5.2.0, darkdetect]
  patterns: [MVC controller pattern, StringVar for reactive display, lambda closure for button callbacks, dependency injection for testability]

key-files:
  created:
    - src/calculator/ui/calculator_window.py
    - src/calculator/ui/display.py
    - src/calculator/ui/button_panel.py
    - src/calculator/controller/calculator_controller.py
    - tests/test_controller.py
  modified:
    - src/calculator/config/locale.py
    - src/calculator/config/constants.py
    - src/calculator/main.py

key-decisions:
  - "MVC pattern with controller mediating between view and engine"
  - "StringVar for reactive display updates without manual refresh"
  - "Lambda closure pattern (lambda l=label) to capture button labels correctly"
  - "Dependency injection in controller constructor for testability"
  - "Dark theme set before window creation via ctk.set_appearance_mode"
  - "Button color coding: numbers dark, operators orange, functions gray, actions light"

patterns-established:
  - "MVC Controller Pattern: CalculatorController mediates between CalculatorWindow (view) and CalculatorEngine (model)"
  - "LABEL_TO_TOKEN mapping: Transform button labels (√, π, x^y) to engine tokens (sqrt(, pi, ^)"
  - "Mock view testing: Controller tests use Mock() for view to test logic independently"
  - "Grid weight configuration: responsive resizing with grid_rowconfigure/columnconfigure weight=1"

# Metrics
duration: 3.88min
completed: 2026-02-05
---

# Phase 2 Plan 2: Basic GUI Summary

**CustomTkinter GUI with dark theme, responsive layout, basic/scientific mode toggle, and MVC controller wiring to calculation engine**

## Performance

- **Duration:** 3.88 min
- **Started:** 2026-02-05T19:37:58Z
- **Completed:** 2026-02-05T19:41:51Z
- **Tasks:** 2
- **Files modified:** 8 (3 created UI, 1 created controller, 1 created tests, 3 extended)

## Accomplishments
- Complete CustomTkinter GUI with dark theme and rounded buttons (corner_radius=10)
- Responsive grid layout that expands/shrinks buttons with window resize
- DisplayPanel with expression (top, 16pt) and result (bottom, 32pt bold) labels using StringVar
- ButtonPanel with basic (5 rows x 4 cols) and scientific mode (+3 rows) layouts
- MVC controller with LABEL_TO_TOKEN mapping for scientific buttons (√→sqrt(, π→pi, x^y→^, n!→factorial()
- Main.py as GUI entry point launching controller.run()
- 15 controller unit tests with mocked view (100% pass rate)
- All 139 tests passing (124 engine + 15 controller)

## Task Commits

Each task was committed atomically:

1. **Task 1: Create UI components and extend config** - `67a55ea` (feat)
2. **Task 2: Create controller, update main.py, and add tests** - `ed3703a` (feat)

## Files Created/Modified
- `src/calculator/ui/calculator_window.py` - Main CTk window with mode selector, display, button panel, responsive grid
- `src/calculator/ui/display.py` - DisplayPanel with expression/result labels using StringVar for reactive updates
- `src/calculator/ui/button_panel.py` - ButtonPanel with basic/scientific layouts, rounded CTkButtons, color coding
- `src/calculator/controller/calculator_controller.py` - MVC controller mediating UI events to CalculatorEngine
- `src/calculator/main.py` - GUI entry point launching CalculatorController().run()
- `src/calculator/config/locale.py` - Extended with Polish button labels and window title
- `src/calculator/config/constants.py` - Extended with UI layouts, colors, fonts, geometry constants
- `tests/test_controller.py` - 15 controller unit tests with mocked view

## Decisions Made
- **MVC pattern:** Controller mediates between view and engine, enabling testability with mocked view
- **StringVar for display:** Reactive updates without manual refresh - controller calls update_expression/update_result
- **Lambda closure pattern:** `lambda l=label: callback(l)` to correctly capture button label values in loops
- **Dependency injection:** Controller accepts optional engine/view params for testing with mocks
- **Dark theme before window:** `ctk.set_appearance_mode("dark")` must be called before creating CTk window
- **Button color coding:** Numbers (#2B2B2B dark), operators (#FF9500 orange), functions (#505050 gray), actions (#D4D4D2 light)
- **LABEL_TO_TOKEN mapping:** Transform UI symbols to engine tokens (√→sqrt(, π→pi, x^y→^, n!→factorial()

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Installed missing customtkinter dependency**
- **Found during:** Task 1 verification (import test)
- **Issue:** customtkinter not installed, imports failing - required for GUI
- **Fix:** Ran `pip3 install "customtkinter>=5.2.0"` which also installed darkdetect dependency
- **Files modified:** None (system-level package installation)
- **Verification:** Import test passed, all UI modules importable
- **Committed in:** Not applicable (package installation, not code change)

**2. [Rule 3 - Blocking] Fixed import paths to use src. prefix**
- **Found during:** Task 2 verification (pytest collection failed)
- **Issue:** UI modules and controller used relative imports without src. prefix, conflicting with existing codebase pattern
- **Fix:** Changed all imports from `calculator.X` to `src.calculator.X` to match existing pattern in logic/evaluator/validator modules
- **Files modified:**
  - src/calculator/ui/display.py
  - src/calculator/ui/button_panel.py
  - src/calculator/ui/calculator_window.py
  - src/calculator/controller/calculator_controller.py
  - src/calculator/main.py
- **Verification:** All 139 tests passed (124 engine + 15 controller)
- **Committed in:** ed3703a (Task 2 commit)

---

**Total deviations:** 2 auto-fixed (2 blocking)
**Impact on plan:** Both auto-fixes necessary to unblock execution. Import path consistency required for test suite compatibility. No scope creep.

## Issues Encountered
None - plan executed smoothly after resolving import patterns and dependency installation.

## Next Phase Readiness
**Ready for Phase 3 enhanced UI features:**
- ✓ GUI foundation complete with responsive layout
- ✓ MVC pattern established for clean separation
- ✓ Controller tested independently with mocked view
- ✓ Basic/scientific mode toggle working
- ✓ All buttons wired to controller callbacks
- ✓ Display updates correctly via StringVar

**Future enhancements ready to build on:**
- Keyboard input handling (Phase 3)
- History panel (Phase 3)
- Angle mode UI selector (Phase 3)
- Memory functions UI (Phase 3)

**No blockers or concerns.**

---
*Phase: 02-scientific-functions-basic-gui*
*Completed: 2026-02-05*
