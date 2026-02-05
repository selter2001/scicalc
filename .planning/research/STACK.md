# Technology Stack

**Project:** Python Scientific Calculator with CustomTkinter
**Researched:** 2026-02-05
**Overall Confidence:** HIGH

## Executive Summary

The 2026 standard stack for a professional Python desktop calculator leverages CustomTkinter for modern GUI, Python's decimal module for precision arithmetic, and Ruff for tooling. This stack prioritizes: (1) correctness over performance, (2) minimal dependencies over feature bloat, (3) cross-platform consistency over platform-specific optimization.

**Core philosophy:** Use Python stdlib where possible, add proven third-party libraries sparingly, avoid experimental tools in production code.

---

## Recommended Stack

### Core Framework

| Technology | Version | Purpose | Why | Confidence |
|------------|---------|---------|-----|------------|
| **Python** | 3.10+ | Runtime | Industry standard for desktop apps. 3.10+ required for optimal macOS dark mode support. CustomTkinter supports 3.7+, but 3.10+ gives better type hints and pattern matching. | HIGH |
| **CustomTkinter** | 5.2.2 | GUI Framework | Modern Tkinter wrapper with automatic dark/light mode, cross-platform consistency, minimal dependencies. Active maintenance (13.1k stars, 600 commits, regular updates). Built on stdlib Tkinter = no heavy Qt/GTK dependencies. | HIGH |

**Rationale for CustomTkinter:**
- **Native feel:** Unlike Electron/Qt, leverages OS-native Tkinter. Small footprint, fast startup.
- **Dark mode native:** Built-in theme system adapts to system appearance (Windows 10/11, macOS). No manual theme logic required.
- **Stability:** Based on Python's stdlib Tkinter. If Tkinter works, CustomTkinter works.
- **Polish support:** Unicode-friendly, no localization issues.
- **Active development:** "Update as often as possible" per maintainer. Beta features stabilizing rapidly.

### Mathematical Precision

| Library | Version | Purpose | When to Use | Confidence |
|---------|---------|---------|-------------|------------|
| **decimal** | stdlib | Financial-grade precision | All calculator operations. Default 28 decimal places eliminates float representation errors (e.g., 0.1 + 0.2 = 0.3 exactly). Critical for calculator UX. | HIGH |
| **math** | stdlib | Transcendental functions | Trig (sin, cos, tan), logs, powers, constants (π, e). Use via `Decimal(str(math.sin(float(x))))` for precision preservation. | HIGH |

**Why NOT NumPy/SciPy:**
- **Overkill:** NumPy targets array operations. Calculator is scalar-only.
- **Dependency weight:** ~50MB vs 0MB for stdlib. Breaks "minimal dependencies" constraint.
- **API mismatch:** NumPy types don't play well with GUI widgets expecting Python scalars.

**Precision strategy:**
- Store all user input as `Decimal` immediately upon entry
- Convert to `float` ONLY for `math` functions, then back to `Decimal`
- Set `getcontext().prec` to 28 (default) for display, higher if needed for intermediate calculations
- Display formatted to user's locale (decimal comma vs period for Polish users)

### Code Quality & Tooling

| Tool | Version | Purpose | Why | Confidence |
|------|---------|---------|-----|------------|
| **Ruff** | 0.15.0 | Linter & Formatter | Replaces Black + Flake8 + isort + pyupgrade. 30x faster than Black, >99.9% compatible. Written in Rust = instant feedback. Single tool = simpler CI. | HIGH |
| **Mypy** | 1.x | Type Checker | Dominant type checker with best plugin ecosystem. Slower than Pyright/ty but mature and stable. Run in CI, not pre-commit (too slow). | MEDIUM |
| **pytest** | 9.0.2 | Testing Framework | Industry standard. Clean syntax, rich plugin ecosystem, mature. Requires xvfb for headless GUI testing in CI. | HIGH |

**Ruff configuration:**
```toml
[tool.ruff]
target-version = "py310"
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "UP", "B", "A", "C4", "SIM"]
ignore = ["E501"]  # Line length handled by formatter
```

**Why Ruff over Black + Flake8:**
- **Performance:** Large projects format in milliseconds vs seconds
- **Consolidation:** One tool vs 3-5 separate tools
- **Black compatible:** Drop-in replacement, existing projects migrate easily
- **Future-proof:** Active development, Rust foundation = long-term performance edge

**Why Mypy over Pyright:**
- **Plugin support:** Django/SQLAlchemy plugins (not needed here, but ecosystem signal)
- **Stability:** Mature, well-documented, predictable
- **Tradeoff:** 3-5x slower than Pyright, but acceptable for CI-only usage

