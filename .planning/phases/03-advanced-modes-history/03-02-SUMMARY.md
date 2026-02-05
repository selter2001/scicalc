---
phase: 03-advanced-modes-history
plan: 02
subsystem: ui
tags: [customtkinter, history, scrollable-panel, click-to-recall, polish-localization]

# Dependency graph
requires:
  - phase: 03-01
    provides: "Angle mode toggle, keyboard bindings, clipboard support in CalculatorWindow"
  - phase: 02-02
    provides: "MVC controller pattern, calculator window layout, button panel"
provides:
  - "Scrollable history side panel (HistoryPanel) with previous calculations display"
  - "Click-to-recall functionality for inserting history results into expression"
  - "History clear button with synchronized UI and controller state"
  - "2-column window layout (calculator left, history right)"
  - "History state management with MAX_HISTORY_ENTRIES limit enforcement"
affects: [Phase 4 might extend history with persistence, export features]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "CTkScrollableFrame for history entries list with dynamic widget creation"
    - "Lambda closure pattern (lambda e, r=result) for click event binding in loops"
    - "Chronological history display (oldest top, newest bottom)"
    - "2-column grid layout pattern: expanding left column, fixed-width right column"
    - "Empty state pattern: show message when no history entries exist"
    - "History limit enforcement with pop(0) to remove oldest entry"

key-files:
  created:
    - "src/calculator/ui/history_panel.py"
  modified:
    - "src/calculator/ui/calculator_window.py"
    - "src/calculator/controller/calculator_controller.py"
    - "src/calculator/config/locale.py"
    - "src/calculator/config/constants.py"
    - "tests/test_controller.py"

key-decisions:
  - "HistoryPanel as CTkFrame with CTkScrollableFrame for entries (not CTkScrollableFrame directly)"
  - "Lambda closure pattern with default param captures result correctly in click bindings"
  - "Chronological order: oldest top, newest bottom (append pattern)"
  - "2-column layout: calc_frame wraps calculator components, history_panel in column 1"
  - "History recall appends result to expression (vs replacing) for composability"
  - "History recall clears error state before inserting result"
  - "MAX_HISTORY_ENTRIES=100 enforced with pop(0) to remove oldest"
  - "Empty state label recreated after clear (not persistent hidden widget)"
  - "Window width increased to 700px (min 650px) to accommodate history panel"

patterns-established:
  - "Multi-column window layout: transparent wrapper frames for grouped components"
  - "History state synchronization: controller maintains list, view manages UI"
  - "Callback wiring pattern: set_*_callback methods for loose coupling"
  - "Empty state handling: destroy/recreate label vs hide/show toggle"

# Metrics
duration: 2.77min
completed: 2026-02-05
---

# Phase 3 Plan 2: History Panel Summary

**Scrollable history side panel with click-to-recall in 2-column layout, history limited to 100 entries, synchronized controller state**

## Performance

- **Duration:** 2.77 min
- **Started:** 2026-02-05T20:16:49Z
- **Completed:** 2026-02-05T20:19:34Z
- **Tasks:** 2
- **Files modified:** 6

## Accomplishments
- Created scrollable HistoryPanel component with clickable entries, clear button, and empty state
- Integrated history panel into 2-column window layout (calculator left, history right, 700px total width)
- Implemented history state management in controller with MAX_HISTORY_ENTRIES enforcement
- Added click-to-recall functionality that inserts result into expression and clears error state
- Extended test suite with 7 history tests covering add, recall, clear, limit, error scenarios
- All 156 tests pass (149 from previous plans + 7 new history tests)

## Task Commits

Each task was committed atomically:

1. **Task 1: Create HistoryPanel component and add Polish locale strings** - `01a810c` (feat)
2. **Task 2: Integrate history panel into window layout and controller, add tests** - `f284ddc` (feat)

## Files Created/Modified
- `src/calculator/ui/history_panel.py` - Scrollable history panel with clickable entries, clear button, empty state (CTkFrame with CTkScrollableFrame)
- `src/calculator/ui/calculator_window.py` - Restructured to 2-column layout with calc_frame (left) and history_panel (right), added convenience methods
- `src/calculator/controller/calculator_controller.py` - Added history list, wire callbacks, add on calculate, recall inserts result, clear syncs state
- `src/calculator/config/locale.py` - Added Polish strings: HIST_TITLE="Historia", HIST_CLEAR="Wyczysc historie", HIST_EMPTY="Brak historii"
- `src/calculator/config/constants.py` - Added MAX_HISTORY_ENTRIES=100, HISTORY_PANEL_WIDTH=250, WINDOW_WITH_HISTORY_WIDTH=700, font sizes
- `tests/test_controller.py` - Extended mock_view with history methods, added 7 history tests

## Decisions Made

1. **HistoryPanel wrapping pattern:** Used CTkFrame as container with CTkScrollableFrame inside (vs making HistoryPanel extend CTkScrollableFrame) - allows header and clear button outside scrollable area
2. **Lambda closure with default param:** `lambda e, r=result: self._on_entry_click(r)` captures result correctly in loop (avoids late binding bug)
3. **Chronological order:** Oldest entries at top, newest at bottom - natural append pattern matches user expectation of history growth
4. **2-column layout implementation:** Created transparent calc_frame wrapper for left column components, moved all calculator widgets from self to calc_frame parent
5. **History recall behavior:** Appends result to expression (vs replacing) - enables composability like "5+[click history 42]" → "5+42"
6. **History recall error handling:** Clears error state before inserting - prevents confusion when clicking history after division by zero
7. **History limit enforcement:** Use pop(0) to remove oldest when exceeding MAX_HISTORY_ENTRIES=100 - simple FIFO queue pattern
8. **Empty state recreation:** Destroy/recreate empty label after clear (vs hide/show toggle) - simpler state management, no persistent hidden widget
9. **Window geometry update:** Increased to 700px width (min 650px) - accommodates 250px history panel plus 400px calculator with padding
10. **Grid weight configuration:** Column 0 weight=1 (calculator expands), column 1 weight=0 (history fixed width) - history panel maintains constant 250px

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None - implementation proceeded smoothly with all tests passing on first run.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Phase 3 complete! All advanced features implemented:
- Angle mode toggle (DEG/RAD) integrated with trigonometric functions
- Keyboard input support with shortcuts (Enter, Escape, Backspace, Ctrl+C, Ctrl+V)
- Clipboard operations (copy result, paste with validation)
- History panel with click-to-recall and clear functionality

Ready for Phase 4 (polish, refinement, or additional features as specified in project plan).

**Blockers/Concerns:**
- None - all Phase 3 requirements satisfied
- Potential future enhancement: history persistence (save/load on app restart)
- Potential future enhancement: history export to file
- Potential future enhancement: inverse trigonometric functions (asin, acos, atan) - constants defined but not implemented

---
*Phase: 03-advanced-modes-history*
*Completed: 2026-02-05*
