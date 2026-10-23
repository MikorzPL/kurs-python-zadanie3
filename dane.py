from typing import Dict
import json
import random
import csv
from typy import FormatPliku
from pathlib import Path

def czytaj_plik(sciezka: Path, format_pliku: FormatPliku) -> int:
    """
    Parametry:
        - sciezka: scieżka do pliku typu Path
        - format_pliku: wartość typu FormatPliku określająca z jakim plikiem pracujemy

    Czyta dane z pliku w podanej lokalizacji, zwraca wartość Czas jeśli Model to A, w przeciwnym przypadku zwraca 0.
    """
    if format_pliku == FormatPliku("c"):
        return czytaj_csv(sciezka)
    elif format_pliku == FormatPliku("j"):
        return czytaj_json(sciezka)
    else:
        raise ValueError("Zły typ pliku")

def czytaj_csv(sciezka: Path) -> int:
    """
    Zwraca wartość czas jezeli Model to A we wskazanym pliku csv
        
    """

    with open(sciezka, newline="", encoding="utf-8") as plik:
        reader = csv.DictReader(plik, delimiter=";")

        for wiersz in reader:
            model = wiersz["Model"].strip()
            czas = wiersz["Czas"].strip().removesuffix("s")

            if model == "A":
                return int(czas)

        return 0

def odczytaj_dane_z_json(sciezka: Path) -> Dict[str, int | str]:
    with open(sciezka) as plik:
        dane = json.load(plik)
        return dane


def czytaj_json(sciezka: Path) -> int:
    """
    Zwraca wartość czas jezeli Model to A we wskazanym pliku json
    """
    dane = odczytaj_dane_z_json(sciezka)
    if dane["Model"] == "A":
        return int(str(dane["Czas"]).removesuffix("s"))
    return 0

def wygeneruj_dane() -> Dict[str, int | str]:
    """
    Proponowana funkcja do generowania losowych danych.
    Zwraca słownik, który można łatwo zapisać do csv jak i json.
    """

    return{
        "Model": random.choice(["A", "B", "C"]),
        "Wynik": random.randint(0, 1000),
        "Czas": str(random.randint(0, 1000)) + "s"
    }

def tworz_plik(sciezka: Path, format_pliku: FormatPliku) -> None:
    """
    Parametry:F
        - sciezka: scieżka do pliku typu Path
        - format_pliku: wartość typu FormatPliku określająca z jakim plikiem pracujemy

    Rozsyła tworzenie do kolejnych metod i wywołuje generowanie danych do zapisanie w pliku.
    """

    dane = wygeneruj_dane();

    if format_pliku == FormatPliku("c"):
        zapisz_dane_do_csv(sciezka, dane)
    elif format_pliku == FormatPliku("j"):
        zapisz_dane_do_json(sciezka, dane)
    else:
        raise ValueError(f"Zły typ pliku")


def zapisz_dane_do_csv(sciezka: Path, dane: Dict[str, int | str]) -> None:
    """
    Prametry:F
        - sciezka: sciezka do pliku typu Path
        - dane: wygenerowane losowe dane które program ma zapisać do pliku

    Tworzy plik na danej ściezce z danymi podanymi w argumencie
    """

    path = Path(sciezka)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", newline="", encoding='utf-8') as plik:

        pola = ["Model", "Wynik", "Czas"]

        writer = csv.DictWriter(
            plik,
            fieldnames=pola,
            delimiter=";"
        )

        writer.writeheader()
        writer.writerow(dane)

def zapisz_dane_do_json(sciezka: Path, dane: Dict[str, int | str]) -> None:
    with open(sciezka, "w", encoding="utf-8") as plik:
        json.dump(dane, plik)