**Testing strategy:**
- **Unit tests:** Test calculation logic in isolation (no GUI). Use `pytest` with parametrized tests for edge cases.
- **GUI tests:** Minimal. Separate business logic from presentation. Test button callbacks by mocking Tkinter events.
- **Headless CI:** Use `xvfb-run pytest` on GitHub Actions to test GUI code without display.

### Packaging & Distribution

| Tool | Version | Purpose | When to Use | Confidence |
|------|---------|---------|-------------|------------|
| **PyInstaller** | 6.18.0 | Bundler | Standalone executables for Windows/macOS/Linux. Broader ecosystem than cx_Freeze, better hook support. Use `--onedir` for faster startup vs `--onefile`. | HIGH |
| **Poetry** | 2.x | Package Manager | Modern dependency management with lock files. Use `pyproject.toml` for all config. Better than pip + requirements.txt for reproducible builds. | MEDIUM |

**PyInstaller vs cx_Freeze:**
- **Choose PyInstaller:** Larger community (12.8k stars vs 1.5k), better documentation, more hooks for libraries
- **Tradeoff:** Slower startup with `--onefile` (~50s vs 8s for cx_Freeze). Mitigate by using `--onedir`.
- **Best practice:** Test `--onedir` first (faster startup, easier debugging), switch to `--onefile` only if single-file distribution required.

**Packaging workflow:**
```bash
# Development
poetry install

# Build executable (Windows example)
poetry run pyinstaller --onedir --windowed --name "Calculator" main.py

# Distribute
# Windows: Zip the dist/Calculator/ folder
# macOS: Create .app bundle with py2app (alternative) or PyInstaller
```

### Version Control

| Tool | Purpose | Configuration | Confidence |
|------|---------|---------------|------------|
| **Git** | Version control | Standard GitHub workflow | HIGH |
| **.gitignore** | Ignore patterns | Use GitHub's Python template + CustomTkinter-specific entries | HIGH |

**Critical .gitignore entries:**
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so

# Virtual environments
venv/
env/
ENV/
.venv

# IDE
.vscode/
.idea/
*.swp

# Distribution
build/
dist/
*.egg-info/
*.spec

# Sensitive
.env
config.ini
secrets.json

# OS
.DS_Store
Thumbs.db
```

---

## Alternatives Considered

| Category | Recommended | Alternative | Why Not | Confidence |
|----------|-------------|-------------|---------|------------|
| **GUI Framework** | CustomTkinter | PyQt5/PySide6 | Heavier (250MB vs 1MB), GPL/commercial licensing complexity, overkill for calculator | HIGH |
| | | Kivy | Mobile-first design, less native feel, smaller community for desktop | MEDIUM |
| | | DearPyGUI | Immediate-mode GUI = harder state management for calculator, less mature | LOW |
| **Math Library** | decimal (stdlib) | NumPy | Array library for scalar math, 50MB dependency, precision overkill | HIGH |
| | | mpmath | Arbitrary precision overkill (28 decimals sufficient), slower | MEDIUM |
| **Formatter** | Ruff | Black | Slower (30x), requires additional tools (isort, Flake8), same output | HIGH |
| **Type Checker** | Mypy | Pyright | Faster (3-5x) but no plugin system, less mature ecosystem | MEDIUM |
| | | ty (new) | 10-60x faster but too new (2025 release), unproven in production | LOW |
| **Packager** | PyInstaller | cx_Freeze | Faster startup but smaller community, fewer library hooks | MEDIUM |
| | | Nuitka | C compilation = smallest binary but slower builds, overkill | LOW |
| **Testing** | pytest | unittest | Boilerplate-heavy, less readable, fewer plugins | HIGH |

---

## Installation

### Development Environment Setup

```bash
# 1. Create virtual environment (Python 3.10+)
python3.10 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install Poetry (optional but recommended)
pip install poetry

# 3. Install dependencies via Poetry
poetry install

# Or use pip with requirements.txt
pip install -r requirements.txt
```

### Core Dependencies (`pyproject.toml`)

```toml
[tool.poetry.dependencies]
python = "^3.10"
customtkinter = "^5.2.2"

[tool.poetry.group.dev.dependencies]
ruff = "^0.15.0"
mypy = "^1.0"
pytest = "^9.0"
pyinstaller = "^6.18"
```

### Alternative: requirements.txt

```
# Production
customtkinter==5.2.2

