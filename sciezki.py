from typy import Miesiac, DzienTygodnia, PoraDnia, TrybPracy, FormatPliku
from typing import List, Tuple

def obsluguj_sciezki(
    dane: List[Tuple[Miesiac, DzienTygodnia, PoraDnia]],
    tryb_pracy: TrybPracy,
    format_pliku: FormatPliku
) -> None:
    """
    Parametry: 
        - dane: lista krotek w postaci (typy.Miesiac, typy.DzienTygodnia, typy.PoraDnia). 
            Każda krotka to jeden plik w zapytaniu.
            Zakresy dni (pn-czw) będą rozbite na pojedyncze zapytania.
        - tryb_pracy: wartość typy.TrybPracy określająca czy tworzymy czy odczytujemy pliki
        - format_pliku: wartość typy.FormatPliku określająca oczekiwany typ plików

    Wynikiem funkcji jest wywołanie odpowiednich funkcji generowania/odczytywania plików z dane.py w podanych lokalizacjach.
    Dodatkowo jeśli tryb_pracy == ODCZYT funkcja sumuje i podaje wynik odczytu dla kolejnych plików z zapytania.
    """
    pass