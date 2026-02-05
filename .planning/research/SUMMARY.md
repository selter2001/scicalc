# Project Research Summary

**Project:** Python Scientific Calculator with CustomTkinter
**Domain:** Desktop GUI Application (Scientific Calculator)
**Researched:** 2026-02-05
**Confidence:** HIGH

## Executive Summary

Scientific calculators are a well-established domain where success depends on flawless execution of expected features rather than innovation. The research confirms that a Python-based desktop calculator should use CustomTkinter for the GUI (modern, cross-platform, minimal dependencies), Python's `decimal` module for precision arithmetic (eliminating float errors), and follow MVC architecture with clear separation between calculation logic, UI components, and control flow.

The critical risk is using Python's `eval()` for expression evaluation, which creates catastrophic security vulnerabilities. Research strongly recommends safe alternatives like `simpleeval` or `asteval` libraries, or implementing a custom operator-precedence parser. The second major risk is floating-point precision errors—using `Decimal` instead of `float` is non-negotiable for calculator accuracy. Third, radians/degrees confusion in trigonometric functions will silently produce wrong results unless properly managed with explicit mode indicators and conversion wrappers.

The recommended approach is incremental development: Phase 1 (core calculation engine with safe parsing and precision handling), Phase 2 (GUI with basic/scientific mode toggle), Phase 3 (history panel and keyboard support), Phase 4 (polish and testing). This ordering enables testing the most critical components (accuracy, security) first, with each phase delivering a working product.

## Key Findings

### Recommended Stack

Python 3.10+ with CustomTkinter 5.2.2 provides the optimal foundation for a modern desktop calculator. CustomTkinter offers native OS integration, automatic dark/light mode, and minimal dependencies compared to Qt/Electron alternatives. The stack prioritizes correctness over performance, using stdlib where possible.

**Core technologies:**
- **Python 3.10+**: Required for macOS dark mode support; provides modern type hints and pattern matching
- **CustomTkinter 5.2.2**: Modern Tkinter wrapper with built-in dark theme, active development (13.1k stars), cross-platform consistency
- **decimal module (stdlib)**: Financial-grade precision (28 decimal places default) eliminates float representation errors—critical for calculator trust
- **Ruff 0.15.0**: Replaces Black + Flake8 + isort; 30x faster formatting, single tool simplifies CI
- **pytest 9.0.2**: Industry standard testing with clean syntax; use xvfb for headless GUI tests in CI
- **PyInstaller 6.18.0**: Creates standalone executables for Windows/macOS/Linux; use `--onedir` for faster startup

**Critical version requirements:**
- Python 3.10+ minimum (3.9 has macOS dark mode quirks)
- CustomTkinter 5.2.2 or later (active development, update monthly)

**Why NOT NumPy/SciPy:** 50MB dependency for scalar math is overkill; stdlib `decimal` and `math` modules are sufficient.

### Expected Features

Scientific calculator users have crystal-clear expectations formed by decades of hardware calculators and established software. Missing any table stakes feature makes the product feel incomplete; feature differentiation comes from execution quality, not novelty.

**Must have (table stakes):**
- Basic arithmetic (+, -, ×, ÷) with correct order of operations (PEMDAS)
- Parentheses with nested support and bracket matching validation
- Scientific functions: sin, cos, tan, arcsin, arccos, arctan, ln, log10, √, x², xʸ
- Constants: π, e
- Angle mode toggle (DEG/RAD/GRAD) with prominent indicator—wrong mode causes catastrophic calculation errors
- Clear (C) and All Clear (AC) buttons
- Delete/backspace for input corrections
- Error handling for division by zero, domain errors (√-1, ln(-5))
- ANS (previous result) for chaining calculations
- Multi-line display showing expression + result simultaneously
- Calculation history panel (clickable to recall)
- Keyboard support (desktop users expect number keys, operators, Enter for =)

**Should have (competitive differentiators):**
- Copy/paste support (integrate with desktop workflow)
- Expression editing with cursor navigation
- Dark theme (already planned)
- Polish language UI (already planned, local market advantage)
- Export history to TXT/CSV
- Memory slots (M+, M-, MR, MC)
- Unit converter (adjacent need, medium complexity)