# Development
ruff==0.15.0
mypy==1.0.0
pytest==9.0.2
pyinstaller==6.18.0
```

---

## Project Structure (OOP Best Practices)

Modern Python projects use flat structure with clear separation:

```
calculator/
├── pyproject.toml          # Poetry config, all tool settings
├── .gitignore              # GitHub Python template
├── README.md               # Setup, usage, screenshots
├── src/
│   └── calculator/
│       ├── __init__.py     # Empty (best practice per 2025 guidelines)
│       ├── main.py         # Entry point, app initialization
│       ├── ui/
│       │   ├── __init__.py
│       │   ├── app.py      # Main window, theme setup
│       │   ├── buttons.py  # Button grid layout
│       │   └── display.py  # Display widget
│       ├── logic/
│       │   ├── __init__.py
│       │   ├── calculator.py    # Core calculation engine (Decimal-based)
│       │   └── expression.py    # Expression parser/validator
│       └── history/
│           ├── __init__.py
│           └── manager.py       # History panel logic
└── tests/
    ├── __init__.py
    ├── test_calculator.py       # Unit tests for logic
    └── test_ui.py               # Minimal GUI integration tests
```

**Key principles:**
- **Separation:** UI (`ui/`) never contains math logic. Logic (`logic/`) never imports Tkinter.
- **Testability:** `logic/` is 100% unit-testable without GUI. `ui/` tests mock user events.
- **Empty `__init__.py`:** Normal and recommended (2025 best practice). Share code via explicit imports.
- **pyproject.toml:** Single source of truth for Poetry, Ruff, Mypy, pytest config.

---

## Configuration Files

### pyproject.toml (Comprehensive)

```toml
[tool.poetry]
name = "scientific-calculator"
version = "1.0.0"
description = "Professional scientific calculator with CustomTkinter"
authors = ["Your Name <email@example.com>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.10"
customtkinter = "^5.2.2"

[tool.poetry.group.dev.dependencies]
ruff = "^0.15.0"
mypy = "^1.0"
pytest = "^9.0"
pyinstaller = "^6.18"

[tool.ruff]
target-version = "py310"
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "UP", "B", "A", "C4", "SIM"]
ignore = ["E501"]

