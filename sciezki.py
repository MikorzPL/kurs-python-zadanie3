from dane import tworz_plik
from dane import czytaj_plik
from typy import Miesiac, DzienTygodnia, PoraDnia, TrybPracy, FormatPliku
from typing import Callable, List, Tuple
from pathlib import Path

DOMYSLNA_NAZWA_PLIKU: str = "Dane"


def obsluz_wynik(wynik: int) -> None:
    """
    Funkcja wypisuje wynik dla pliku. Można potencjalnie zastąpić np: zapisem do logów.
    """
    print(f'Suma czasu modeli "A": {wynik=}')


def obsluguj_sciezki(
    dane: List[Tuple[Miesiac, DzienTygodnia, PoraDnia]],
    tryb_pracy: TrybPracy,
    format_pliku: FormatPliku,
    obsluz_wynik: Callable[[int], None] = obsluz_wynik
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

    if tryb_pracy == TrybPracy.TWORZENIE:
        stworz_pliki_z_wejscia(dane, format_pliku)
    else:
        wynik = czytaj_pliki_z_wejscia(dane, format_pliku)
        obsluz_wynik(wynik)

def krotka_na_sciezke(krotka: Tuple[Miesiac, DzienTygodnia, PoraDnia]) -> Path:
    return Path(".") / krotka[0].pelna_nazwa / krotka[1].pelna_nazwa / krotka[2].pelna_nazwa


def stworz_pliki_z_wejscia(dane: List[Tuple[Miesiac, DzienTygodnia, PoraDnia]], format_pliku: FormatPliku) -> None:
    for k in dane:
        sciezka = krotka_na_sciezke(k)
        sciezka.mkdir(parents=True, exist_ok=True)

        pelna_nazwa_pliku = DOMYSLNA_NAZWA_PLIKU + "." + format_pliku.pelna_nazwa
        plik = sciezka / pelna_nazwa_pliku

        if plik.exists():
            continue

        tworz_plik(plik, format_pliku)

def czytaj_pliki_z_wejscia(dane: List[Tuple[Miesiac, DzienTygodnia, PoraDnia]], format_pliku: FormatPliku) -> int:
    wynik = 0

    for k in dane:
        sciezka = krotka_na_sciezke(k)
        pelna_nazwa_pliku = DOMYSLNA_NAZWA_PLIKU + "." + format_pliku.pelna_nazwa
        plik = sciezka / pelna_nazwa_pliku
        
        if not plik.exists():
            # pliki, których nie ma są ignorowane
            # można zmienić
            print(f'Plik: {plik} nie istnieje i zostanie zignorowany')
            continue

        wynik += czytaj_plik(plik, format_pliku)
        
    return wynik
