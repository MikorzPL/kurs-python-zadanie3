from typing import Dict
import json
from typy import FormatPliku
from pathlib import Path

def czytaj_plik(sciezka: Path, format_pliku: FormatPliku) -> int:
    """
    Parametry:
        - sciezka: scieżka do pliku typu Path
        - format_pliku: wartość typu FormatPliku określająca z jakim plikiem pracujemy

    Czyta dane z pliku w podanej lokalizacji, zwraca wartość Czas jeśli Model to A, w przeciwnym przypadku zwraca 0.
    """
    pass

def tworz_plik(sciezka: Path, format_pliku: FormatPliku) -> None:
    """
    Parametry:
        - sciezka: scieżka do pliku typu Path
        - format_pliku: wartość typu FormatPliku określająca z jakim plikiem pracujemy

    Tworzy plik z danymi uzupełnionymi zgodnie z treścią zadania.
    """
    pass

def zapisz_dane_do_json(sciezka: Path, dane: Dict[str, int | str]) -> None:
    with open(sciezka, "w") as plik:
        json.dump(dane, plik)

def odczytaj_dane_z_json(sciezka: Path) -> Dict[str, int | str]:
    with open(sciezka) as plik:
        dane = json.load(plik)
        return dane

def wygeneruj_dane() -> Dict[str, int | str]:
    """
    Proponowana funkcja do generowania losowych danych.
    Zwraca słownik, który można łatwo zapisać do csv jak i json.
    """
    pass