**Defer (v2+ or avoid entirely):**
- Graphing capabilities (scope creep, immense complexity—different product category)
- Symbolic algebra/CAS (very high complexity, defer to SymPy/Mathematica)
- Matrix operations (limited audience, high UI complexity)
- Statistics functions (requires data entry UI, different use case)
- Cloud sync, social features, voice input (unnecessary complexity, wrong paradigm for desktop calculator)

**Critical insight:** Calculators live or die by accuracy and reliability. A calculator with occasional wrong results is worthless regardless of feature count. "Clarity over complexity" is the guiding principle.

### Architecture Approach

Python GUI calculators with CustomTkinter should follow class-based Model-View-Controller (MVC) architecture with modular components organized by responsibility. This structure separates calculation logic (Model), UI presentation (View), and event coordination (Controller) into distinct modules, avoiding the common anti-pattern of monolithic single-file applications with global variables.

**Major components:**

1. **Model Layer** (`logic/`):
   - `CalculatorEngine` — performs mathematical operations, evaluates expressions using safe parser (NOT `eval()`)
   - `HistoryManager` — stores/retrieves calculation history with JSON persistence
   - `Evaluator` — safely evaluates expressions; handles error cases (division by zero, invalid syntax)
   - `ScientificFunctions` — wraps Python `math` module with angle mode awareness
   - **Key principle:** No UI dependencies; pure Python functions/classes; fully testable

2. **View Layer** (`ui/`):
   - `MainWindow` (inherits `customtkinter.CTk`) — root window managing overall layout and theme
   - `DisplayField` — shows current input and results (multi-line preferred)
   - `ButtonPanel` — grid of calculator buttons; mode-aware (basic/scientific)
   - `HistoryPanel` — sidebar with scrollable history; supports double-click recall
   - `ModeToggle` — switch between basic and scientific modes
   - **Key principle:** Inherits from CTk/CTkFrame; uses `.grid()` geometry (NEVER `.place()`); exposes public methods (`setDisplayText()`, `getDisplayText()`) for controller

3. **Controller Layer** (`controller/`):
   - `CalculatorController` — connects Model and View; handles button clicks; orchestrates data flow
   - `EventHandlers` — maps user events to model operations; updates view with results
   - **Key principle:** Receives Model and View as constructor parameters; implements signal-slot pattern (callback functions)

4. **Configuration** (`config/`):
   - `constants.py` — window dimensions, button sizes, grid layout specs
   - `theme.py` — dark theme colors, CustomTkinter theme selection
   - `locale.py` — Polish UI strings (centralized, NOT hard-coded throughout codebase)

**Data flow:** User clicks button → View calls `controller.on_button_click()` → Controller updates state → Controller calls `model.evaluate()` → Model returns result or raises error → Controller calls `view.setDisplayText()` → Display updates

**Build order:** Configuration modules → Basic Evaluator → CalculatorEngine → Display/ButtonPanel → MainWindow → Controller → Entry point. This dependency order enables incremental testing with working deliverables at each phase.

### Critical Pitfalls

The research identified 15 domain-specific pitfalls; the top 5 require architectural decisions upfront and are expensive to fix later:

1. **Using `eval()` for expression evaluation** — Creates remote code execution vulnerability. Attackers can inject arbitrary code like `__import__('os').system('rm -rf /')`. Blocklists are insufficient; bypass techniques are trivial. **Solution:** Use `simpleeval`, `asteval`, or `numexpr` libraries, or implement custom operator-precedence parser. NEVER use `eval()` or `exec()` on user input. **Severity:** CRITICAL—must decide in Phase 1 (architecture).

2. **Floating-point precision errors** — Python's `float` type causes visible errors: `0.1 + 0.1 + 0.1 == 0.3` evaluates to `False`; displays `0.30000000000000004`. **Solution:** Use `decimal.Decimal` module for all calculator operations (28 decimal places default eliminates representation errors). Set explicit rounding modes. **Severity:** CRITICAL—affects all calculations, hard to change later (Phase 1 decision).

3. **Radians/degrees confusion in trigonometry** — Python's `math.sin()`, `math.cos()`, `math.tan()` ONLY accept radians. Passing degrees directly produces wildly wrong results: `math.sin(30)` returns -0.988, not 0.5. Users expect calculators to default to degrees. **Solution:** Implement explicit mode switching with prominent UI indicator; create wrapper functions (`sin_degrees()`, `sin_radians()`); use `math.radians()` for conversion. **Severity:** CRITICAL—wrong results destroy calculator trust (Phase 1 decision).

