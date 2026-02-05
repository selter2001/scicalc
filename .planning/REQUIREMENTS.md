# Requirements: SciCalc

**Defined:** 2026-02-05
**Core Value:** Kalkulator musi działać bezbłędnie — poprawne obliczenia z czytelnym, nowoczesnym interfejsem.

## v1 Requirements

### Obliczenia (CALC)

- [ ] **CALC-01**: Użytkownik może wykonać podstawowe operacje: +, -, *, /
- [ ] **CALC-02**: Użytkownik może używać nawiasów do grupowania wyrażeń
- [ ] **CALC-03**: Użytkownik może obliczać funkcje trygonometryczne: sin, cos, tan
- [ ] **CALC-04**: Użytkownik może obliczać pierwiastek kwadratowy (sqrt)
- [ ] **CALC-05**: Użytkownik może potęgować liczby (x^y)
- [ ] **CALC-06**: Użytkownik może obliczać logarytmy: ln (naturalny) i log10
- [ ] **CALC-07**: Użytkownik może obliczać silnię (n!)
- [ ] **CALC-08**: Wyrażenia są parsowane bezpiecznym parserem (nie eval())
- [ ] **CALC-09**: Obliczenia używają modułu decimal dla precyzji (nie float)
- [ ] **CALC-10**: Błędne wyrażenia pokazują czytelny komunikat błędu po polsku

### Tryby i Interakcja (MODE)

- [ ] **MODE-01**: Użytkownik może przełączać między trybem basic i scientific
- [ ] **MODE-02**: W trybie basic widoczne są tylko podstawowe operacje
- [ ] **MODE-03**: W trybie scientific widoczne są wszystkie funkcje naukowe
- [ ] **MODE-04**: Użytkownik może przełączać tryb kątów DEG/RAD
- [ ] **MODE-05**: Aktualny tryb kątów jest wyraźnie widoczny na ekranie
- [ ] **MODE-06**: Użytkownik może wpisywać cyfry i operatory z klawiatury
- [ ] **MODE-07**: Klawiatura obsługuje Enter (oblicz), Backspace (cofnij), Escape (wyczyść)

### Historia (HIST)

- [ ] **HIST-01**: Boczny panel wyświetla listę poprzednich obliczeń
- [ ] **HIST-02**: Kliknięcie wpisu historii wstawia wynik do wyświetlacza
- [ ] **HIST-03**: Użytkownik może wyczyścić historię
- [ ] **HIST-04**: Użytkownik może kopiować wynik (Ctrl+C)
- [ ] **HIST-05**: Użytkownik może wkleić wartość do wyświetlacza (Ctrl+V)

### Interfejs (UI)

- [ ] **UI-01**: Aplikacja używa ciemnego motywu (CustomTkinter dark mode)
- [ ] **UI-02**: Przyciski są zaokrąglone z czytelną typografią
- [ ] **UI-03**: Cały interfejs jest w języku polskim
- [ ] **UI-04**: Okno skaluje się poprawnie przy zmianie rozmiaru (responsywny grid)
- [ ] **UI-05**: Wyświetlacz pokazuje zarówno wyrażenie jak i wynik

### Struktura Projektu (PROJ)

- [ ] **PROJ-01**: Kod jest modularny OOP — logika oddzielona od UI
- [ ] **PROJ-02**: Profesjonalny README.md z opisem, instalacją, uruchomieniem
- [ ] **PROJ-03**: .gitignore odpowiedni dla Pythona
- [ ] **PROJ-04**: requirements.txt z zależnościami
- [ ] **PROJ-05**: Logiczna struktura katalogów (src/ z modułami)

## v2 Requirements

### Rozszerzenia

- **EXT-01**: Przycisk ANS — wstawia ostatni wynik do nowego wyrażenia
- **EXT-02**: Zapis historii do pliku JSON (persystencja między sesjami)
- **EXT-03**: Pakowanie do .exe/.app przez PyInstaller
- **EXT-04**: Tryb GRAD dla kątów (oprócz DEG/RAD)

## Out of Scope

| Feature | Reason |
|---------|--------|
| Wykresy / wizualizacje funkcji | Wysoka złożoność, nie core value kalkulatora |
| Algebra symboliczna (CAS) | Scope creep — to byłby oddzielny produkt |
| Operacje macierzowe | Nie potrzebne w kalkulatorze naukowym v1 |
| Wielojęzyczność (i18n) | Tylko polski — nie komplikujemy v1 |
| Testy jednostkowe | Nie wymagane w v1 |
| Czat w czasie rzeczywistym / cloud sync | Nie dotyczy kalkulatora desktopowego |
| Aplikacja mobilna | Web/desktop first |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| CALC-01 | Phase 1 | Complete |
| CALC-02 | Phase 1 | Complete |
| CALC-03 | Phase 2 | Pending |
| CALC-04 | Phase 2 | Pending |
| CALC-05 | Phase 2 | Pending |
| CALC-06 | Phase 2 | Pending |
| CALC-07 | Phase 2 | Pending |
| CALC-08 | Phase 1 | Complete |
| CALC-09 | Phase 1 | Complete |
| CALC-10 | Phase 1 | Complete |
| MODE-01 | Phase 2 | Pending |
| MODE-02 | Phase 2 | Pending |
| MODE-03 | Phase 2 | Pending |
| MODE-04 | Phase 3 | Pending |
| MODE-05 | Phase 3 | Pending |
| MODE-06 | Phase 3 | Pending |
| MODE-07 | Phase 3 | Pending |
| HIST-01 | Phase 3 | Pending |
| HIST-02 | Phase 3 | Pending |
| HIST-03 | Phase 3 | Pending |
| HIST-04 | Phase 3 | Pending |
| HIST-05 | Phase 3 | Pending |
| UI-01 | Phase 2 | Pending |
| UI-02 | Phase 2 | Pending |
| UI-03 | Phase 2 | Pending |
| UI-04 | Phase 2 | Pending |
| UI-05 | Phase 2 | Pending |
| PROJ-01 | Phase 1 | Complete |
| PROJ-02 | Phase 4 | Pending |
| PROJ-03 | Phase 1 | Complete |
| PROJ-04 | Phase 1 | Complete |
| PROJ-05 | Phase 1 | Complete |

**Coverage:**
- v1 requirements: 32 total
- Mapped to phases: 32
- Unmapped: 0 ✓

---
*Requirements defined: 2026-02-05*
*Last updated: 2026-02-05 after Phase 1 completion — 9 requirements complete*
