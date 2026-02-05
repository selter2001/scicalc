# Roadmap: SciCalc — Kalkulator Naukowy

## Overview

Build a professional scientific calculator from greenfield to GitHub-ready release. Start with secure calculation engine and precision handling (critical architectural decisions), layer on CustomTkinter GUI with dual modes (basic/scientific), add history panel and keyboard support, and finish with professional packaging. Each phase delivers working functionality while front-loading security and accuracy decisions that are expensive to change later.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [ ] **Phase 1: Project Foundation & Core Engine** - Project structure, safe parser, decimal-based arithmetic with error handling
- [ ] **Phase 2: Scientific Functions & Basic GUI** - Trigonometric/logarithmic functions, CustomTkinter interface, basic mode operations
- [ ] **Phase 3: Advanced Modes & History** - Scientific mode toggle, angle mode system (DEG/RAD), history panel with keyboard support
- [ ] **Phase 4: Polish & Professional Package** - Final UX refinements, professional documentation, GitHub-ready release

## Phase Details

### Phase 1: Project Foundation & Core Engine
**Goal**: Establish secure calculation foundation with correct arithmetic and professional project structure
**Depends on**: Nothing (first phase)
**Requirements**: PROJ-01, PROJ-03, PROJ-04, PROJ-05, CALC-01, CALC-02, CALC-08, CALC-09, CALC-10
**Success Criteria** (what must be TRUE):
  1. User can execute basic arithmetic operations (+, -, ×, ÷) with parentheses and see correct results
  2. Expressions are parsed safely without eval() vulnerability
  3. Calculations use Decimal precision (no floating-point errors like 0.1+0.2≠0.3)
  4. Invalid expressions show clear Polish error messages instead of crashing
  5. Project has professional structure (src/ with modules, requirements.txt, .gitignore)
**Plans**: 2 plans

Plans:
- [ ] 01-01-PLAN.md — Project scaffolding, directory structure, .gitignore, requirements.txt, config modules (locale.py, constants.py)
- [ ] 01-02-PLAN.md — Core calculation engine with TDD: SafeEvaluator, InputValidator, CalculatorEngine

### Phase 2: Scientific Functions & Basic GUI
**Goal**: Deliver working calculator GUI with all scientific functions in basic mode
**Depends on**: Phase 1
**Requirements**: CALC-03, CALC-04, CALC-05, CALC-06, CALC-07, UI-01, UI-02, UI-03, UI-04, UI-05, MODE-01, MODE-02, MODE-03
**Success Criteria** (what must be TRUE):
  1. User can calculate trigonometric functions (sin, cos, tan), logarithms (ln, log10), square root, exponentiation, and factorial
  2. GUI displays in CustomTkinter dark theme with zaokraglone przyciski and Polish labels
  3. Wyswietlacz shows both current expression and result clearly
  4. User can click buttons to input numbers, operators, and functions
  5. Window scales properly when resized (responsive grid layout)
  6. Basic mode shows only essential operations in clean, uncluttered layout
**Plans**: TBD

Plans:
- [ ] 02-01: TBD
- [ ] 02-02: TBD

### Phase 3: Advanced Modes & History
**Goal**: Complete calculator with scientific mode toggle, angle mode system, history panel, and keyboard control
**Depends on**: Phase 2
**Requirements**: MODE-04, MODE-05, MODE-06, MODE-07, HIST-01, HIST-02, HIST-03, HIST-04, HIST-05
**Success Criteria** (what must be TRUE):
  1. User can toggle between basic and scientific modes (scientific reveals all functions)
  2. User can switch angle mode between DEG and RAD with mode clearly displayed
  3. Trigonometric calculations respect angle mode (sin(30°) = 0.5, sin(30 rad) ≠ 0.5)
  4. History panel shows all previous calculations and user can click any entry to recall result
  5. User can type calculations with keyboard (numbers, operators, Enter for =, Backspace, Escape for clear)
  6. User can copy results (Ctrl+C) and paste values (Ctrl+V)
**Plans**: TBD

Plans:
- [ ] 03-01: TBD
- [ ] 03-02: TBD

### Phase 4: Polish & Professional Package
**Goal**: GitHub-ready professional calculator with comprehensive documentation
**Depends on**: Phase 3
**Requirements**: PROJ-02
**Success Criteria** (what must be TRUE):
  1. README.md includes project description, installation instructions, usage examples, and screenshots
  2. All features work smoothly with no obvious bugs or UI glitches
  3. Calculator feels professional and production-ready
  4. Repository structure is clean and follows Python best practices
  5. Git history shows logical commit progression
**Plans**: TBD

Plans:
- [ ] 04-01: TBD

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Project Foundation & Core Engine | 0/2 | Not started | - |
| 2. Scientific Functions & Basic GUI | 0/2 | Not started | - |
| 3. Advanced Modes & History | 0/2 | Not started | - |
| 4. Polish & Professional Package | 0/1 | Not started | - |

---
*Roadmap created: 2026-02-05*
*Last updated: 2026-02-05 after Phase 1 planning*