4. **Incorrect order of operations** — Expression `2 + 3 * 4` evaluating as `(2 + 3) * 4 = 20` instead of `2 + (3 * 4) = 14`. Left-to-right evaluation violates PEMDAS/BODMAS. **Solution:** Implement operator-precedence parser (precedence climbing method or Shunting Yard algorithm); support implicit multiplication (`2π` → `2*π`). **Severity:** CRITICAL—fundamental requirement for scientific calculator (Phase 1 decision).

5. **No parentheses matching validation** — Unbalanced parentheses like `((2+3)*4` crash parser or hang application. **Solution:** Implement stack-based parentheses matching BEFORE parsing; validate count and ordering; return clear error messages highlighting error location. **Severity:** CRITICAL—affects reliability (Phase 1 decision).

**Moderate pitfalls (fixable without major rewrites):**
- Grid layout without proper sticky/weight configuration (buttons don't resize properly)
- Mode switching without state management (loses current expression)
- Division by zero without error handling (crashes instead of showing message)
- History panel without scroll or size limits (memory issues, UI freezes)
- Dark theme without contrast validation (accessibility issues)

**Minor pitfalls (easily fixable):**
- No keyboard input support (mouse-only feels toy-like)
- Entry widget cursor manipulation bugs (can't edit mid-expression)
- Polish UI strings hard-coded (difficult to update, no i18n structure)
- Memory leaks from TopLevel windows (not calling `.destroy()`)
- No input validation for malformed expressions (`2++3`, `**5`)

## Implications for Roadmap

Based on research findings, the recommended phase structure prioritizes risk mitigation (address critical decisions early) and incremental delivery (each phase produces working product).

### Phase 1: Core Calculation Engine & Safe Parsing

**Rationale:** CRITICAL security and accuracy decisions must be made upfront. `eval()` vulnerability, precision handling, and operator precedence are architectural choices that are expensive to change later. Building the calculation core first enables thorough testing of correctness before adding UI complexity.

**Delivers:**
- Safe mathematical expression parser (using `simpleeval`/`asteval` or custom parser)
- `Decimal`-based arithmetic engine (28-place precision)
- Basic operations (+, -, ×, ÷) with correct PEMDAS precedence
- Parentheses matching validation
- Error handling for division by zero, invalid syntax
- Unit tests verifying calculation accuracy

**Addresses features:**
- Basic arithmetic (table stakes)
- Order of operations (table stakes)
- Parentheses/grouping (table stakes)
- Error handling (table stakes)

**Avoids pitfalls:**
- Pitfall 1: `eval()` vulnerability (CRITICAL)
- Pitfall 2: Floating-point precision errors (CRITICAL)
- Pitfall 4: Incorrect operator precedence (CRITICAL)
- Pitfall 5: No parentheses validation (CRITICAL)
- Pitfall 8: Division by zero crashes (MODERATE)

**Research flag:** HIGH—needs deep research into safe parser libraries (simpleeval vs asteval vs custom implementation). Compare performance, feature coverage, and security posture.

### Phase 2: Scientific Functions & Angle Mode System

**Rationale:** Depends on Phase 1 calculation engine. Scientific functions introduce radians/degrees confusion (critical pitfall). Mode system must be designed carefully to avoid wrong results. Building this before GUI enables testing trig accuracy in isolation.

**Delivers:**
- Trigonometric functions (sin, cos, tan, arcsin, arccos, arctan)
- Logarithms (ln, log10)
- Exponentiation (√, x², xʸ)
- Constants (π, e)
- Angle mode system (DEG/RAD/GRAD) with state management
- Wrapper functions for all trig operations
- Unit tests for all scientific functions in each angle mode

**Addresses features:**
- Trigonometric functions (table stakes)
- Inverse trig (table stakes)
- Logarithms (table stakes)
- Exponentiation (table stakes)
- Square root (table stakes)
- Angle mode toggle (table stakes)
- Constants (table stakes)

**Avoids pitfalls:**
- Pitfall 3: Radians/degrees confusion (CRITICAL)

**Research flag:** MEDIUM—angle mode state management needs design. Should mode be global setting or per-function? How to persist across mode switches?

### Phase 3: GUI Foundation & Basic Mode

**Rationale:** With calculation engine proven accurate, build UI layer. Start with basic mode (fewer buttons, simpler layout) to validate MVC structure and grid layout patterns before adding scientific mode complexity.

**Delivers:**
- MainWindow with CustomTkinter dark theme
- DisplayField (multi-line: expression + result)
- ButtonPanel with basic operations (numbers 0-9, +, -, ×, ÷, =, C, AC, backspace)
- CalculatorController connecting Model and View
- Grid layout with proper sticky/weight configuration
- Entry point (`main.py`) initializing MVC components
- Polish UI strings in `config/locale.py`

**Addresses features:**
- Display shows full expression (table stakes)
- Clear/AC button (table stakes)
- Delete/backspace (table stakes)
- Dark theme (competitive differentiator)
- Polish language UI (competitive differentiator)

**Avoids pitfalls:**
- Pitfall 6: Grid layout without sticky/weight (MODERATE)
- Pitfall 10: Dark theme without accessibility (MODERATE)
- Pitfall 13: Hard-coded Polish strings (MINOR)

**Research flag:** LOW—MVC with CustomTkinter is well-documented. Grid geometry manager has authoritative official docs. Standard patterns apply.

### Phase 4: Scientific Mode & Mode Toggle

**Rationale:** Extends Phase 3 GUI with scientific button panel. Depends on Phase 2 scientific functions. Mode switching introduces state management complexity (moderate pitfall).

**Delivers:**
- Extended ButtonPanel with scientific function buttons
- ModeToggle component (basic ↔ scientific switch)
- Controller mode management (show/hide button groups)
- Angle mode indicator (prominent display)
- State preservation across mode switches (expression, history, angle mode)
- Responsive window resizing for scientific mode

**Addresses features:**
- Angle mode toggle UI (table stakes)
- All scientific functions accessible (table stakes)
- Mode toggle (enhancement—basic calculators don't have separate modes)

**Avoids pitfalls:**
- Pitfall 7: Mode switching without state management (MODERATE)

**Research flag:** MEDIUM—state management design needs careful thought. Which widgets to show/hide vs recreate? How to test all state combinations?

### Phase 5: History Panel & Keyboard Support

**Rationale:** UX enhancements that don't affect calculation correctness. History adds value but is independent of core functionality. Keyboard support is expected on desktop but can be added incrementally.

**Delivers:**
- HistoryPanel with scrollable frame
- HistoryManager with JSON persistence
- Double-click history to recall expression
- Clear history button
- History size limits (last 500 calculations)
- Keyboard event bindings (number keys, operators, Enter, Escape, Backspace)
- ANS button for previous result

**Addresses features:**
- Calculation history panel (table stakes)
- ANS/previous result (table stakes)
- Keyboard support (table stakes)

**Avoids pitfalls:**
- Pitfall 9: History without scroll/limits (MODERATE)
- Pitfall 11: No keyboard input (MINOR)
- Pitfall 12: Entry cursor manipulation bugs (MINOR)

**Research flag:** LOW—JSON persistence is straightforward Python; history panel has verified implementation examples.

### Phase 6: Advanced UX & Testing

**Rationale:** Polish and quality assurance. Copy/paste, expression editing, and comprehensive testing. Unit tests should be written throughout (test-as-you-go), but integration tests and UI polish happen here.

**Delivers:**
- Copy/paste support (Ctrl+C, Ctrl+V)
- Expression editing with cursor navigation (arrow keys, insert mode)
- Comprehensive test suite (unit tests for all logic, GUI integration tests)
- Memory management validation (no leaks from TopLevel windows)
- Input validation for malformed expressions (`2++3` detection)
- Packaging with PyInstaller (standalone executables)
- Final theme/contrast adjustments

**Addresses features:**
- Copy/paste support (competitive differentiator)
- Expression editing (competitive differentiator)

**Avoids pitfalls:**
- Pitfall 14: Memory leaks from TopLevel windows (MINOR)
- Pitfall 15: No input validation (MINOR)

**Research flag:** MEDIUM—GUI testing approaches for CustomTkinter are less mature than PyQt5. May need xvfb for headless CI. Investigate pytest strategies.

### Phase Ordering Rationale

**Why this order:**
1. **Security and accuracy first:** Phases 1-2 address all CRITICAL pitfalls (eval vulnerability, precision errors, trig confusion, operator precedence). Testing core logic before GUI reduces debugging complexity.
2. **Incremental UI complexity:** Phase 3 validates MVC structure with simple basic mode; Phase 4 adds scientific mode complexity only after foundation is proven.
3. **Independent enhancements:** Phases 5-6 add value but don't affect correctness. History and keyboard support can be deferred if timeline pressure exists.
4. **Dependency flow:** Each phase builds on previous: Engine → Scientific functions → Basic GUI → Scientific GUI → UX enhancements → Testing/Polish.

**Why this grouping:**
- **Architecture components:** Model (Phases 1-2), View (Phases 3-4), Controller (Phase 3), Enhancements (Phases 5-6) align with MVC structure recommended in ARCHITECTURE.md.
- **Feature clusters:** Table stakes features span Phases 1-5; competitive differentiators are Phases 3 (dark theme, Polish UI), 5 (history), 6 (copy/paste, expression editing).
- **Risk mitigation:** All CRITICAL pitfalls addressed by end of Phase 2; MODERATE pitfalls addressed by end of Phase 5; MINOR pitfalls addressed in Phase 6.

**How this avoids pitfalls:**
- Front-loading critical decisions (Phases 1-2) prevents expensive architectural rewrites.
- Incremental delivery enables testing at each phase; bugs are caught early when simpler to fix.
- Separation of concerns (MVC) prevents global state anti-patterns and enables unit testing.

### Research Flags

**Phases likely needing deeper research during planning:**

- **Phase 1:** Safe expression parser selection (simpleeval vs asteval vs custom). Need to evaluate: security posture, performance benchmarks, feature coverage (implicit multiplication, scientific notation), community support, licensing. Estimate 2-4 hours research.

- **Phase 2:** Angle mode state management design. Questions: Should angle mode persist in calculator state or be passed to each function? How to display mode prominently without cluttering UI? How to test all combinations? Estimate 1-2 hours design.

- **Phase 4:** Mode switching state preservation strategy. Questions: Which widgets to show/hide vs destroy/recreate? How to prevent memory leaks? How to test state transitions? Review CustomTkinter examples. Estimate 1-2 hours research.

- **Phase 6:** GUI testing approaches for CustomTkinter. Questions: Can pytest-qt work with CustomTkinter? Need xvfb for headless CI? How to mock button clicks? Unit vs integration test balance? Estimate 2-3 hours research.

**Phases with standard patterns (skip research-phase):**

- **Phase 3:** MVC with CustomTkinter, grid layout—well-documented in official CustomTkinter wiki and Real Python tutorials. TkDocs has authoritative grid geometry guide.
- **Phase 5:** JSON persistence, keyboard event binding—straightforward Python stdlib. History panel has verified implementation examples.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | CustomTkinter 5.2.2 verified via PyPI and official docs; Python 3.10+ stdlib well-documented; Ruff/pytest verified production-ready. All core library versions confirmed. |
| Features | HIGH | Scientific calculator domain is well-established; table stakes features verified across multiple sources (SSL Shopper, technical reviews, UX studies). User research confirms clarity over complexity principle. |
| Architecture | HIGH | MVC pattern verified with Real Python tutorial and official Tkinter examples; CustomTkinter wiki explicitly recommends class-based structure and `.grid()` usage. File organization follows Hitchhiker's Guide to Python authoritative guidance. |
| Pitfalls | HIGH | `eval()` security vulnerability verified with official Python security audits and Sourcery analysis; floating-point precision documented in official Python tutorial; radians/degrees confusion confirmed in Python `math` module docs; operator precedence from authoritative compiler theory sources. |

**Overall confidence:** HIGH

All four research files are grounded in authoritative sources: official documentation (Python, CustomTkinter, pytest), established best practices (Real Python, Hitchhiker's Guide), and verified security research (Sourcery, Leapcell). The domain is mature with decades of established patterns.

### Gaps to Address

**Low confidence areas identified:**

1. **GUI testing specifics for CustomTkinter:** Limited CustomTkinter-specific testing examples found. Tkinter testing patterns should apply (pytest, xvfb), but may require experimentation. **Mitigation:** Research during Phase 6; allocate buffer time for testing strategy validation.

2. **Safe parser performance:** `simpleeval` and `asteval` both claim production-ready, but performance benchmarks are sparse. Need to validate acceptable performance for interactive calculator use (<100ms response time requirement). **Mitigation:** Phase 1 research includes basic performance testing; measure actual latency in prototype.

3. **Polish localization edge cases:** CustomTkinter Unicode support confirmed generally, but Polish-specific decimal separator handling (comma vs period) may need custom logic. Example: Polish users write "3,14" but Python expects "3.14". **Mitigation:** Test during Phase 3 GUI implementation; may need input preprocessing.

4. **History panel scalability threshold:** Research indicates JSON file will slow down after ~10,000 entries, but exact threshold depends on hardware and access patterns. **Mitigation:** Implement size limits in Phase 5 (default 500 items); document upgrade path to SQLite if needed.

**Validation during implementation:**

- **Parser choice:** Build simple prototype in Phase 1 comparing `simpleeval`, `asteval`, and minimal custom parser. Validate security (can it be bypassed?), performance (<100ms for complex expressions), and feature coverage (implicit multiplication, scientific notation).

- **Angle mode UI design:** Mock up prominent angle mode indicator options in Phase 2. User test with 3-5 target users (students, engineers) to validate mode is "impossible to miss."

- **Mode switching performance:** Test show/hide vs destroy/recreate widget patterns in Phase 4. Profile memory usage and transition latency. Target <50ms mode switch time.

## Sources

### Primary (HIGH confidence)

**Official Documentation:**
- [CustomTkinter PyPI](https://pypi.org/project/customtkinter/), [GitHub](https://github.com/TomSchimansky/CustomTkinter), [Official Docs](https://customtkinter.tomschimansky.com/)
- [Python decimal module](https://docs.python.org/3/library/decimal.html), [math module](https://docs.python.org/3/library/math.html)
- [Ruff PyPI](https://pypi.org/project/ruff/), [pytest PyPI](https://pypi.org/project/pytest/), [PyInstaller PyPI](https://pypi.org/project/pyinstaller/)
- [TkDocs Grid Geometry Manager](http://tkdocs.com/tutorial/grid.html)

**Security Research:**
- [Sourcery: Python eval() Detection Vulnerability](https://www.sourcery.ai/vulnerabilities/python-lang-security-audit-eval-detected)
- [Leapcell: Dark Side of Python's eval()](https://leapcell.io/blog/python-eval-how-it-works-and-why-its-risky)
- [TheLinuxCode: eval() Pitfalls and Safer Patterns](https://thelinuxcode.com/eval-in-python-power-pitfalls-and-safer-patterns-you-can-actually-ship/)

**Best Practices:**
- [Structuring Your Project - Hitchhiker's Guide to Python](https://docs.python-guide.org/writing/structure/)
- [Real Python: Python PyQt GUI Calculator (MVC Pattern)](https://realpython.com/python-pyqt-gui-calculator/)
- [Real Python: Python Application Layouts](https://realpython.com/python-application-layouts/)

### Secondary (MEDIUM confidence)

**Feature Analysis:**
- [SSL Shopper: Best Scientific Calculators 2026](https://www.sslshopper.com/reviews/products/best-scientific-calculators/)
- [UXPin: Calculator Design](https://www.uxpin.com/studio/blog/calculator-design/)
- [Nielsen Norman Group: Calculator Tool Recommendations](https://www.nngroup.com/articles/recommendations-calculator/)
- [Calc9: Building Perfect Calculator UI/UX](https://calc9.com/blog/building-the-perfect-calculator-ui-ux-principles/)

**Implementation Patterns:**
- [Medium: Tkinter Best Practices](https://medium.com/tomtalkspython/tkinter-best-practices-optimizing-performance-and-code-structure-c49d1919fbb4)
- [The Python Code: Calculator with Tkinter](https://thepythoncode.com/article/make-a-calculator-app-using-tkinter-in-python)
- [Python Hub: CustomTkinter Calculator](https://python-hub.com/calculator-app-in-python-customtkinter/)

### Tertiary (LOW confidence)

**Community Examples:**
- Various GitHub repositories for calculator projects (code examples, not authoritative architecture)
- Medium articles on general MVC patterns (concepts, not Python-specific verification)
- Performance claims for PyInstaller vs cx_Freeze (sourced from vendor blogs, not independent benchmarks)

---

**Research completed:** 2026-02-05

**Ready for roadmap:** Yes

**Next step:** Create ROADMAP.md defining phases with detailed task breakdown, acceptance criteria, and estimated timelines. Use phase structure suggested above as starting point; refine based on project timeline and priorities.