[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = "-v --tb=short"
```

---

## Technology Versions Summary

| Component | Version | Release Date | Status |
|-----------|---------|--------------|--------|
| Python | 3.10+ | Oct 2021 (3.10.0) | Stable, LTS |
| CustomTkinter | 5.2.2 | Jan 10, 2024 | Active development |
| Ruff | 0.15.0 | Feb 3, 2026 | Production-ready |
| pytest | 9.0.2 | Dec 6, 2025 | Stable |
| PyInstaller | 6.18.0 | Jan 13, 2026 | Stable |
| Mypy | 1.x | 2024-2025 | Stable |

**Update policy:**
- **Pin exact versions** in `requirements.txt` for reproducibility
- **Use version ranges** in `pyproject.toml` for flexibility (`^5.2.2` = 5.x, not 6.x)
- **Update frequently:** CustomTkinter is under active development. Run `poetry update` monthly.

---

## Cross-Platform Considerations

### Windows
- **Tkinter:** Bundled with Python installer. No extra dependencies.
- **Dark mode:** CustomTkinter auto-detects Windows 10/11 theme.
- **Packaging:** PyInstaller produces `.exe`. Use `--onedir` for antivirus compatibility.

### macOS
- **Tkinter:** Bundled with Python 3.10+ (official python.org installer).
- **Dark mode:** Requires Python 3.10+ for proper title bar theme. 3.9 has quirks.
- **Packaging:** PyInstaller creates `.app` bundle. Code signing recommended for distribution.

### Linux
- **Tkinter:** Install via package manager (`python3-tk` on Debian/Ubuntu).
- **Dark mode:** CustomTkinter reads GTK theme settings.
- **Packaging:** PyInstaller creates binary. Distribute as `.AppImage` or `.deb` for wider compatibility.

**Testing matrix:**
- Develop on macOS/Windows (whichever you use)
- Test on all three platforms before release (use VMs or GitHub Actions)
- CustomTkinter handles platform differences automatically

---

## What NOT to Use

### Anti-Patterns for Calculator Stack

| Technology | Why Avoid | Impact |
|------------|-----------|--------|
| **Electron/Web frameworks** | 200MB runtime for calculator, slow startup, non-native feel | Deal-breaker for lightweight desktop app |
| **NumPy/SciPy** | Array libraries for scalar math, 50MB dependency bloat | Violates minimal dependencies constraint |
| **Flask/Django** | Web frameworks for desktop app, unnecessary complexity | Wrong paradigm |
| **SQLite/databases** | Overkill for in-memory history, adds I/O complexity | History is session-scoped, no persistence needed |
| **eval()** for expressions | Security risk, unpredictable behavior, hard to debug | Use proper expression parser |
| **Global state** | Hard to test, brittle, non-OOP | Use classes with encapsulated state |
| **Threads for GUI** | Tkinter is single-threaded. Threading breaks GUI updates. | Calculator is fast enough without async |

---

## Confidence Assessment

| Area | Confidence | Rationale |
|------|------------|-----------|
| **GUI Framework** | HIGH | CustomTkinter verified via PyPI (5.2.2, Jan 2024), GitHub (13.1k stars, active), official docs. Widely adopted for modern Python desktop apps. |
| **Math Libraries** | HIGH | Python stdlib (decimal, math) is authoritative source. Decimal module designed for financial precision, perfect for calculator. |
| **Code Quality Tools** | HIGH | Ruff 0.15.0 (Feb 2026), pytest 9.0.2 (Dec 2025) verified via PyPI. Ruff adoption growing rapidly (Dagster, others in production). |
| **Packaging** | MEDIUM | PyInstaller 6.18.0 verified via PyPI. Startup performance claim (cx_Freeze faster) sourced from WebSearch, not official benchmarks. Recommend testing both. |
| **Type Checking** | MEDIUM | Mypy vs Pyright comparison from multiple sources, but ty (new tool) claims 10-60x speed. Monitor ty maturity for future migration. |
| **Project Structure** | HIGH | 2025 best practices from Hitchhiker's Guide to Python, Real Python, multiple Medium articles. Consensus on flat structure, empty `__init__.py`. |

**Low confidence areas:**
- **GUI testing specifics:** Limited CustomTkinter-specific testing examples. Tkinter testing patterns should apply, but may require experimentation.
- **Polish localization:** CustomTkinter Unicode support confirmed, but Polish-specific decimal separator (comma vs period) may need custom logic.

---

## Sources

### Official Documentation
- [CustomTkinter PyPI](https://pypi.org/project/customtkinter/) - Version 5.2.2 verification
- [CustomTkinter GitHub](https://github.com/TomSchimansky/CustomTkinter) - Maintenance status, features
- [CustomTkinter Docs](https://customtkinter.tomschimansky.com/) - Official usage guide
- [Python decimal module](https://docs.python.org/3/library/decimal.html) - Precision arithmetic docs
- [Ruff PyPI](https://pypi.org/project/ruff/) - Version 0.15.0 verification
- [pytest PyPI](https://pypi.org/project/pytest/) - Version 9.0.2 verification
- [PyInstaller PyPI](https://pypi.org/project/pyinstaller/) - Version 6.18.0 verification
- [GitHub .gitignore templates](https://github.com/github/gitignore/blob/main/Python.gitignore) - Python patterns

### Ecosystem & Best Practices
- [Python GUI comparison 2026](https://www.pythonguis.com/faq/which-python-gui-library/)
- [Ruff vs Black comparison](https://www.packetcoders.io/whats-the-difference-black-vs-ruff/)
- [PyInstaller vs cx_Freeze 2026](https://ahmedsyntax.com/cx-freeze-vs-pyinstaller/)
- [Python type checking comparison 2025](https://medium.com/@asma.shaikh_19478/python-type-checking-mypy-vs-pyright-performance-battle-fce38c8cb874)
- [Python project structure 2025](https://medium.com/the-pythonworld/the-cleanest-way-to-structure-a-python-project-in-2025-4f04ccb8602f)
- [Structuring Your Project - Hitchhiker's Guide](https://docs.python-guide.org/writing/structure/)

**Verification status:** All core library versions verified via official PyPI pages. Architecture patterns cross-referenced with multiple authoritative sources (Real Python, Python.org, GitHub). Performance claims (Ruff speed, PyInstaller startup) sourced from vendor blogs and verified with user reports.

---

## Final Recommendations

### For This Project (Scientific Calculator)

**Adopt immediately:**
1. **Python 3.10+** - Required for macOS dark mode, better typing
2. **CustomTkinter 5.2.2** - Core GUI requirement, actively maintained
3. **decimal module** - Precision is non-negotiable for calculator
4. **Ruff** - Single tool replaces 3-5 linters/formatters
5. **pytest** - Industry standard, clean syntax

**Adopt with testing:**
1. **PyInstaller** - Test `--onedir` vs `--onefile` for your target platforms
2. **Mypy** - Run in CI only (slow), configure strict mode incrementally

**Monitor but defer:**
1. **ty type checker** - Too new (2025), wait for 1.0 release and adoption
2. **Nuitka** - Compile to C if PyInstaller binaries too large (unlikely)

### Stack Evolution Strategy

**2026:** Use recommended stack as-is.
**2027:** Evaluate Pyright/ty if Mypy becomes bottleneck in CI.
**2028:** Consider migrating to Textual if terminal UI becomes popular (unlikely for calculator).

**Update cadence:**
- **Monthly:** `poetry update` for patch versions
- **Quarterly:** Review CustomTkinter releases for new features
- **Annually:** Re-evaluate type checker, formatter landscape

---

**STACK COMPLETE**
**Ready for roadmap creation.**
