# SciCalc - Kalkulator Naukowy

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-green.svg)

## Opis

Profesjonalny kalkulator naukowy z nowoczesnym interfejsem w języku polskim. Aplikacja oferuje dwa tryby pracy (podstawowy i naukowy), ciemny motyw oraz panel historii obliczeń. Wszystkie obliczenia są wykonywane z wykorzystaniem bezpiecznej ewaluacji wyrażeń, co gwarantuje ochronę przed niebezpiecznym kodem.

## Funkcje

- Dwa tryby pracy: podstawowy i naukowy
- Funkcje naukowe: sin, cos, tan, sqrt, potęgowanie (x^y), logarytmy (ln, log10), silnia (n!)
- Stałe matematyczne: pi, e
- Panel historii obliczeń z możliwością ponownego użycia wyników
- Przełącznik trybu kątów DEG/RAD
- Obsługa klawiatury i schowka (Ctrl+C/V)
- Ciemny motyw z zaokrąglonymi przyciskami (CustomTkinter)
- Bezpieczna ewaluacja wyrażeń (simpleeval — bez eval())
- Precyzja obliczeń z użyciem modułu Decimal
- Polskie komunikaty błędów i interfejs

## Zrzuty ekranu

![Kalkulator w trybie podstawowym](assets/screenshots/basic-mode.png)
*Tryb podstawowy*

![Tryb naukowy z funkcjami matematycznymi](assets/screenshots/scientific-mode.png)
*Tryb naukowy z rozszerzonymi funkcjami*

![Panel historii obliczeń](assets/screenshots/history-panel.png)
*Panel historii z listą obliczeń*

## Instalacja

### Wymagania

- Python 3.10 lub nowszy
- pip (menedżer pakietów Python)
- System operacyjny: Windows, macOS, lub Linux

### Kroki instalacji

1. Sklonuj repozytorium:
```bash
git clone https://github.com/username/scicalc.git
cd scicalc
```

2. Utwórz wirtualne środowisko:
```bash
python -m venv venv

# Linux/macOS:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

3. Zainstaluj zależności:
```bash
pip install -r requirements.txt
```

## Użycie

Uruchom kalkulator poleceniem:
```bash
python -m src.calculator.main
```

Otworzy się okno kalkulatora z ciemnym motywem. Możesz przełączać się między trybem podstawowym a naukowym za pomocą przycisku w dolnej części okna. Panel historii wyświetla wszystkie wykonane obliczenia i pozwala na szybkie ponowne użycie wyników.

## Skróty klawiszowe

| Klawisz      | Funkcja                  |
|--------------|--------------------------|
| 0-9          | Cyfry                    |
| +, -, *, /   | Operatory                |
| Enter        | Oblicz wynik             |
| Backspace    | Usuń ostatni znak        |
| Escape       | Wyczyść                  |
| Ctrl+C       | Kopiuj wynik             |
| Ctrl+V       | Wklej                    |

## Struktura projektu

```
src/calculator/
├── config/       # Konfiguracja aplikacji i lokalizacja
│   ├── constants.py    # Stałe konfiguracyjne
│   └── locale.py       # Polskie komunikaty
├── logic/        # Logika kalkulatora i silnik obliczeń
│   ├── calculator_engine.py  # Główny silnik
│   ├── evaluator.py          # Bezpieczna ewaluacja wyrażeń
│   ├── validator.py          # Walidacja wyrażeń
│   └── formatters.py         # Formatowanie wyników
├── ui/           # Komponenty interfejsu użytkownika
│   ├── calculator_view.py    # Główny widok
│   ├── history_panel.py      # Panel historii
│   └── buttons.py            # Definicje przycisków
└── controller/   # Kontroler MVC łączący logikę z UI
    └── calculator_controller.py
```

## Testy

Projekt zawiera 156 testów jednostkowych pokrywających silnik obliczeń, walidację wyrażeń i kontroler.

Uruchom testy:
```bash
pytest tests/
```

## Technologie

- **Python 3.10+** - język programowania
- **CustomTkinter** - nowoczesna biblioteka GUI
- **simpleeval** - bezpieczna ewaluacja wyrażeń matematycznych

## Licencja

Projekt dostępny na licencji MIT. Zobacz [LICENSE](LICENSE) dla szczegółów.

## Autor

Wojciech Olszak
