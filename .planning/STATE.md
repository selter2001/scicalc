# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-02-05)

**Core value:** Kalkulator musi dzialac bezblednie — poprawne obliczenia z czytelnym, nowoczesnym interfejsem.
**Current focus:** Phase 3 - Advanced Modes & History

## Current Position

Phase: 3 of 4 (Advanced Modes & History) — IN PROGRESS
Plan: 01 of 2 in phase (plan 03-01 complete)
Status: Phase 3 in progress — 1 plan complete, 1 remaining
Last activity: 2026-02-05 — Completed 03-01-PLAN.md (angle mode, keyboard, clipboard)

Progress: [██████████████░░] 5/8 total plans complete (Phase 1: 2/2, Phase 2: 2/2, Phase 3: 1/2)

## Performance Metrics

**Velocity:**
- Total plans completed: 5
- Average duration: 3.31 min
- Total execution time: 0.28 hours

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 01-project-foundation-core-engine | 2 | 5.37 min | 2.69 min |
| 02-scientific-functions-basic-gui | 2 | 8.40 min | 4.20 min |
| 03-advanced-modes-history | 1 | 2.70 min | 2.70 min |

**Recent Trend:**
- Last 5 plans: 01-02 (3.87 min), 02-01 (4.52 min), 02-02 (3.88 min), 03-01 (2.70 min)
- Trend: Decreasing - last plan significantly faster

*Updated after each plan completion*

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.
Recent decisions affecting current work:

- Phase 1: Must use safe parser (simpleeval/asteval) instead of eval() to avoid security vulnerabilities
- Phase 1: Must use Decimal module for precision arithmetic to eliminate float representation errors
- Phase 2: Angle mode system critical for correct trigonometric calculations
- **01-01:** Modular OOP structure established: logic/, ui/, controller/, config/ separation
- **01-01:** Polish localization centralized in config/locale.py with proper diacritics
- **01-01:** Decimal precision set to 28 digits with ROUND_HALF_UP for financial accuracy
- **01-01:** simpleeval chosen as safe expression parser (vs eval())
- **01-02:** Float-to-Decimal bridge pattern: Decimal(str(round(result, 10))) to handle simpleeval's float results
- **01-02:** Stack-based parentheses validation for O(n) performance and position tracking
- **01-02:** Validator-Evaluator-Orchestrator pattern separates concerns (validation, evaluation, formatting)
- **02-01:** Power operator precedence: preprocess ^ to ** instead of AST remapping
- **02-01:** Angle mode with dynamic function rebuilding (closures capture mode, rebuild on change)
- **02-01:** Custom _safe_factorial wrapper for localized validation errors
- **02-02:** MVC pattern with controller mediating between view and engine
- **02-02:** StringVar for reactive display updates without manual refresh
- **02-02:** Lambda closure pattern (lambda l=label) to capture button labels correctly
- **02-02:** Dependency injection in controller constructor for testability
- **02-02:** Dark theme set before window creation via ctk.set_appearance_mode
- **02-02:** Button color coding: numbers dark, operators orange, functions gray, actions light
- **02-02:** LABEL_TO_TOKEN mapping: Transform button labels (√, π, x^y) to engine tokens (sqrt(, pi, ^)
- **03-01:** CTkSegmentedButton for DEG/RAD angle mode toggle (always visible below result)
- **03-01:** Lambda closure pattern with default param (lambda e, c=char) for keyboard binding loops
- **03-01:** Window-level keyboard bindings ensure input works regardless of widget focus
- **03-01:** Return 'break' from clipboard handlers prevents tkinter default Ctrl+C/V behavior
- **03-01:** Clipboard paste validation: only numeric/operator characters allowed (0-9, +, -, *, /, (, ), ., e, E)

### Pending Todos

[From .planning/todos/pending/ — ideas captured during sessions]

None yet.

### Blockers/Concerns

[Issues that affect future work]

- ~~Phase 1: Need to select safe expression parser library (simpleeval vs asteval vs custom) — research during planning~~ RESOLVED: simpleeval selected
- ~~Phase 2: Need to extend SafeEvaluator with math functions while maintaining security constraints~~ RESOLVED: 02-01 complete with 8 scientific functions
- ~~Phase 2: Angle mode implementation needs to integrate with simpleeval's evaluation context~~ RESOLVED: Dynamic function rebuilding pattern
- ~~Phase 2: GUI needs to wire up scientific buttons to backend functions (Plan 02-02)~~ RESOLVED: 02-02 complete with MVC controller and button mapping
- ~~Phase 3: Keyboard input handling for GUI~~ RESOLVED: 03-01 complete with window-level bindings
- Phase 3: Angle mode state management for UI persistence (DEG/RAD toggle state)
- Phase 3: Need inverse trigonometric functions (asin, acos, atan) - constants already defined
- Phase 3: History panel for expression tracking (Plan 03-02)

## Session Continuity

Last session: 2026-02-05T20:13:36Z
Stopped at: Completed 03-01-PLAN.md
Resume file: None

---
*State initialized: 2026-02-05*
*Last updated: 2026-02-05 after 03-01 completion*
