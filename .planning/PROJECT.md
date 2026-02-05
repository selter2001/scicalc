# SciCalc — Kalkulator Naukowy

## What This Is

Profesjonalny kalkulator naukowy w Pythonie z nowoczesnym GUI (CustomTkinter, ciemny motyw). Posiada dwa tryby — podstawowy i naukowy — z bocznym panelem historii obliczeń. Interfejs w języku polskim. Projekt przygotowany pod publiczne repozytorium GitHub z profesjonalną strukturą commitów, README i dokumentacją.

Autor: Wojciech Olszak.

## Core Value

Kalkulator musi działać bezbłędnie — poprawne obliczenia (w tym trygonometria, logarytmy, potęgowanie) z czytelnym, nowoczesnym interfejsem, który robi profesjonalne wrażenie.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Podstawowe operacje: dodawanie, odejmowanie, mnożenie, dzielenie
- [ ] Funkcje naukowe: sin, cos, tan, sqrt, potęgowanie, logarytmy (ln, log10)
- [ ] Przełącznik trybu basic/scientific (kompaktowy vs pełny)
- [ ] Boczny panel historii obliczeń (klikalny — ponowne użycie wyniku)
- [ ] Ciemny motyw z zaokrąglonymi przyciskami (CustomTkinter)
- [ ] Czytelna typografia i nowoczesny wygląd
- [ ] Interfejs w języku polskim
- [ ] Struktura OOP — logika oddzielona od UI (osobne moduły)
- [ ] Profesjonalny README.md z opisem, instalacją, uruchomieniem
- [ ] .gitignore dla Pythona
- [ ] Logiczna historia commitów (profesjonalna struktura Git)

### Out of Scope

- Zapis historii do pliku / bazy danych — historia tylko w ramach sesji
- Testy jednostkowe — nie wymagane w v1
- Eksport obliczeń do pliku
- Wielojęzyczność (i18n) — tylko polski
- Wykresy / wizualizacje funkcji matematycznych

## Context

- Projekt od zera (greenfield), brak istniejącego kodu
- Docelowo publiczne repozytorium GitHub
- CustomTkinter jako biblioteka GUI — wymaga `pip install customtkinter`
- Python 3.10+ (f-stringi, match/case opcjonalnie)
- Struktura plików jak u doświadczonego dewelopera: `src/`, moduły, `requirements.txt`, `venv`

## Constraints

- **Tech stack**: Python 3 + CustomTkinter — bez innych frameworków GUI
- **Zależności**: Minimalne — customtkinter + standardowa biblioteka (math)
- **Platforma**: Cross-platform (Windows/macOS/Linux) dzięki Tkinter
- **Struktura**: Modularna OOP — nie jeden monolityczny plik

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| CustomTkinter zamiast czystego Tkinter | Nowoczesny wygląd out-of-the-box, ciemny motyw natywnie | — Pending |
| Dwa tryby (basic/scientific) | Czystszy UI w trybie basic, pełna funkcjonalność w scientific | — Pending |
| Boczny panel historii | Zawsze widoczny, klikalny, intuicyjny | — Pending |
| Polski interfejs | Preferencja autora | — Pending |
| Historia tylko w sesji | Prostota v1, bez persystencji | — Pending |

---
*Last updated: 2026-02-05 after initialization*
